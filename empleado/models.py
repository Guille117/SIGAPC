from django.db import models

class Persona(models.Model):
    idPersona = models.AutoField(primary_key=True)
    primerNombre = models.CharField(max_length=30)
    segundoNombre = models.CharField(max_length=30)
    tercerNombre = models.CharField(max_length=30)
    primerApellido = models.CharField(max_length=30)
    segundoApellido = models.CharField(max_length=30)
    telefono = models.CharField(max_length=10)
    correo = models.EmailField()
    CUI = models.CharField(max_length=13)
    fechaNac = models.DateField()
    fechaRegistro = models.DateTimeField(auto_now_add=True)

class Departamento(models.Model):
    idDepartamento = models.AutoField(primary_key=True)
    nombreDepa = models.CharField(max_length=100)
    descripcion = models.TextField()
    jefeDepartamento = models.ForeignKey('Empleado', on_delete=models.SET_NULL, null=True, blank=True, related_name='departamentos_dirigidos')
    telefono = models.CharField(max_length=10)


class Empleado(models.Model):
    idEmpleado = models.AutoField(primary_key=True)
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE)
    puesto = models.CharField(max_length=100)
    fechaContratacion = models.DateField()
    salarioBase = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=15,choices=[
            ('Activo', 'Activo'),
            ('Inactivo', 'Inactivo'),
            ('Suspendido', 'Suspendido'),
            ('Vacaciones', 'Vacaciones')
        ],
        default='Activo'
    )