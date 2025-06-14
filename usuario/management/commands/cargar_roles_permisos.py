from django.core.management.base import BaseCommand
from usuario.models import Rol, Permiso, RolPermiso 

class Command(BaseCommand):
    help = 'Carga roles, permisos y asignaciones iniciales entre ellos'

    def handle(self, *args, **kwargs):
        # 1. Crear Roles
        roles = [
            {"nombre_rol": "Administrador", "descripcion": "Acceso completo al sistema"},
            {"nombre_rol": "Recepcionista", "descripcion": "Gestión de visitantes y llamadas"},
            {"nombre_rol": "Supervisor", "descripcion": "Monitoreo y reportes"},
            {"nombre_rol": "RRHH", "descripcion": "Gestión de empleados y departamentos"},
            {"nombre_rol": "Invitado", "descripcion": "Acceso de solo lectura"}
        ]

        for r in roles:
            obj, creado = Rol.objects.get_or_create(nombre_rol=r["nombre_rol"], defaults=r)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Rol creado: {obj.nombre_rol}"))
            else:
                self.stdout.write(self.style.WARNING(f"Rol ya existe: {obj.nombre_rol}"))

        # 2. Crear Permisos
        permisos = [
            {"codigo_permiso": "usuario_crear", "descripcion": "Permite crear nuevos usuarios", "modulo": "Seguridad"},
            {"codigo_permiso": "usuario_editar", "descripcion": "Permite editar información de usuarios", "modulo": "Seguridad"},
            {"codigo_permiso": "empleado_ver", "descripcion": "Permite ver información de empleados", "modulo": "Recursos Humanos"},
            {"codigo_permiso": "empleado_editar", "descripcion": "Permite editar empleados", "modulo": "Recursos Humanos"},
            {"codigo_permiso": "departamento_ver", "descripcion": "Permite visualizar departamentos", "modulo": "Administración"},
            {"codigo_permiso": "rol_asignar", "descripcion": "Permite asignar roles a usuarios", "modulo": "Seguridad"},
        ]

        for p in permisos:
            obj, creado = Permiso.objects.get_or_create(codigo_permiso=p["codigo_permiso"], defaults=p)
            if creado:
                self.stdout.write(self.style.SUCCESS(f"Permiso creado: {obj.codigo_permiso}"))
            else:
                self.stdout.write(self.style.WARNING(f"Permiso ya existe: {obj.codigo_permiso}"))

        # 3. Asignaciones Rol y Permiso
        asignaciones = {
            "Administrador": ["usuario_crear", "usuario_editar", "empleado_ver", "empleado_editar", "departamento_ver", "rol_asignar"],
            "Recepcionista": ["empleado_ver", "departamento_ver"],
            "Supervisor": ["empleado_ver", "departamento_ver"],
            "RRHH": ["empleado_ver", "empleado_editar", "departamento_ver"],
            "Invitado": ["empleado_ver"]
        }

        for nombre_rol, codigos_permisos in asignaciones.items():
            try:
                rol = Rol.objects.get(nombre_rol=nombre_rol)
                for cod_permiso in codigos_permisos:
                    try:
                        permiso = Permiso.objects.get(codigo_permiso=cod_permiso)
                        obj, creado = RolPermiso.objects.get_or_create(rol=rol, permiso=permiso)
                        if creado:
                            self.stdout.write(self.style.SUCCESS(f"Asignado permiso '{cod_permiso}' al rol '{nombre_rol}'"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Asignación ya existe: '{cod_permiso}' → '{nombre_rol}'"))
                    except Permiso.DoesNotExist:
                        self.stdout.write(self.style.ERROR(f"Permiso no encontrado: {cod_permiso}"))
            except Rol.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"Rol no encontrado: {nombre_rol}"))
