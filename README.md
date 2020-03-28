# django_templates
A collection of Django Project Templates for CS 1XA3 McMaster

## Usage
- See https://docs.anaconda.com/anaconda/install/ for info on how to **Install Anaconda**
- All of the templates are meant to be run inside a **conda environment** that can be installed through **environment.yml**
  ```bash
  conda env create -f environment.yml
     # will create a new environment djangoenv
  conda info --envs
     # will show a list of available environments (djangoenv should be listed now)
  ```
- This will install an environment named **djangoenv** on your system, remember to activate it with
  ```bash
  conda activate djangoenv
     # (djangoenv) should appear on the left of your shell prompt now
  ```
- When you are finished you can deactivate with
  ```bash
  conda deactivate
     # (base) should return to the left of your shell prompt
  ```
- Each template *contains its own README.md* that specifies how to **run and recreate** the template

### Creating Your Own Project
- I recommend you don't modify these templates, but rather recreate the parts of
  each template yourself, using the template and it's README.md as a reference
- To create a new django project, **make sure djangoenv is activated** (see
  above), and use **django-admin** to create a new project
  ```bash
  django-admin startproject <proj_name>
    # creates a new project with the name <proj_name>
  ```

## Templates Overview
  - **simple_app** template shows how to setup a simple as possible Django
    project with a single app that serves Hello World! (constructed in **lab week09**)
  - **simple_server** template shows how to serve html documents with static
    assets like javascript, and respond to basic http get/posts (constructed in
    **lecture week09**)
  - **simple_ajax** template shows two ways the client can update with the server
     - Using Django's template language to render HTML files (see https://docs.djangoproject.com/en/3.0/ref/templates/language/)
     - AJAX methods (via JQuery) executed manually in your Javascript code (see
     https://www.w3schools.com/jquery/jquery_ajax_intro.asp) 
     - constructed in **lab week10**
  - **fancy_urls** template contains examples of more sophisticated url
    manipulation, including capturing values from URLS, parsing regex expression
    based URL's, referencing URL's from templates, and redirecting to URL's from
    the server side (constructed in **lecture week 10**)
  - **class_views** template contains examples of more sophisticated url
    manipulation, including capturing values from URLS, parsing regex expression
    based URL's, referencing URL's from templates, and redirecting to URL's from
    the server side (constructed in **lecture week 10**)
  - **simple_models** template contains an example of how to create and run
    migrations on simple django models (i.e constructing a database). Note: it
    only goes over the preliminaries of how to use models (construct in **lab week 11**)
  - **relational_models** contains examples of models with a variety of
    different relations, and how to query and render them into a Django
    template. Use in **lecture week 11**
