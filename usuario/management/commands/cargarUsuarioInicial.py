from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from usuario.models import Usuario, Rol
from empleado.models import Empleado

class Command(BaseCommand):
    help = 'Crea un usuario inicial con acceso total'

    def handle(self, *args, **kwargs):
        try:
            empleado = Empleado.objects.get(idEmpleado=1)  
        except Empleado.DoesNotExist:
            self.stdout.write(self.style.ERROR("Empleado con ID 1 no existe."))
            return

        rol_admin = Rol.objects.get(id=1)  

        usuario, creado = Usuario.objects.get_or_create(
            empleado=empleado,
            defaults={
                "nikname": "sigapuser",
                "contrasenia": make_password("siga12345"),
                "rol": rol_admin
            }
        )

        if creado:
            self.stdout.write(self.style.SUCCESS(f"Usuario '{usuario.nikname}' creado con éxito."))
        else:
            self.stdout.write(self.style.WARNING(f"El usuario ya existe: {usuario.nikname}"))
