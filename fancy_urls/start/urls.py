from django.urls import path
from . import views
urlpatterns = [
    path('names/<str:name>/', views.name_view),
     # handles any non-empty string name
]
