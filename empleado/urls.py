from django.urls import path
from . import views

urlpatterns = [
    path('crearEmp/', views.crearEmpleado, name = 'crearEmpleado'),
    path('verEmps/', views.listarEmpleados, name = 'verEmpleados'),
    path('actualizarEmp/', views.actualizarEmpleado, name='actualizarEmpleado'),
    path('eliminarEmp/<int:id>/', views.eliminarEmpleado, name='elimianrEmpleado'),
    path('estadoEmp/', views.cambiarEstadoEmpleado, name='cambiarEsado'),
    path('departamentoEmps/', views.listarEmpleadosDepartamento, name='empleadosPorDepartemento'),
    path('verEmp/<int:id>/', views.obtenerEmpleado, name='verEmpleado'),
]