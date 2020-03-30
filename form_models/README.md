# form_models
This project contains examples of how to automatically generate Html Forms for
Djano Templates from Django Models
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
  django-admin startproject form_models
  ```

### Creating the done app
- Make sure you're **inside the project root directory** (with [manage.py](manage.py) inside it)
- Create the done app with the command
  ```bash
  python manage.py startapp done
  ```
- Install the app to [settings.py](form_models/settings.py)
  ```python
  INSTALLED_APPS = [
    'done.apps.DoneConfig', 
    'django.contrib.admin',
    ...
    ]
  ```
# Creating templates and static files
- While you're editing [setings.py](form_models/settings.py), add a base tempaltes directory by editing
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates")],  # add me 
        'APP_DIRS': True,
        ...
```
- and add the following to configure static files directories at the bottom of [settings.py](form_models/settings.py)
```python
STATIC_URL = '/u/macid/static/'
STATIC_ROOT = '/home/macid/public_html/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    ]
```
- then create the directories [static](static/) and [templates](templates/)
### Routing to the done app
- Go to [form_models/urls.py](form_models/urls.py) and change the default paths to route to done.urls
  ```python
  from django.urls import path,include # add include to imports

  urlpatterns = [
      path('e/macid/', include('done.urls')), # add me
  ]
  ```
- Then create a file [done/urls.py](done/urls.py) 
  ```python
  from django.urls import path
  from . import views

  app_name = 'done'

  urlpatterns = [
      path('pcpart_post/', views.pcpart_post_view, name="pcpart_post"),
      path('', views.home_template_view, name="home_template"),
      ]
  ```
- *NOTE* the inclusion of **app_name** allows to distinguish the url names
  (**pcpart_post** and **home_template**) from the start app in templates
  (should be referenced with {% url app_name:urlname %})

### Constructing Models for a Database in models.py
- Define a variety of models for testing out different types of relations in
  [done/models.py](done/models.py) 
  ```python 
  from django.db import models
  from django import forms

  # Example Models
  PART_CHOICES = (
          ('GPU','GPU'),
          ('RAM','RAM'),
          ('MB','Motherboard'),
          ('CL','Cooler'),
          ('CPU','CPU'),
          )

  class PCBrand(models.Model):
      brand_name = models.CharField(max_length=30,primary_key=True)

      def __str__(self):
          return self.brand_name

  class PCPart(models.Model):
      part_type = models.CharField(max_length=5,choices=PART_CHOICES,default='GPU')
      name = models.CharField(max_length=30,primary_key=True)
      brand = models.ManyToManyField(PCBrand)

  # Used to automatically generate form inputs in template
  class PCBrandForm(forms.ModelForm):
      class Meta:
          model = PCBrand
          fields = ['brand_name']

  class PCPartForm(forms.ModelForm):
      class Meta:
          model = PCPart
          fields = ['part_type','brand']
  ```
- *NOTE* the two **ModelForm** classes will allow use to generate form for
  PCBrand and PCPart in our templates, as well as easily interface them in our views

### Handling URLs and Forms in views.py
- Now define a view to render a template and handle our forms in [done/views.py](done/views.py)
  ```python
  from django.http import HttpResponse,HttpResponseNotFound
  from django.shortcuts import render

  from . import models

  def home_template_view(request):
      pcpart_form = models.PCPartForm()
      context = { 'pcpart_form' : pcpart_form,
                  }

      return render(request,'done/home.djhtml',context)

  def pcpart_post_view(request):
      context = { 'pcparts' : [] }
      if request.method == 'POST':
          # validate that the post contains valid input data for both forms
          part_form = models.PCPartForm(request.POST)
          if part_form.is_valid():
              # values from from input are placed in cleaned_data dictionary
              part_type = part_form.cleaned_data['part_type']
              brand = part_form.cleaned_data['brand']  # NOTE returns a QuerySet
              # now we can use those values to query our PCPart Model
              context['pcparts'] = list(models.PCPart.objects.filter(part_type=part_type,
                                                                    brand__in=brand))
              # NOTE the __in field lookup used on brand is used to check if a m2m field is inside a QuerySet
              return render(request,'done/pcparts.djhtml',context)
          else:
              return HttpResponseNotFound("Form Data Invalid")

      return HttpResponseNotFound()
  ```
- *NOTE* the use of our ModelForm classes to validate POST data (assuming it was
  from the corresponding form) directly

### Constructing a template to display data from the Database
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
  [done/templates/done/](done/templates/done/)
- Note: the extra *done* directory will help distinguish between templates used
  by the *start* and *done* apps
- Then add a new file to it [home.djhtml](done/templates/done/home.djhtml) with the following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}Home Page{% endblock %}

  {% block header %}
      <h1>Home Page</h1>
  {% endblock %}

  {% block content %}
      <h1>PC Part Form</h1>
      <form method="post" id="pcpartform" action="{% url 'done:pcpart_post' %}">
          {% csrf_token %}
          {{ pcpart_form }}
          <input type="submit" value="Submit" />
      </form>
  {% endblock %}
  ```
- **NOTE** how the template uses the *form* created using the ModelForm class to
  insert in *input elements*
- Also add a file [pcparts.djhtml](done/templates/done/pcparts.djhtml) with the
  following content
  ```html
  {% extends 'base.djhtml' %}

  {% block title %}PCParts Page{% endblock %}

  {% block header %}
      <h1>PC Parts List: </h1>
      {% with pcpart=pcparts|first %}
          <h2> {{ pcpart.part_type }} </h2>
      {% endwith %}
  {% endblock %}

  {% block content %}
      <ul>
      {% for pcpart in pcparts %}
          <li> {{ pcpart.name }}  </li>
      {% endfor %}
      </ul>
  {% endblock %}
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
```
- *Note*: *XXXX* is a revision number that increments each migration, and
  *myapp* is the name of the app the model belongs too
- if you forget what current migration number you're on, list all migrations with
```bash
python manage.py showmigrations
```
### Populating the database
- **AFTER YOU"VE MADE MIGRATIONS"**: create a script to populate the database in [populate_db.py](populate_db.py)
```python
from done import models

def populate():
    # Populate PCBrand Table
    nvidia = models.PCBrand.objects.create(brand_name="Nvidia")
    corsair = models.PCBrand.objects.create(brand_name="Corsair")
    cooler = models.PCBrand.objects.create(brand_name="CoolerMaster")
    msi = models.PCBrand.objects.create(brand_name="MSI")
    intel = models.PCBrand.objects.create(brand_name="Intel")
    amd = models.PCBrand.objects.create(brand_name="AMD")

    # Populate PCPart Table
    i9 = models.PCPart.objects.create(part_type='CPU',name="i9 9900k")
    i9.brand.add(intel)
    i9.save()
    ryzen = models.PCPart.objects.create(part_type='CPU',name="Ryzen 5 3600x")
    ryzen.brand.add(amd)
    ryzen.save()
    vengence = models.PCPart.objects.create(part_type='RAM',name="Vengence")
    vengence.brand.add(corsair)
    vengence.save()
    ultracool = models.PCPart.objects.create(part_type='CL',name="UltraCool")
    ultracool.brand.add(cooler)
    ultracool.save()
    b450 = models.PCPart.objects.create(part_type='MB',name="Tomohawk B450")
    b450.brand.add(msi)
    b450.save()
    g2080 = models.PCPart.objects.create(part_type='GPU',name="2080ti")
    g2080.brand.add(nvidia,msi)
    g2080.save()
    g2070 = models.PCPart.objects.create(part_type='GPU',name="2070")
    g2070.brand.add(nvidia,msi)
    g2070.save()
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
- Make database migrations by *cd*-ing into *form_models* (i.e the directory that contains *manage.py*) and running
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
- Get the server to server you *home.djhtml* by going to 
  **locahost:8000/e/macid/done/** 
- Enter in a PC Part and Brand Name to test using a form post and querying the
  database for PC Part names

### Running on mac1xa3.ca
- Make sure the **conda environment is activated** (see **README.md** in parent
  directory)
  ```bash
  conda activate djangoenv
  ```
- To run on mac1xa3.ca you *MUST REPLACE URLS WITH macid TO YOUR ACTUAL MACID*
- Make sure to replace macid at the bottom of
  [settings.py](form_models/settings.py) for dealing with static files
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
