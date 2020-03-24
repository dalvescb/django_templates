from django.shortcuts import render

def template_view(request):
    return render(request,'lab11.djhtml')
