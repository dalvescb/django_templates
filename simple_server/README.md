# simple_server
A simple project that shows how to serve html, static assets, and respond to
GET/POST requests. Used for Lecture Week09

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
  django-admin startproject simple_server
  ```

### Creating the home app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the home app with the command
  ```bash
  python manage.py startapp home
  ```
- Install the app to *simple_server/simple_server/settings.py*
  ```python
  INSTALLED_APPS = [
    'home.apps.HomeConfig',  # add this here
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
### Routing to the home app
- Go to *simple_server/simple_server/urls.py* and change the default paths to route to home.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/', include('home.urls')), # add me
        # path('admin/', admin.site.urls),
  ]
  ```
- Then create a file *simple_server/home/urls.py*
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
    path('',views.home_view),
  ]
  ```

### Serving html templates
- Now we need to create the function *home_view* in *simple_server/home/views.py*
  ```python
  from django.shortcuts import render

  def home_view(request):
      return render(request,'home.html')
  ```
- The above function will serve a file *home.html* 
- The function *render* will automatically look for html files in *templates* directories
- Create the directory *simple_server/home/templates/* 
- Add a file *simple_server/home/templates/home.html* with the following content
  ```html
  <!DOCTYPE html>
  <html lang="en">
    <head>
       <title>Home Page</title>
        <script
            src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js">
        </script>
    </head>
    <body>
     Home Webpage
    </body>
  </html>
  ```

### Serving static files
- To link static files (assets like css, javascript, images, videos, etc) create
  another directory to hold them *simple_server/home/static/*
- Try adding an image *simple_server/home/static/some_img.jpg*
- Then link to the image in *simple_server/home/templates/home.html* by **adding the following code to the body**
  ```html
  {% load static %}
  <img src="{% static 'some_img.jpg' %}">
  ```

### Including custom javascript files
- Javascript files also count as static files
- Add the following to *simple_server/home/templates/home.html* **at the bottom of the body**
  ```html
  <button>Click Me</button>
  {% load static %}
  <script src="{% static 'home.js' %}"></script>
  ```
- Then add the javascript file to *simple_server/home/static/home.js*
  ```javascript
  $(document).ready(function(){
    $("button").click(function(){
      $("img").hide();
    });
  });
  ```

### Handling A Get Request
- Add a route for a get request in *simple_server/home/urls.py*
  ```python
  urlpatterns = [
    ...
    path('get_test/',views.home_get,name='home_get'), # add this
  ]
  ```
- Now add a function **home_get** in *simple_server/home/views.py*
  ```python
  def home_get(request):
      name = request.GET.get("name","NoNameGiven")
      age = request.GET.get("age","NoAgeGiven")

      html = "<html><body> " + name + " " + age + "</body></html>"
      return HttpResponse(html)
  ```

### Handling A Post Request
- Add a route for a get request in *simple_server/home/urls.py*
  ```python
  urlpatterns = [
    ...
    path('post_test/',views.home_post,name='home_post'), # add this
  ]
  ```
- Now add a function **home_post** in *simple_server/home/views.py*
  ```python
  def home_post(request):
      name = request.POST.get("name","NoNameGiven")
      age = request.POST.get("age","NoAgeGiven")

      html = "<html><body> " + name + " " + age + "</body></html>"
      return HttpResponse(html)
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
- With the server running, you can have django serve you **home.html** (and its
  static assets) by opening the url *localhost:8000/e/macid/* in your browser
- With the server running, you can send a get request by opening the url
  *localhost:8000/e/macid/get_test/?name=Curtis&age=43* in your browser (and you
  can change around the parameters name and age)
- You can't send a POST request directly through the browser because there is
  no way of specifying parameters. Short of writing some javascript, you can
  test it by using the *curl* program like so
  ```bash
  curl -X POST "localhost:8000/e/macid/post_test/" -d "name=Curtis&age=43" -m 30 -v
  ```

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
  STATIC_ROOT = '/home/macid/public_html/' # add me
        # where macid is your macid
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
