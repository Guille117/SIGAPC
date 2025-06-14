from django.db import models
from empleado.models import Empleado  

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True,)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_rol


class Permiso(models.Model):
    codigo_permiso = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    modulo = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.codigo_permiso


# relación de muchos a muchos entre rol y permisos
class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')

    def __str__(self):
        return f"{self.rol} -> {self.permiso}"
    

class Usuario(models.Model):
    empleado = models.OneToOneField(Empleado, to_field="idEmpleado", on_delete=models.CASCADE)
    nikname = models.CharField(max_length=20, unique=True)
    contrasenia = models.CharField(max_length=128)
    activo = models.BooleanField(default=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    ultimo_ingreso = models.DateTimeField(null=True, blank=True)
    intentos_fallidos = models.IntegerField(default=0)

    def __str__(self):
        return self.nikname
    

# relación de muchos a muchos entre empleados y roles
class UsuarioRol(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        unique_together = ('usuario', 'rol')

    def __str__(self):
        return f"{self.usuario} -> {self.rol}"

