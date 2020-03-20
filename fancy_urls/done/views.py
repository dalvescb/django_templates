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
