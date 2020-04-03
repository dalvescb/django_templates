# user_models_2
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
  django-admin startproject user_models_2
  ```

### Creating the login app
- Make sure you're **inside the project root directory** (with [manage.py](manage.py) inside it)
- Create the login app with the command
  ```bash
  python manage.py startapp login
  ```
- Install the app to [settings.py](user_models_2/settings.py)
  ```python
  INSTALLED_APPS = [
    'login.apps.LoginConfig', 
    'django.contrib.admin',
    ...
    ]
  ```
# Creating templates and static files
- While you're editing [setings.py](user_models_2/settings.py), add a base tempaltes directory by editing
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],  # add me 
        'APP_DIRS': True,
        ...
```
- and add the following to configure static files directories at the bottom of [settings.py](user_models_2/settings.py)
```python
STATIC_URL = '/u/macid/static/'
STATIC_ROOT = '/home/macid/public_html/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    ]
```
- then create the directories [static](static/) and [templates](templates/)
### Routing to the login app
- Go to [user_models_2/urls.py](user_models_2/urls.py) and change the default paths to route to login.urls
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('e/macid/', include('login.urls')),
    path('e/macid/admin/', admin.site.urls),
]
```
- Then create a file [login/urls.py](login/urls.py) 
  ```python
  from django.urls import path

  from . import views

  app_name = 'login'

  urlpatterns = [
      path('session/', views.session_view, name="session_view"),
      path('auth/',views.auth_view,name='auth_view'),
      path('private/',views.private_view,name='private_view'),
      path('login/', views.login_template_view, name="login_view"),
      path('logout/', views.logout_view, name="logout_view"),
      path('signup/', views.signup_template_view, name="signup_view"),
      path('create/', views.user_create_view, name="create_view"),
      path('change/', views.password_change_view, name="change_view"),
  ]
  ```
- *NOTE* the inclusion of **app_name** allows to distinguish the url names
  between apps in templates
  (should be referenced with {% url app_name:urlname %})
### Handling URLs and Forms in views.py
- Now define a view to render a template and handle our forms in [login/views.py](login/views.py)
  ```python
  from django.http import HttpResponse,HttpResponseNotFound
  from django.shortcuts import render,redirect
  from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
  from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
  from django.contrib import messages

  from . import models

  def session_view(request):
      """Illustates the use of the Sessions Middleware
      Parameters
      ---------
        request: (HttpRequest) - assign and use the sessions attribute attached to it
      Returns
      --------
        out: (HttpResponse) - sends back the current count kept in the sessions attribute
      """
      i = request.session.get('counter',0)
      request.session['counter'] = i+1

      return HttpResponse('Current Count: %s' % (i+1))

  def login_template_view(request):
      """Serves lagin.djhtml from /e/macid/login/ (url name: login_view)
      Parameters
      ----------
        request: (HttpRequest) - expected to be an empty get request
      Returns
      -------
        out: (HttpResponse) - renders login.djhtml
      """
      form = AuthenticationForm(request)
      failed = request.session.get('failed',False)
      context = { 'auth_form' : form,
                  'failed' : failed }

      return render(request,'login.djhtml',context)

  def logout_view(request):
      """Redirects to login_view from /e/macid/logout/ (url name: logout_view)
      Parameters
      ----------
        request: (HttpRequest) - expected to be an empty get request
      Returns
      -------
        out: (HttpResponse) - perform User logout and redirects to login_view
      """
      logout(request)
      return redirect('login:login_view')

  def auth_view(request):
      """Authorizes and Logs In a User
      Parameters
      ---------
        request: (HttpRequest) - should contain POST data from AuthenticationForm
      Returns
      --------
        out: (HttpResponse) - should redirect to an authorized page on success, back to login on failure
      """
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
      """Private Page Only an Authorized User Can View
      Parameters
      ---------
        request: (HttpRequest) - should contain an authorized user
      Returns
      --------
        out: (HttpResponse) - if user is authenticated, will render private.djhtml
      """
      if request.user.is_authenticated:
          context = { 'user' : request.user }
          return render(request,'private.djhtml',context)

      request.session['failed'] = True
      return redirect('login:login_view')

  def signup_template_view(request):
      """Serves signup.djhtml from /e/macid/signup (url name: signup_view)
      Parameters
      ----------
        request : (HttpRequest) - expected to be an empty get request
      Returns
      -------
        out : (HttpRepsonse) - renders signup.djhtml
      """
      form = UserCreationForm()
      failed = request.session.get('create_failed',False)
      context = { 'create_form' : form
                  ,'create_failed' : failed }

      return render(request,'signup.djhtml',context)

  def user_create_view(request):
      """Creates a new User
      Parameters
      ----------
        request : (HttpRequest) - expects POST data from create_form
      Returns
      -------
        out : (HttpRepsonse) - if user is successfully created, will login and redirect to private.djhtml
      """
      if request.method == 'POST':
          form = UserCreationForm(request.POST)
          if form.is_valid():
              form.save()
              username = form.cleaned_data.get('username')
              raw_password = form.cleaned_data.get('password1')
              user = authenticate(username=username, password=raw_password)
              login(request, user)
              return redirect('login:private_view')

      request.session['create_failed'] = True
      return redirect('login:signup_view')

  def password_change_view(request):
      if not request.user.is_authenticated:
          redirect('login:login_view')

      if request.method == 'POST':
          form = PasswordChangeForm(request.user, request.POST)
          if form.is_valid():
              user = form.save()
              update_session_auth_hash(request, user)
              return redirect('login:login_view')
      else:
          form = PasswordChangeForm(request.user)
      context = { 'user' : request.user
                  ,'change_form' : form }
      return render(request, 'change.djhtml',context)
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
          {% block csslinks %}
          {% endblock %}
          <title>{% block title %}Default Title{% endblock %}</title>
      </head>

      <body>
          {% block header %}{% endblock %}
          <div id="content">
              {% block content %}{% endblock %}
          </div>
          {% block script %}
          {% endblock %}
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

  {% block csslinks %}
      {% load static %}
      <link rel="stylesheet" href="{% static 'w3login.css' %}">
  {% endblock %}

  {% block title %}Login Page{% endblock %}

  {% block header %}
      <h1>Login Page</h1>
  {% endblock %}

  {% block content %}
  <!-- Button to open the modal login form -->
  <button onclick="document.getElementById('id01').style.display='block'">Login</button>

  <!-- The Modal -->
  <div id="id01" class="modal">
    <span onclick="document.getElementById('id01').style.display='none'"
  class="close" title="Close Modal">&times;</span>

    <!-- Modal Content -->
    <form class="modal-content animate" method="post" action="{% url 'login:auth_view' %}">
        {% csrf_token %}
        <!-- <div class="imgcontainer">
            <img src="img_avatar2.png" alt="Avatar" class="avatar">
            </div>
        -->
      <div class="container">
              <label for="uname"><b>Username</b></label>
              <input type="text" placeholder="Enter Username" name="username" required>

              <label for="psw"><b>Password</b></label>
              <input type="password" placeholder="Enter Password" name="password" required>
        <button type="submit">Login</button>
        <label>
          <input type="checkbox" checked="checked" name="remember"> Remember me
        </label>
      </div>

      <div class="container" style="background-color:#f1f1f1">
        <button type="button" onclick="document.getElementById('id01').style.display='none'" class="cancelbtn">Cancel</button>
        <span class="psw">Forgot <a href="#">password?</a></span>
      </div>
    </form>
  </div>
  {% endblock %}

  {% block script %}
      <script>
      // Get the modal
      var modal = document.getElementById('id01');

      // When the user clicks anywhere outside of the modal, close it
      window.onclick = function(event) {
          if (event.target == modal) {
              modal.style.display = "none";
          }
      }
      </script>
  {% endblock %}
  ```
- **NOTE** the template makes use of forms from w3schools (i.e https://www.w3schools.com/howto/howto_css_login_form.asp)
- Also add a file [private.djhtml](login/templates/private.djhtml) with the
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
          <form method="post" action="{% url 'login:logout_view' %}">
              {% csrf_token %}
              <button type="submit">Logout</button>
          </form>
          <a href="{% url 'login:change_view' %}">Change Password</a>
      {% else %}
          <p>Welcome, new user. Please log in.</p>
      {% endif %}
  {% endblock %}
  ```
- And a file [change.djhtml](login/templates/change.djhtml) with the
  following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}Change Page {{ user.username }} {% endblock %}

  {% block header %}
      <h1>Change Page</h1>
  {% endblock %}

  {% block content %}
      <form method="post" id="change_form" action="{% url 'login:change_view' %}">
          {% csrf_token %}
          {{ change_form }}
          <input type="submit" value="Submit" />
      </form>
  {% endblock %}
  ```
- And a file [signup.djhtml](login/templates/signup.djhtml) with the
  following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}Signup Page{% endblock %}

  {% block header %}
      <h1>Signup Page</h1>
  {% endblock %}

  {% block content %}
      <form method="post" id="create_form" action="{% url 'login:create_view' %}">
          {% csrf_token %}
          {{ create_form }}
          <input type="submit" value="Submit" />
      </form>
      {% if create_failed %}
          <p style="color:red"> Invalid username or password </p>
      {% endif %}
  {% endblock %}
  ```
- And finally create a CSS file [w3login.css](login/static/w3login.css) (also
  taken from w3schools to support login.djhtml) with the content
  ```css
  /* Bordered form */
  form {
    border: 3px solid #f1f1f1;
  }

  /* Full-width inputs */
  input[type=text], input[type=password] {
    width: 100%;
    padding: 12px 20px;
    margin: 8px 0;
    display: inline-block;
    border: 1px solid #ccc;
    box-sizing: border-box;
  }

  /* Set a style for all buttons */
  button {
    background-color: #4CAF50;
    color: white;
    padding: 14px 20px;
    margin: 8px 0;
    border: none;
    cursor: pointer;
    width: 100%;
  }

  /* Add a hover effect for buttons */
  button:hover {
    opacity: 0.8;
  }

  /* Extra style for the cancel button (red) */
  .cancelbtn {
    width: auto;
    padding: 10px 18px;
    background-color: #f44336;
  }

  /* Center the avatar image inside this container */
  .imgcontainer {
    text-align: center;
    margin: 24px 0 12px 0;
  }

  /* Avatar image */
  img.avatar {
    width: 40%;
    border-radius: 50%;
  }

  /* Add padding to containers */
  .container {
    padding: 16px;
  }

  /* The "Forgot password" text */
  span.psw {
    float: right;
    padding-top: 16px;
  }

  /* Change styles for span and cancel button on extra small screens */
  @media screen and (max-width: 300px) {
    span.psw {
      display: block;
      float: none;
    }
    .cancelbtn {
      width: 100%;
    }
  }

  /* The Modal (background) */
  .modal {
    display: none; /* Hidden by default */
    position: fixed; /* Stay in place */
    z-index: 1; /* Sit on top */
    left: 0;
    top: 0;
    width: 100%; /* Full width */
    height: 100%; /* Full height */
    overflow: auto; /* Enable scroll if needed */
    background-color: rgb(0,0,0); /* Fallback color */
    background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
    padding-top: 60px;
  }

  /* Modal Content/Box */
  .modal-content {
    background-color: #fefefe;
    margin: 5px auto; /* 15% from the top and centered */
    border: 1px solid #888;
    width: 80%; /* Could be more or less, depending on screen size */
  }

  /* The Close Button */
  .close {
    /* Position it in the top right corner outside of the modal */
    position: absolute;
    right: 25px;
    top: 0;
    color: #000;
    font-size: 35px;
    font-weight: bold;
  }

  /* Close button on hover */
  .close:hover,
  .close:focus {
    color: red;
    cursor: pointer;
  }

  /* Add Zoom Animation */
  .animate {
    -webkit-animation: animatezoom 0.6s;
    animation: animatezoom 0.6s
  }

  @-webkit-keyframes animatezoom {
    from {-webkit-transform: scale(0)}
    to {-webkit-transform: scale(1)}
  }

  @keyframes animatezoom {
    from {transform: scale(0)}
    to {transform: scale(1)}
  }
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

## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Make database migrations by *cd*-ing into *user_models_2* (i.e the directory that contains *manage.py*) and running
```bash
    python manage.py makemigrations

      # Migrations for myapp:
      #   myapp/migrations/XXXX_initial.py 

    python manage.py migrate
      # Operations to perform
      #       ....

```
- Note *XXXX* is the current migration revision number
- Then run the server by running (in the same directory)
  ```bash
  python manage.py runserver localhost:8000
  ```
- Get the server to server you [signup.djhtml](login/templates/signup.djhtml) by going to 
  **locahost:8000/e/macid/signup/** 
- Get the server to server you [login.djhtml](login/templates/login.djhtml) by going to 
  **locahost:8000/e/macid/login/**  
  - Enter the username and password you created at the SignUp page to get the
    server to serve you [private.djhtml](login/templates/private.djhtml)
- Get the server to server you [change.djhtml](login/templates/change.djhtml) by going to 
  **locahost:8000/e/macid/change/** 

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- Make sure to replace macid at the bottom of
  [settings.py](user_models_2/settings.py) for dealing with static files
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
