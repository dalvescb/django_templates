# relational_models
This project contains examples of models with a variety of different relations, and how to
query and render them into a Django template
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
  django-admin startproject relational_models
  ```

### Creating the examples app
- Make sure you're **inside the project root directory** (with *manage.py* inside it)
- Create the examples app with the command
  ```bash
  python manage.py startapp examples
  ```
- Install the app to *relational_models/relational_models/settings.py*
  ```python
  INSTALLED_APPS = [
    'examples.apps.ExamplesConfig, 
    'django.contrib.admin',
    ...
    ]
  ```

### Routing to the examples app
- Go to *relational_models/relational_models/urls.py* and change the default paths to route to examples.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/', include('examples.urls')), # add me
  ]
  ```
- Then create a file *relational_models/examples/urls.py*
  ```python
  from django.urls import path

  from . import views

  urlpatterns = [
      path(',views.template_view,name="template_view"),
  ]
  ```

### Constructing Models for a Database in models.py
- Define a variety of models for testing out different types of relations in *relational_models/examples/models.py*
  ```python
  from django.db import models

  # Example: Explicit Primary Key
  class ProgrammingLanguage(models.Model):
    PARADIGM_CHOICES = (
        ("FR","Functional"),
        ("IM","Imperative"),
        ("MX","Mixed"),
    )

    name = models.CharField(max_length=30,primary_key=True)
    paradigm = models.CharField(max_length=10,
                                choices=PARADIGM_CHOICES,
                                default="IM")
    is_oo = models.BooleanField()

  # Example: Implicit Primary Key
  class TestModel(models.Model):
    # id   = models.AutoField(primary_key=True)
      # automatically generated (not necessary to add)
    name = models.CharField(max_length=30)

  # Example: One-To-Many Relationship
  class Company(models.Model):
      name = models.CharField(max_length=15)

  class Employee(models.Model):
      name = models.CharField(max_length=30)
      company = models.ForeignKey(Company,
                                  on_delete=models.CASCADE)

  # Example: Many-To-Many Field
  class Class(models.Model):
    name = models.CharField(max_length=30)

  class Student(models.Model):
    name = models.CharField(max_length=30)
    classes = models.ManyToManyField(Class)

  # Example: Recursive Field
  class Person(models.Model):
    name    = models.CharField(max_length=30)
    friends = models.ManyToManyField('self')
            # self references the Person model

  # Example: One-To-One Field
  class Country(models.Model):
      name = models.CharField(max_length=30)

  class President(models.Model):
      name = models.CharField(max_length=30)
      corrupt = models.BooleanField(default=True)
      country = models.OneToOneField(Country,
                                    on_delete=models.CASCADE,
                                    primary_key=True)
  ```
### Handling URLs in views.py
- Now defined a view to query models and render a template in *relational_models/examples/views.py*
  ```python
  from django.shortcuts import render
  from django.db.models import Q
  from . import models

  def template_view(request):
      # construct a list of all language objects as is
      languages = list(models.ProgrammingLanguage.objects.all())

      # construct a dictionary of company names as keys and lists of Employee objects as values
      #   i.e will alow you to display each company with all employees attached
      companies = models.Company.objects.all()
      companiesDict = {}
      for company in companies:
          companiesDict[company.name] = list(models.Employee.objects.filter(company=company))

      # construct a dictionary of class names as keys and a list of Student objects as values
      #   i.e same as above except there will be overlap in lists of Students now
      classes = models.Class.objects.all()
      classesDict = {}
      for class0 in classes:
          classesDict[class0.name] = list(models.Student.objects.filter(classes=class0))

      # construct a list of all of Joe's friends
      joe = models.Person.objects.get(name="Joe")
      jill = models.Person.objects.get(name="Jill")
      friends = models.Person.objects.filter(Q(friends=joe) | Q(friends=jill)).exclude(Q(name="Joe") | Q(name="Jill"))

      # construct a list of tuples of country and president
      presidents = [ (president.name,president.country.name) for president in models.President.objects.all() ]

      # Put all lists and dictionaries into a single context dictionary
      context = { "languages" : languages
                  ,"companies" : companiesDict
                  ,"classes" : classesDict
                  ,"friends" : friends
                  ,"presidents" : presidents }

      return render(request,'models.djhtml',context)
  ```

### Constructing a template to display data from the Database
- Create a new directory to hold templates in *relational_models/examples/templates*
- Then add a new file to it *models.djhtml* with the following content
  ```html
  <!DOCTYPE html>

  <html lang="en">

      <body>

          <h1>This Project Contains Examples of Models With Different Relations</h1>

          <h2>Programming Languages in Database</h2>
          <ul>
          {% for language in languages %}
              <li> {{ language.name }} </li>
          {% endfor %}
          </ul>

          <h2>Companies In Database </h2>
          {% for company,employees in companies.items %}
              <h3> {{  company }} </h3>
              <ul>
                  {% for employee in employees %}
                      <li> {{ employee.name }} </li>
                  {% endfor %}
              </ul>
          {% endfor %}

          <h2>Classes In Database </h2>
          {% for class,students in classes.items %}
              <h3> {{  class }} </h3>
              <ul>
                  {% for student in students %}
                      <li> {{ student.name }} </li>
                  {% endfor %}
              </ul>
          {% endfor %}

          <h2>Friends of Joe and Jill </h2>
          <ul>
          {% for friend in friends %}
              <li> {{ friend.name }} </li>
          {% endfor %}
          </ul>

          <h2> Countries With Presidents </h2>
          <ul>
              {% for president, country in presidents %}
                  <li> {{ country }} is ruled by {{ president }} </li>
              {% endfor %}
          </ul>
      </body>

  </html>
  ```
- **NOTE** how the template uses the *context* dictionary provided from *views.py* in different ways

### Making Mirgrations
- Before we can use our database, we need to get Django to generate it with
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
- **AFTER YOU"VE MADE MIGRATIONS"**: create a script to populate the database in *relational_models/populate_db.py*
```python
from examples import models

def populate():
    # Populate ProgrammmingLanguage Table
    models.ProgrammingLanguage.objects.create(name="python",paradigm="IM",is_oo=True)
    models.ProgrammingLanguage.objects.create(name="haskell",paradigm="FR",is_oo=False)
    models.ProgrammingLanguage.objects.create(name="c",paradigm="IM",is_oo=False)
    models.ProgrammingLanguage.objects.create(name="c++",paradigm="IM",is_oo=True)

    # Populate TestModel Table
    models.TestModel.objects.create(name="TestField1")
    models.TestModel.objects.create(name="TestField2")

    # Populate Company Table
    superInc = models.Company(name="SuperAwesomeInc")
    superInc.save()
    dumbCo = models.Company(name="ReallyDumbCo")
    dumbCo.save()

    # Populate Employee Table
    models.Employee.objects.create(name="GoodEmployee1",company=superInc)
    models.Employee.objects.create(name="GoodEmployee2",company=superInc)
    models.Employee.objects.create(name="GoodEmployee3",company=superInc)
    models.Employee.objects.create(name="GoodEmployee4",company=superInc)

    models.Employee.objects.create(name="BadEmployee1",company=dumbCo)
    models.Employee.objects.create(name="BadEmployee2",company=dumbCo)
    models.Employee.objects.create(name="BadEmployee3",company=dumbCo)

    # Populate Class Table
    class1 = models.Class(name="CS 1XA3")
    class1.save()
    class2 = models.Class(name="CS 1MD3")
    class2.save()

    # Populate the Student Table
    stud1 = models.Student.objects.create(name="GoodStudent1")
    stud1.classes.add(class1)
    stud1.save()
    stud2 = models.Student.objects.create(name="GoodStudent2")
    stud2.classes.add(class1)
    stud2.save()
    stud3 = models.Student.objects.create(name="GoodStudent3")
    stud3.classes.add(class1)
    stud3.save()
    stud4 = models.Student.objects.create(name="GoodStudent4")
    stud4.classes.add(class1,class2)
    stud4.save()

    stud5 = models.Student.objects.create(name="BadStudent1")
    stud5.classes.add(class1,class2)
    stud5.save()
    stud6 = models.Student.objects.create(name="BadStudent2")
    stud6.classes.add(class1,class2)
    stud6.save()
    stud7 = models.Student.objects.create(name="BadStudent3")
    stud7.classes.add(class2)
    stud7.save()

    # Populate the Person Table
    person1 = models.Person.objects.create(name="Jimmy")
    person2 = models.Person.objects.create(name="Joe")
    person3 = models.Person.objects.create(name="Jill")

    person1.friends.add(person2)
    person3.friends.add(person2)

    # Populate the Country Table
    coolVille = models.Country.objects.create(name="CoolVille")
    lameZone = models.Country.objects.create(name="LameZone")

    # Populate the President Table
    models.President.objects.create(name="Jonny Chill",country=coolVille)
    models.President.objects.create(name="Loser McGuy",country=lameZone)
```
- Then exeute the script with the *django shell*, i.e 
```bash
python manage.py shell
  >>> from populate_db import *
  >>> populate()
      # make note, no errors should occur
  >>> exit()
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
- Make database migrations by *cd*-ing into *relational_models* (i.e the directory that contains *manage.py*) and running
```bash
    python manage.py makemigrations

      # Migrations for myapp:
      #   myapp/migrations/XXXX_initial.py 

    python manage.py migrate
      # Operations to perform
      #       ....

```
- Note *XXXX* is the current migration revision number
- THen populate the database with
```bash
python manage.py shell
  >>> from populate_db import *
  >>> populate()
      # make note, no errors should occur
  >>> exit()
```
- Then run the server by running (in the same directory)
  ```bash
  python manage.py runserver localhost:8000
  ```
- Get the server to server you *models.djhtml* by going to 
  **locahost:8000/e/macid/** 

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
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
