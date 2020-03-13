from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    return render(request,'home.html')

def home_get(request):
    name = request.GET.get("name","NoNameGiven")
    age = request.GET.get("age","NoAgeGiven")

    html = "<html><body> " + name + " " + age + "</body></html>"
    return HttpResponse(html)


def home_post(request):
    name = request.POST.get("name","NoNameGiven")
    age = request.POST.get("age","NoAgeGiven")

    html = "<html><body> " + name + " " + age + "</body></html>"
    return HttpResponse(html)
