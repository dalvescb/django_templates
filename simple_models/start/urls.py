from django.urls import path
from . import views

urlpatterns = [
    path('first_person/',views.first_person_view,name="first_person"),
]
