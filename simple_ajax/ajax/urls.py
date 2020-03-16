from django.urls import path
from . import views

urlpatterns = [
    path('test_template/', views.test_template_view),
    path('test_ajax/', views.test_ajax_view),
]
