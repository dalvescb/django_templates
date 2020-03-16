# simple_ajax
This project shows two ways the client can update with the server
  - Using Django's template language to render HTML files (see https://docs.djangoproject.com/en/3.0/ref/templates/language/)
  - AJAX methods (via JQuery) executed manually in your Javascript code (see https://www.w3schools.com/jquery/jquery_ajax_intro.asp)

Used for Lab Week10

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
  django-admin startproject simple_ajax
  ```
### Creating the ajax app
- Create and install an app named ajax
  - See simple_server *Creating the home app* for details
- Route to the home app in *simple_ajax/urls.py* with the following pattern
  ```python
  from django.urls import path,include

  urlspatterns = [
      path('e/macid/',include('ajax.urls')),
  ]
  ```
### Create templates and static directories
- Create two new directories at the project root (i.e in the same directory as *manage.py*)
  - *simple_ajax/templates* and *simple_ajax/static*
- Create two new directories inside our app directory
  - *simple_ajax/ajax/templates* and *simple_ajax/ajax/templates*

### Create Django Templates (and an accompanying CSS file)
- Create a base template in *simple_ajax/templates/base.djhtml*
  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
        {% load static %}
        <link rel="stylesheet" href="{% static 'styles.css' %}">
        <script
            src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js">
        </script>
        <title>{% block title %}Default Title{% endblock %}</title>
    </head>

    <body>
        <div id="content1">
            {% block content1 %}{% endblock %}
        </div>
        <div id="content2">
            {% block content2 %}{% endblock %}
        </div>
        <div id="content3">
            {% block content3 %}{% endblock %}
        </div>
        {% block script %}{% endblock %}
    </body>
  </html>
  ```
- Create an accompanying CSS file in *simple_ajax/static/styles.css*
  ```css
  body {
    background-color: powderblue;
  }
  #content1 {
    color: red;
  }
  #content2 {
    color: green;
  }
  ```
- Now update *simple_ajax/simple_ajax/settings.py* so that Django can locate our
  new project wide templates directory
  ```python
  TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")], # ADD ME!!!
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
  ]
  ```
- And add the following to the end of *simple_ajax/simple_ajax/settings.py* so
  that Django can locate our new project wide static directory
  ```python
  STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    ]
  ```
- Create a child template in *simple_ajax/ajax/templates/test.djhtml*
  ```html
  {% extends "base.djhtml" %}

  {% block title %}
    Test Page
  {% endblock %}

  {% block content1 %}
    <h1> {{ person.firstName }} and {{ person.age }} </h1>
  {% endblock %}

  {% block content2 %}
    {% if x < 0 %}
        <h2> x is Negative </h2>
    {% elif x == 0 %}
        <h2> x is Zero </h2>
    {% else %}
        <h2> x is Positive </h2>
    {% endif %}

    <ul>
        {% for thing in stuff %}
            <li> {{ thing }} </li>
        {% endfor %}
    </ul>
  {% endblock %}

  {% block content3 %}
    <h1 id="post_out">No Post Recieved Yet</h1>
    <form method="post">
        {% csrf_token %}
        <label for="fname">Name</label><br>
        <input type="text" required="" name="fname" maxlength="150" id="form_id" autofocus="">
        <button type="submit">Clear</button>
    </form>
  {% endblock %}

  {% block script %}
    {% load static %}
    <script>
     $.ajaxSetup({
         headers: { "X-CSRFToken": '{{csrf_token}}' }
     });
    </script>
    <script src="{% static 'test.js' %}"></script>
  {% endblock %}
  ```

### Rendering Django Templates
- Add a view for rendering our template in *simple_ajax/ajax/views.py*
  ```python
  from django.shortcuts import render
  from django.http import JsonResponse

  def test_template_view(request):
      context = { "person" : { "firstName" : "Curt",
                                 "age" : 43 }
                ,"x" : 100
                ,"stuff" : ["one","two","three"] }
      return render(request,'test.djhtml',context)

  def test_ajax_view(request):
      name = request.POST.get('name','NoName')
      data = { 'new_name' : name + ' is dumb' }

      return JsonResponse(data)
  ```
- Don't forget to route to that view in *simple_ajax/ajax/urls.py* (you'll have
  to create this file from scratch)
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('test_template/', views.test_template_view),
      path('test_ajax/', views.test_ajax_view),
  ]
  ```

### Add Javascript code with AJAX
- Add the javascript file linked in our child html template in
  *simple_ajax/ajax/static/test.js*
  ```javascript
  $(document).ready(function() {
    $("#form_id").change(function(){
        let name = $(this).val();

        $.post('/e/macid/test_ajax/'
               ,{ 'name' : name}
               ,function(data,status) {
                   $("#post_out").text(data.new_name);
                   console.log("The reponse was " + data.new_name + "\n with status " + status);
               }
              );
    });
  });
  ```

## Usage 
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Run the server by *cd*-ing into *simple_server* (i.e the directory that
  contains *manage.py*) and running
  ```bash
  python manage.py runserver localhost:8000
  ```
- With the server running, you can have django serve you **test.djhtml** (and its
  static assets) by opening the url *localhost:8000/e/macid/test_template/* in your browser
- To test out AJAX form submission, open your javascript console and start
  entering text into the form. Note the console log when you click off of the
  form

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- To be able to serve static files, you must edit
  *simple_server/simple_server/settings.py* and add/change
  ```python
  # STATIC_URL = '/static/' replace me with
  STATIC_URL = '/u/macid/'  # where macid is your macid
  STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    '/home/macid/public_html/', # uncomment me and change macid
    ]
  ```
- Run the following code to copy all of your static assets to *STATIC_ROOT*
  (make sure you've *cd*-ed into the *simple_server* directory, i.e the one with
  *manage.py*)
  ```bash
  python manage.py collectstatic
  ```
- Lookup your port number from mac1xa3.ca (the webpage) under the Mac1XA3 User
  Ports tab, and run
  ```bash
  python manage.py runserver localhost:portnum
        # where portnum is your port number
  ```
- You can now run all the tests mentioned above but replace *localhost:8000*
  with *mac1xa3.ca* and *macid* with your actual macid
