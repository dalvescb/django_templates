# user_models
This project shows how to use the built in user models, including authentication
## Project Setup
Follow these steps to recreate this template (you probably want to alter some of
these steps a bit, such as selecting a different project or app name)
### Creating the project
- Don't forget to **activate djangoenv**
  ```bash
  conda activate djangoenv
  ```
- The project was created with the command
  ```bash
  django-admin startproject user_models
  ```

### Creating the login app
- Make sure you're **inside the project root directory** (with [manage.py](manage.py) inside it)
- Create the login app with the command
  ```bash
  python manage.py startapp login
  ```
- Install the app to [settings.py](user_models/settings.py)
  ```python
  INSTALLED_APPS = [
    'login.apps.LoginConfig', 
    'django.contrib.admin',
    ...
    ]
  ```
# Creating templates and static files
- While you're editing [setings.py](user_models/settings.py), add a base tempaltes directory by editing
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],  # add me 
        'APP_DIRS': True,
        ...
```
- and add the following to configure static files directories at the bottom of [settings.py](user_models/settings.py)
```python
STATIC_URL = '/u/macid/static/'
STATIC_ROOT = '/home/macid/public_html/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    ]
```
- then create the directories [static](static/) and [templates](templates/)
### Routing to the login app
- Go to [user_models/urls.py](user_models/urls.py) and change the default paths to route to login.urls
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('e/macid/login/', include('login.urls')),
  path('e/macid/admin/', admin.site.urls),
]
```
- Then create a file [done/urls.py](done/urls.py) 
  ```python
  from django.urls import path

  from . import views

  app_name = 'login'

  urlpatterns = [
      path('session/', views.session_view, name="session_view"),
      path('auth/',views.auth_view,name='auth_view'),
      path('private/',views.private_view,name='private_view'),
      path('', views.login_template_view, name="login_view"),
  ]
  ```
- *NOTE* the inclusion of **app_name** allows to distinguish the url names
  between apps in templates
  (should be referenced with {% url app_name:urlname %})
### Handling URLs and Forms in views.py
- Now define a view to render a template and handle our forms in [done/views.py](done/views.py)
  ```python
  from django.http import HttpResponse,HttpResponseNotFound
  from django.shortcuts import render,redirect
  from django.contrib.auth.forms import AuthenticationForm
  from django.contrib.auth import authenticate, login

  from . import models

  def session_view(request):
      i = request.session.get('counter',0)
      request.session['counter'] = i+1

      return HttpResponse('Current Count: %s' % (i+1))

  def login_template_view(request):
      form = AuthenticationForm(request)
      failed = request.session.get('failed',False)
      context = { 'auth_form' : form,
                  'failed' : failed }

      return render(request,'login.djhtml',context)

  def auth_view(request):
      if request.method == 'POST':
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(request, username=username, password=password)
          if user is not None:
              login(request,user)
              request.session['failed'] = False
              return redirect('login:private_view')
          else:
              request.session['failed'] = True
              return redirect('login:login_view')

      return redirect('login:login_view')


  def private_view(request):
      if request.user.is_authenticated:
          context = { 'user' : request.user }
          return render(request,'private.djhtml',context)

      request.session['failed'] = True
      return redirect('login:login_view')
  ```
- *NOTE* the request (HttpRequest) object automatically has attributes
  **session** and **user** because of Django Middleware

### Constructing a Template
- Create a base Django template in
  [templates/base.djhtml](templates/base.djthml) with the content
  ```html
  <!DOCTYPE html>
  <html lang="en">
      <head>
          {% load static %}
          <link rel="stylesheet" href="{% static 'styles.css' %}">
          <title>{% block title %}Default Title{% endblock %}</title>
      </head>

      <body>
          {% block header %}{% endblock %}
          <div id="content">
              {% block content %}{% endblock %}
          </div>
      </body>
  </html>
  ```
- and add a CSS file in [static/styles.css](static/styles.css) with the content
  ```css
  body {
      background-color: lightblue;
  }
  h1 {
      text-align: center;
  }
  #content {
      text-align: center;
  }
  li {
      text-align: left;
  }
  ```
- Next create a new directory to hold templates in
  [login/templates/](login/templates/)
- Then add a new file to it [login.djhtml](login/templates/login.djhtml) with the following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}Login Page{% endblock %}

  {% block header %}
      <h1>Login Page</h1>
  {% endblock %}

  {% block content %}
      <form method="post" id="userauthform" action="{% url 'login:auth_view' %}">
          {% csrf_token %}
          {{ auth_form }}
          <input type="submit" value="Submit" />
      </form>
      {% if failed %}
          <p style="color:red">Incorrect username or password</p>
      {% endif %}
  {% endblock %}
  ```
- **NOTE** how the template uses the *form* created from AuthenticationForm
- Also add a file [private.djhtml](templates/private.djhtml) with the
  following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}Private Page{% endblock %}

  {% block header %}
      <h1>Private Page</h1>
  {% endblock %}

  {% block content %}
      {% if user.is_authenticated %}
          <p>Welcome, {{ user.username }}. Thanks for logging in.</p>
      {% else %}
          <p>Welcome, new user. Please log in.</p>
      {% endif %}
  {% endblock %}
  ```
### Making Migrations
- Even though we haven't made any database models directly, we need to make migrations in order to use the User database
```bash
python manage.py makemigrations
  # Migrations for myapp:
  #   myapp/migrations/XXXX_initial.py 

python manage.py migrate
  # Operations to perform
  #       ....
```
- *Note*: *XXXX* is a revision number that increments each migration, and
  *myapp* is the name of the app the model belongs too
- if you forget what current migration number you're on, list all migrations with
```bash
python manage.py showmigrations
```
### Populating the database
- **AFTER YOU"VE MADE MIGRATIONS"**: you'll need to create at least one User to test out functionality
- The most straight forward way to manually create a user is through the shell, i.e
```bash
python manage.py shell
  >>> from django.contrib.auth.models import User
  >>> user = User.objects.create_user(username='SomeUser',password='1234')
      # creates a user with username SomeUser and password 1234
```
- If you want to make a change and repopulate a fresh database, you can purge the database (without losing all migrations) with
```bash
python manage.py flush
```

## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Make database migrations by *cd*-ing into *user_models* (i.e the directory that contains *manage.py*) and running
```bash
    python manage.py makemigrations

      # Migrations for myapp:
      #   myapp/migrations/XXXX_initial.py 

    python manage.py migrate
      # Operations to perform
      #       ....

```
- Note *XXXX* is the current migration revision number
- Then add users with 
```bash
python manage.py shell
  >>> from django.contrib.auth.models import User
  >>> user = User.objects.create_user(username='SomeUser',password='1234')
      # creates a user with username SomeUser and password 1234
```
- Then run the server by running (in the same directory)
  ```bash
  python manage.py runserver localhost:8000
  ```
- Get the server to server you [login.djhtml](login/templates/login.djhtml) by going to 
  **locahost:8000/e/macid/login/** 
- Enter the username and password you've created to be redirected to [private.djhtml](login/templates/private.djhtml) 

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- Make sure to replace macid at the bottom of
  [settings.py](user_models/settings.py) for dealing with static files
- Make sure the directory **$HOME/public_html/static/** exists (on the server of)
- Run the following command to copy over static files to the above directory
```bash
python manage.py collectstatic
```
- Make the Migrations as in the previous steps
- Populate the Database as in the previous steps
- Lookup your port number from mac1xa3.ca (the webpage) under the Mac1XA3 User
  Ports tab, and run
  ```bash
  python manage.py runserver localhost:portnum
        # where portnum is your port number
  ```
- You can now run all the tests mentioned above but replace *localhost:8000*
  with *mac1xa3.ca* and *macid* with your actual macid
