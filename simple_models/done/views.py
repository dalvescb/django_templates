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
