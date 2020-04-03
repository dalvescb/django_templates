from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages

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
    """Serves lagin.djhtml from /e/macid/login/ (url name: login_view)
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

def logout_view(request):
    """Redirects to login_view from /e/macid/logout/ (url name: logout_view)
    Parameters
    ----------
      request: (HttpRequest) - expected to be an empty get request
    Returns
    -------
      out: (HttpResponse) - perform User logout and redirects to login_view
    """
    logout(request)
    return redirect('login:login_view')

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

def signup_template_view(request):
    """Serves signup.djhtml from /e/macid/signup (url name: signup_view)
    Parameters
	----------
	  request : (HttpRequest) - expected to be an empty get request
	Returns
	-------
	  out : (HttpRepsonse) - renders signup.djhtml
    """
    form = UserCreationForm()
    failed = request.session.get('create_failed',False)
    context = { 'create_form' : form
                ,'create_failed' : failed }

    return render(request,'signup.djhtml',context)

def user_create_view(request):
    """Creates a new User
    Parameters
	----------
	  request : (HttpRequest) - expects POST data from create_form
	Returns
	-------
	  out : (HttpRepsonse) - if user is successfully created, will login and redirect to private.djhtml
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('login:private_view')

    request.session['create_failed'] = True
    return redirect('login:signup_view')

def password_change_view(request):
    if not request.user.is_authenticated:
        redirect('login:login_view')

    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('login:login_view')
    else:
        form = PasswordChangeForm(request.user)
    context = { 'user' : request.user
                ,'change_form' : form }
    return render(request, 'change.djhtml',context)
