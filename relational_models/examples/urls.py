from django.urls import path
from . import views

urlpatterns = [
    path('', views.template_view, name="template_view"),
]
