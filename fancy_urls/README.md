# fancy_urls
This project contains examples of more sophisticated url manipulation, including
capturing values from URLS, parsing regex expression based URL's, referencing
URL's from templates, and redirecting to URL's from the server side

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
  django-admin startproject fancy_url
  ```

### Creating the done app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the done app with the command
  ```bash
  python manage.py startapp done
  ```
- Install the app to *fancy_urls/fancy_urls/settings.py*
  ```python
  INSTALLED_APPS = [
    'done.apps.DoneConfig,  # add this here
    'django.contrib.admin',
    ...
    ]
  ```

### Routing to the done app
- Go to *fancy_urls/fancy_urls/urls.py* and change the default paths to route to done.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/', include('done.urls')), # add me
  ]
  ```
- Then create a file *fancy_urls/done/urls.py*
  ```python
  from django.urls import path, re_path
  from . import views

  app_name = 'done'

  urlpatterns = [
    path('names/jimmy/', views.jimmy_view),
     # special case name
    path('names/<str:name>/', views.name_view),
     # handles any non-empty string name
    path('names/<str:name>/<int:age>/',views.name_age_view),
     # handles any int for an age with a name
    re_path(r'^names2/(?P<name>[a-z]+)/(?P<age>[0-9]{2})/$',views.regex_view),
     # same as above but uses regex to constrain age to two digits

    path('index/',views.index_view),
    path('hello/',views.hello_view,name='hello'),
    path('goodbye/<int:count>/',views.goodbye_view,name='goodbye'),
    path('reverse/',views.reverse_view,name='reverse'),
      # used with the index.djhtml template

    path('unfound/<int:x>/',views.unfound_view),
  ]
  ```

### Serving html templates
- Create the directory *fancy_urls/done/templates/* 
- Add a file *fancy_urls/done/templates/index.html* with the following content
  ```html
  <!DOCTYPE html>

  <html>
    <body>
        <h1> Simple Webpage With A Link </h1>
        <a href="{% url 'done:hello' %}">Go To Hello View</a>
        <a href="{% url 'done:goodbye' 100 %}">Go To Goodbye View</a>
        <a href="{% url 'done:reverse' %}">Go To Goodbye View 1000</a>
    </body>
  </html>
  ```

### Handling URLs in views.py
- Now add a our view functions in *fancy_urls/done/views.py*
  ```python
  from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
  from django.urls import reverse
  from django.shortcuts import render

  # route /done/names/jimmy/
  def jimmy_view(request):
      return HttpResponse("Jimmy is alright I guess")

  # route /done/names/<str:name>/
  def name_view(request,name):
      return HttpResponse(name + " is a real ***hole")

  # route /done/names/<str:name>/<int:age>/
  def name_age_view(request,name,age):
      return HttpResponse(name + " is " + str(age) + " years old, and a ***hole")

  # route /done/^names2/(?P<name>[a-z]+)/(?P<age>[0-9]{2})/$
  def regex_view(request,name,age):
      return HttpResponse(name + " is " + age + " years old, and a ***hole")

  # route /done/index/
  def index_view(request):
      return render(request,'index.djhtml')

  # route /done/hello/
  def hello_view(request):
      return HttpResponse("Hello")

  # route /done/goodbye/<int:count>/
  def goodbye_view(request,count):
      count += 1
      return HttpResponse("Goodbye, " + str(count) + " times")

  # route /done/reverse/
  def reverse_view(request):
      count = 1000
      return HttpResponseRedirect(reverse('done:goodbye',args=(count,)))

  def unfound_view(request,x):
      if x == 0:
          return HttpResponseNotFound()

      return HttpResponse('<h1>Everythings cool</h1>')
  ```

## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Run the server by *cd*-ing into *fancy_urls* (i.e the directory that
  contains *manage.py*) and running
  ```bash
  python manage.py runserver localhost:8000
  ```
- Test out the the url value captures  by going to
  **locahost:8000/e/macid/names/<anyname>/<anyage>/** where anyname and anyage
  are a sample name and age
- Test out the regex url value captures by going to
  **locahost:8000/e/macid/names2/<anyname>/<anyage>/** where anyname and anyage
  are a sample name and age
- Go to **localhost:8000/e/macid/index/** to test out the template url functionality
- Go to **localhost:8000/e/macid/reverse/** to test out Http Redirection
- Go to **localhost:8000/e/macid/unfound/<x>** where x is 0 to test out Http Not Found

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- Lookup your port number from mac1xa3.ca (the webpage) under the Mac1XA3 User
  Ports tab, and run
  ```bash
  python manage.py runserver localhost:portnum
        # where portnum is your port number
  ```
- You can now run all the tests mentioned above but replace *localhost:8000*
  with *mac1xa3.ca* and *macid* with your actual macid
