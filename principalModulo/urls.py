from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.log, name="loglog"),
    path('home/', views.home, name="inicio"),
]
