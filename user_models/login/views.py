from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login

from . import models

def session_view(request):
    """Illustates the use of the Sessions Middleware
    Parameters
    ---------
      request: (HttpRequest) - assign and use the sessions attribute attached to it
    Returns
    --------
      out: (HttpResponse) - sends back the current count kept in the sessions attribute
    """
    i = request.session.get('counter',0)
    request.session['counter'] = i+1

    return HttpResponse('Current Count: %s' % (i+1))

def login_template_view(request):
    """Serves lagin.djhtml from /e/macid/login/ (url name: login_template)
    Parameters
    ----------
      request: (HttpRequest) - expected to be an empty get request
    Returns
    -------
      out: (HttpResponse) - renders login.djhtml
    """
    form = AuthenticationForm(request)
    failed = request.session.get('failed',False)
    context = { 'auth_form' : form,
                'failed' : failed }

    return render(request,'login.djhtml',context)

def auth_view(request):
    """Authorizes and Logs In a User
    Parameters
    ---------
      request: (HttpRequest) - should contain POST data from AuthenticationForm
    Returns
    --------
      out: (HttpResponse) - should redirect to an authorized page on success, back to login on failure
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['failed'] = False
            return redirect('login:private_view')
        else:
            request.session['failed'] = True
            return redirect('login:login_view')

    return redirect('login:login_view')


def private_view(request):
    """Private Page Only an Authorized User Can View
    Parameters
    ---------
      request: (HttpRequest) - should contain an authorized user
    Returns
    --------
      out: (HttpResponse) - if user is authenticated, will render private.djhtml
    """
    if request.user.is_authenticated:
        context = { 'user' : request.user }
        return render(request,'private.djhtml',context)

    request.session['failed'] = True
    return redirect('login:login_view')
