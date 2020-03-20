from django.urls import path, re_path
from . import views

app_name = 'done'

urlpatterns = [
    path('names/jimmy/', views.jimmy_view),
     # special case name
    path('names/<str:name>/', views.name_view),
     # handles any non-empty string name
    path('names/<str:name>/<int:age>/',views.name_age_view),
     # handles any int for an age with a name
    re_path(r'^names2/(?P<name>[a-z]+)/(?P<age>[0-9]{2})/$',views.regex_view),
     # same as above but uses regex to constrain age to two digits

    path('index/',views.index_view),
    path('hello/',views.hello_view,name='hello'),
    path('goodbye/<int:count>/',views.goodbye_view,name='goodbye'),
    path('reverse/',views.reverse_view,name='reverse'),
      # used with the index.djhtml template

    path('unfound/<int:x>/',views.unfound_view),
]
