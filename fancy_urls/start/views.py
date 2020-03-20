from django.http import HttpResponse

# route /e/macid/start/names/<str:name>/
def name_view(request,name):
    return HttpResponse(name + " is a real ***hole")
