from django.urls import path

from .views import HelloView,IndexPageView,GoToIndexView
from django.views.generic.base import RedirectView

urlpatterns = [
    path('hello/<slug:name>/', HelloView.as_view(), name="hello-view"),
    path('index/<slug:name>/', IndexPageView.as_view(), name="index-view"),
    path('redirect/<slug:name>/', GoToIndexView.as_view(), name='redirect-view'),
    path('go-to-google/',RedirectView.as_view(url="https://google.ca"),name="go-to-google-view"),
]
