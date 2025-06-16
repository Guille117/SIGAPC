
from django.core.management.base import BaseCommand
from empleado.models import Departamento, Persona, Empleado
from faker import Faker
from random import randint, choice
from datetime import date
import random

class Command(BaseCommand):
    help = 'Carga departamentos y 25 empleados con datos realistas'

    def handle(self, *args, **kwargs):
        fake = Faker(locale='es_MX') 

        departamentos_data = [
            {"nombreDepa": "Recursos Humanos", "descripcion": "Maneja el personal", "telefono": fake.msisdn()[:10]},
            {"nombreDepa": "Finanzas", "descripcion": "Administra finanzas", "telefono": fake.msisdn()[:10]},
            {"nombreDepa": "TI", "descripcion": "Tecnología e infraestructura", "telefono": fake.msisdn()[:10]},
            {"nombreDepa": "Logística", "descripcion": "Distribución y transporte", "telefono": fake.msisdn()[:10]},
            {"nombreDepa": "Atención al Cliente", "descripcion": "Soporte al cliente", "telefono": fake.msisdn()[:10]},
        ]

        departamentos = []
        for data in departamentos_data:
            depto, created = Departamento.objects.get_or_create(
                nombreDepa=data["nombreDepa"],
                defaults=data
            )
            departamentos.append(depto)
            msg = "creado" if created else "existía"
            self.stdout.write(self.style.SUCCESS(f"Departamento '{depto.nombreDepa}' {msg}."))

        for _ in range(25):
            nombre = fake.first_name()
            segundo = fake.first_name()
            apellido = fake.last_name()
            segundo_ap = fake.last_name()
            telefono = fake.msisdn()[:10]
            correo = fake.email()
            cui = str(fake.random_number(digits=13, fix_len=True))
            fecha_nac = fake.date_of_birth(minimum_age=20, maximum_age=60)

            persona = Persona.objects.create(
                primerNombre=nombre,
                segundoNombre=segundo,
                tercerNombre='',
                primerApellido=apellido,
                segundoApellido=segundo_ap,
                telefono=telefono,
                correo=correo,
                CUI=cui,
                fechaNac=fecha_nac
            )

            Empleado.objects.create(
                persona=persona,
                departamento=choice(departamentos),
                puesto=fake.job(),
                fechaContratacion=fake.date_between(start_date='-2y', end_date='today'),
                salarioBase = round(random.uniform(3000, 7000), 2)
            )

        self.stdout.write(self.style.SUCCESS("25 empleados con datos realistas creados correctamente."))
