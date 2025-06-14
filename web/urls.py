from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('nosotros/', views.nosotros, name='noso'),
    path('contacto/', views.contacto, name="contac"),
    path('servicios/', views.serv, name="servs"),
    path('ubicacion/', views.ubi, name='ubica'),
]