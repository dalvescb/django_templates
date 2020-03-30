from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render

from . import models

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

    return render(request,'done/home.djhtml',context)

def pcpart_post_view(request):
    """Handles form post from /e/macid/pcpart_post/ (url name: pcpart_post)
    Parameters
    ----------
      request: (HttpRequest) - Should be a post request with forms.PCPartForm input
    Returns
    -------
      out: (HttpResponse) - Sends a Success response back
    """
    context = { 'pcparts' : [] }
    if request.method == 'POST':
        # validate that the post contains valid input data for both forms
        part_form = models.PCPartForm(request.POST)
        if part_form.is_valid():
            # values from from input are placed in cleaned_data dictionary
            part_type = part_form.cleaned_data['part_type']
            brand = part_form.cleaned_data['brand']  # NOTE returns a QuerySet
            # now we can use those values to query our PCPart Model
            context['pcparts'] = list(models.PCPart.objects.filter(part_type=part_type,
                                                                   brand__in=brand))
            # NOTE the __in field lookup used on brand is used to check if a m2m field is inside a QuerySet
            return render(request,'done/pcparts.djhtml',context)
        else:
            return HttpResponseNotFound("Form Data Invalid")

    return HttpResponseNotFound()
