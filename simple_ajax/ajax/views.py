from django.shortcuts import render
from django.http import JsonResponse

def test_template_view(request):
    context = { "person" : { "firstName" : "Curt",
                                 "age" : 43 }
                ,"x" : 100
                ,"stuff" : ["one","two","three"] }
    return render(request,'test.djhtml',context)

def test_ajax_view(request):
    name = request.POST.get('name','NoName')
    data = { 'new_name' : name + ' is dumb' }

    return JsonResponse(data)
