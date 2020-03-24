from django.urls import path
from . import views

urlpatterns = [
    path('template_test/',views.template_view,name="template-view"),
    ]
