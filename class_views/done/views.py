from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.views.generic.base import RedirectView

class HelloView(View):
    # limits the view to only http get requests
    http_method_names = ['get']

    # implements the corresponding view function
    def get(self,request,*args,**kwargs):
        return HttpResponse('Hello ' + kwargs['name'])

class IndexPageView(TemplateView):

    template_name = 'index.djhtml'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = kwargs['name']

        return context

class GoToIndexView(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'index-view'

    def get_redirect_url(self, *args, **kwargs):
        return super().get_redirect_url(*args,**kwargs)
