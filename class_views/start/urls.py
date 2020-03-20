from django.urls import path
from .views import HelloView

urlpatterns = [
    path('hello/<slug:name>/', HelloView.as_view(), name="hello-view"),
]
