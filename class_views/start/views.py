from django.http import HttpResponse
from django.views import View

# route /e/macid/start/hello/<slug:name>/
# name start:hello-view
class HelloView(View):
    # limits the view to only http get requests
    http_method_names = ['get']

    # implements the corresponding view function
    def get(self,request,*args,**kwargs):
        return HttpResponse('Hello ' + kwargs['name'])
