# class_views
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
  django-admin startproject class_view
  ```

### Creating the done app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the done app with the command
  ```bash
  python manage.py startapp done
  ```
- Install the app to *class_views/class_views/settings.py*
  ```python
  INSTALLED_APPS = [
    'done.apps.DoneConfig,  # add this here
    'django.contrib.admin',
    ...
    ]
  ```

### Routing to the done app
- Go to *class_views/class_views/urls.py* and change the default paths to route to done.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/done/', include('done.urls')), # add me
  ]
  ```
- Then create a file *class_views/done/urls.py*
  ```python
  from django.urls import path

  from .views import HelloView,IndexPageView,GoToIndexView
  from django.views.generic.base import RedirectView

  urlpatterns = [
      path('hello/<slug:name>/', HelloView.as_view(), name="hello-view"),
      path('index/<slug:name>/', IndexPageView.as_view(), name="index-view"),
      path('redirect/<slug:name>/', GoToIndexView.as_view(), name='redirect-view'),
      path('go-to-google/',RedirectView.as_view(url="https://google.ca"),name="go-to-google-view"),
  ]
  ```

### Serving html templates
- Create the directory *class_views/done/templates/* 
- Add a file *class_views/done/templates/index.html* with the following content
  ```html
  <!DOCTYPE html>

  <html>
      <body>
          <h1> Test Template View Page </h1>
          <h2> With Name: {{ name }} </h2>
      </body>
  </html>
  ```

### Handling URLs in views.py
- Now define class based views in *class_views/done/views.py*
  ```python
  from django.http import HttpResponse
  from django.views import View
  from django.views.generic.base import TemplateView
  from django.views.generic.base import RedirectView

  class HelloView(View):
      # limits the view to only http get requests
      http_method_names = ['get']

      # implements the corresponding view function
      def get(self,request,*args,**kwargs):
          return HttpResponse('Hello ' + kwargs['name'])

  class IndexPageView(TemplateView):

      template_name = 'index.djhtml'

      def get_context_data(self,**kwargs):
          context = super().get_context_data(**kwargs)
          context['name'] = kwargs['name']

          return context

  class GoToIndexView(RedirectView):
      permanent = False
      query_string = True
      pattern_name = 'index-view'

      def get_redirect_url(self, *args, **kwargs):
          return super().get_redirect_url(*args,**kwargs)
  ```

## Usage
The project can be run as is locally but will require some alteration to run on mac1xa3.ca

### Running A Local Server (For Debugging Purposes)
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- Run the server by *cd*-ing into *class_views* (i.e the directory that
  contains *manage.py*) and running
  ```bash
  python manage.py runserver localhost:8000
  ```
- Test out the the HelloView class based view by going to 
  **locahost:8000/e/macid/done/hello/<anyname>/** where anyname 
  is any string of word character and/or hyphens
- Test out the the IndexPageView class based view by going to 
  **locahost:8000/e/macid/done/index/<anyname>/** where anyname 
  is any string of word character and/or hyphens
- Test out the the GoToIndexView class based view by going to 
  **locahost:8000/e/macid/done/redirect/<anyname>/** where anyname 
  is any string of word character and/or hyphens
- Test out the the built-in RedirectView class based view by going to 
  **locahost:8000/e/macid/done/go-to-google/** 

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
