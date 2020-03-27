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
