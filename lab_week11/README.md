# lab_week11
This project is the starting point for the lab week11 activity. Please follow the activity instructions 
given to complete
## Project Setup
The project was creating using the following steps *NOTE* you do not need to do
this to complete the lab activity, follow the steps in
1XA3\_LabActivity\_Week11.pdf to complete the lab
### Creating the project
- Don't forget to **activate djangoenv**
  ```bash
  conda activate djangoenv
  ```
- The project was created with the command
  ```bash
  django-admin startproject lab_week11
  ```

### Creating the start app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the start app with the command
  ```bash
  python manage.py startapp start
  ```
- Install the app to *lab_week11/lab_week11/settings.py*
  ```python
  INSTALLED_APPS = [
    'home.apps.StartConfig,  # add this here
    'django.contrib.admin',
    ...
    ]
  ```
- Comment out the CSRF token middleware (needed to test POST Requests with curl)
  ```python
  MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware', COMMENT THIS OUT
    ...
    ]
  ```

### Routing to the start app
- Go to *lab_week11/lab_week11/urls.py* and change the default paths to route to start.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/start/', include('start.urls')), 
  ]
  ```
- Then create a file *lab_week11/start/urls.py*
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
      path('template_test/',views.template_view,name="template-view"),
    ]
  ]
  ```

### Serving html templates
- Now we need to create the function *home_view* in *lab_week11/start/views.py*
  ```python
  from django.shortcuts import render

  def template_view(request):
      return render(request,'lab11.djhtml')
  ```
- The above function will serve a file *lab11.djhtml* 
- The function *render* will automatically look for html files in *templates* directories
- Create the directory *lab_week11/start/templates/* 
- Add a file *lab_week11/start/templates/lab11.djhtml* with the following content
  ```html
  <!DOCTYPE html>

  <html>
      <body>
          <h1> TODO REPLACE ME WITH TEMPLATE VARIABLE </h1>
      </body>
  </html>
  ```
### Serving static files
- To link static files (assets like css, javascript, images, videos, etc) create
  another directory to hold them *lab_week11/start/static/*
- Try adding an image *lab_week11/start/static/test.jpeg*


## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Run the server by *cd*-ing into *lab_week11* (i.e the directory that
  contains *manage.py*) and running
  ```bash
  python manage.py runserver localhost:8000
  ```
- With the server running, you can have django serve you **lab11.djhtml** (and its
  static assets) by opening the url *localhost:8000/e/macid/test_template/* in your browser

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- To be able to serve static files, you must edit
  *lab_week11/lab_week11/settings.py* and add/change
  ```python
  STATIC_URL = '/u/macid/static/'  # where macid is your macid
  STATIC_ROOT = '/home/macid/public_html/static/'
        # where macid is your macid
  ```
- *NOTE* make sure to create the directory */home/macid/public_html/static/* on
  the server with mkdir if it doesn't already exist
- Run the following code to copy all of your static assets to *STATIC_ROOT*
  (make sure you've *cd*-ed into the *lab_week11* directory, i.e the one with
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
