from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import Person

# route from:
#       /e/macid/done/first_person/
def first_person_view(request):
    person = Person.objects.first()
    json = { "name" : person.name,
             "age" : person.age }
    return JsonResponse(json)
