# simple_app
A simple project that shows how to make a simple app that serves a Hello World poge. Use by Lab Week09

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
  django-admin startproject simple_app
  ```

### Creating the home app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the home app with the command
  ```bash
  python manage.py startapp hello
  ```
- Install the app to *simple_app/simple_app/settings.py*
  ```python
  INSTALLED_APPS = [
    'hello.apps.HelloConfig',  # add this here
    'django.contrib.admin',
    ...
    ]
  ```
   
### Routing to the hello app
- Go to *simple_app/simple_app/urls.py* and change the default paths to route to hello.urls
  ```python
  from django.urls import path, include # add include to imports

  urlpatterns = [
      path('e/macid/', include('hello.urls')), # add me
        # path('admin/', admin.site.urls),
  ]
  ```
- Then create a file *simple_app/hello/urls.py*
  ```python
  from django.urls import path
  from . import views

  urlpatterns = [
    path('',views.hello_view),
  ]
  ```

### Adding A Simple View
- Now we need to create the function *hello_view* in *simple_app/hello/views.py*
  ```python
  from django.http import HttpResponse

  def hello_view(request):
      html = "<html><body>Hello World</body></html>"
      return HttpResponse(html)
  ```
- The above function will html code that the recieving browser will automatically display 

## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Run the server by *cd*-ing into *simple_app* (i.e the directory that
  contains *manage.py*) and running
  ```bash
  python manage.py runserver localhost:8000
  ```
- With the server running, got to *localhost:8000/e/macid/home/* in your browser
- You should recieve a html page that **Displays Hello World** in the body
- If you recieve an error, try reading python errors **From the BOTTOM UP**

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
- To leave the server running in the background (i.e after you've exited your
  ssh session), use the *nohup* command
  ```bash
  nohup python manage.py runserver localhost:portnum &
  ```
- To kill the server (or if you are unable to run the server because your port is taken) use
  ```bash
  killall -SIGKILL python
  ```
