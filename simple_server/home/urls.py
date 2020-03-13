from django.urls import path

from . import views

urlpatterns = [
    path('',views.home_view,name='home_view'),
    path('get_test/',views.home_get,name='home_get'),
    path('post_test/',views.home_post,name='home_post'),
]
