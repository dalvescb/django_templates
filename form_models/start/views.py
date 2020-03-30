from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm

from done import models

def home_template_view(request):
    """Serves home.djhtml from /e/macid/ (url name: home_template)
    Parameters
    ----------
      request: (HttpRequest) - expected to be an empty get request
    Returns
    -------
      out: (HttpResponse) - renders home.djhtml
    """
    pcpart_form = models.PCPartForm()
    context = { 'pcpart_form' : pcpart_form,
                }

    return render(request,'home.djhtml',context)
