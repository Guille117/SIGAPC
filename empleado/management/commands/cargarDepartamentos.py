from django.core.management.base import BaseCommand
from empleado.models import Departamento

class Command(BaseCommand):
    help = 'Carga departamentos iniciales sin jefe de departamento'

    def handle(self, *args, **kwargs):
        datos = [
            {"nombreDepa": "Recursos Humanos", "descripcion": "Maneja el personal de la empresa", "telefono": "12345678"},
            {"nombreDepa": "Finanzas", "descripcion": "Administra los recursos financieros", "telefono": "33445566"},
            {"nombreDepa": "TI", "descripcion": "Tecnologías de la información", "telefono": "44556677"},
            {"nombreDepa": "Logística", "descripcion": "Manejo de transporte y distribución", "telefono": "44556677"},
            {"nombreDepa": "Atención al Cliente", "descripcion": "Soporte y contacto con clientes", "telefono": "55667788"},
        ]

        for depa in datos:
            departamento, creado = Departamento.objects.get_or_create(nombreDepa=depa["nombreDepa"], defaults=depa)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Departamento '{departamento.nombreDepa}' creado."))
            else:
                self.stdout.write(self.style.WARNING(f"Departamento '{departamento.nombreDepa}' ya existía."))
