from django.urls import path
from . import views

urlpatterns=[
    path('crear/', views.crearUsuario, name='crearUsuario'),
    path('mostrar/', views.listarUsuarios, name='mostrarUsuarios'),
    path('verUsu/<int:id>/', views.obtenerUsuario, name='mostrarUsuario'),
    path('modificar/', views.modificarUsuario, name='modificarUsuario'),
    path('eliminar/<int:id>/', views.eliminarUsuario, name='eliminarUsuario'),
    path('mostrarPorRol/', views.usuariosRol, name='usuariosRol'),
    path('usuario/', views.usu, name="ususu"),
    path('methLogin/', views.loginUsuario, name="metodoLogin" )
]