# simple_models
This project contains an example of how to create and run migrations on simple django
models. Note: it only goes over the preliminaries of how to use models

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
  django-admin startproject simple_models
  ```

### Creating the done app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the done app with the command
  ```bash
  python manage.py startapp done
  ```
- Install the app to *simple_models/simple_models/settings.py*
  ```python
  INSTALLED_APPS = [
    'done.apps.DoneConfig,  # add this here
    'django.contrib.admin',
    ...
    ]
  ```

### Routing to the done app
- Go to *simple_models/simple_models/urls.py* and change the default paths to route to done.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/done/', include('done.urls')), # add me
  ]
  ```
- Then create a file *simple_models/done/urls.py*
  ```python
  from django.urls import path

  from . import views

  urlpatterns = [
      path('first_person/',views.get_person_view,name="first_person"),
      path('create_person/<name>/<age>/',views.create_person_view,name="create_person"),
      path('get_person/<name>/<age>/',views.get_person_view,name="get_person"),
      path('filter_person/<age>/',views.filter_person_view,name="filter_person"),
      path('exclude_person/<age>/',views.exclude_person_view,name="exclude_person"),
  ]
  ```

### Handling URLs in views.py
- Now define class based views in *simple_models/done/views.py*
  ```python
  from django.http import HttpResponse,JsonResponse, HttpResponseNotFound
  from django.core.exceptions import ObjectDoesNotExist

  from .models import DPerson

  # route from:
  #       /e/macid/done/first_person/
  def first_person_view(request):
      person = DPerson.objects.first()
      json = { "name" : person.name,
              "age" : person.age }
      return JsonResponse(json)

  # route from:
  #      /e/macid/done/create_person/<name>/<age>/
  def create_person_view(request,name,age):
      new_person = DPerson.objects.create(name=name,age=age)

      new_person.save()
      return HttpResponse("Added new person")

  # route from:
  #      /e/macid/done/get_person/<name>/<age>/
  def get_person_view(request,name,age):
      try:
          person = DPerson.objects.get(name=name,age=age)
          json = { "name" : person.name,
                  "age" : person.age }
          return JsonResponse(json)

      except ObjectDoesNotExist:
          return HttpResponseNotFound("Failed to lookup: (%s,%s)" % (name,age))

  # route from:
  #       /e/macid/done/filter_person/age/
  def filter_person_view(request,age):
      people = DPerson.objects.filter(age=age)
      json = { "names" : [], "ages" : [] }
      for person in people:
          json['names'].append(person.name)
          json['ages'].append(person.age)

      return JsonResponse(json)

  # route from:
  #       /e/macid/done/exclude_person/age/
  def exclude_person_view(request,age):
      people = DPerson.objects.exclude(age=age)
      json = { "names" : [], "ages" : [] }
      for person in people:
          json['names'].append(person.name)
          json['ages'].append(person.age)

      return JsonResponse(json)
  ```

### Making Mirgrations
- Before we can use our database, we need to get Django to generate it with
```bash
python manage.py makemigrations
  # Migrations for myapp:
  #   myapp/migrations/XXXX_initial.py 

python manage.py migrate
  # Operations to perform
  #       ....

python manage.py sqlmigrate myapp XXXX
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
- Make database migrations by *cd*-ing into *simple_models* (i.e the directory that contains *manage.py*) and running
```bash
    python manage.py makemigrations

      # Migrations for myapp:
      #   myapp/migrations/XXXX_initial.py 

    python manage.py migrate
      # Operations to perform
      #       ....

    python manage.py sqlmigrate myapp XXXX
```
- Note *XXXX* is the current migration revision number
- Then run the server by running (in the same directory)
  ```bash
  python manage.py runserver localhost:8000
  ```
- Test out retrieving the first entry in the person table with
  **locahost:8000/e/macid/done/first_person/** 
- Test out adding an entry to the person table with
  **locahost:8000/e/macid/done/create_person/<anyname>/<anyage>/** where anyname 
  and anyage are the entry values
- Test out retrieving a specific entry from the person table with
  **locahost:8000/e/macid/done/create_person/<anyname>/<anyage>/** where anyname 
  and anyage are the entry values
- Test out querying a person by age with
  **locahost:8000/e/macid/done/filter_person/<anyage>/** where anyage is the entry value 
- Test out querying a person by excludign an age with
  **locahost:8000/e/macid/done/exclude_person/<anyage>/** where anyage is the entry value 

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- Make the Migrations in the previous steps
- Lookup your port number from mac1xa3.ca (the webpage) under the Mac1XA3 User
  Ports tab, and run
  ```bash
  python manage.py runserver localhost:portnum
        # where portnum is your port number
  ```
- You can now run all the tests mentioned above but replace *localhost:8000*
  with *mac1xa3.ca* and *macid* with your actual macid
