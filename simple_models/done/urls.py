from django.urls import path

from . import views

urlpatterns = [
    path('first_person/',views.get_person_view,name="first_person"),
    path('create_person/<name>/<age>/',views.create_person_view,name="create_person"),
    path('get_person/<name>/<age>/',views.get_person_view,name="get_person"),
    path('filter_person/<age>/',views.filter_person_view,name="filter_person"),
    path('exclude_person/<age>/',views.exclude_person_view,name="exclude_person"),
]
