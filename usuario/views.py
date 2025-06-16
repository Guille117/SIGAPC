import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from usuario.models import Usuario, Rol
from empleado.models import Empleado
from django.db.models import F, Value
from django.db.models.functions import Concat
from usuario.utilidades import rol_requerido


def usu(request):
    return render(request, 'Usuario1.html')


@csrf_exempt
@require_http_methods(["POST"])
@rol_requerido("Administrador")
def crearUsuario(request):
    try:
        data = json.loads(request.body)
        empleado = Empleado.objects.get(idEmpleado=data["idEmpleado"])

        if Usuario.objects.filter(nikname=data["nikname"]).exists():
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)

        rol = Rol.objects.get(id=data["idRol"])

        usuario = Usuario.objects.create(
            empleado=empleado,
            nikname=data["nikname"],
            contrasenia=make_password(data["contrasenia"]),
            activo=True
        )
        usuario.rol = rol
        usuario.save()

        return JsonResponse({"mensaje": "Usuario creado correctamente", "idUsuario": usuario.id}, status=201)

    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
    except Rol.DoesNotExist:
        return JsonResponse({"error": "Rol no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def listarUsuarios(request):
    usuarios = Usuario.objects.select_related("empleado", "rol").all()
    datos = []
    for u in usuarios:
        datos.append({
            "idUsuario": u.id,
            "nikname": u.nikname,
            "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
            "activo": u.activo,
            "mail": u.empleado.persona.correo,
            "rol": u.rol.nombre_rol if u.rol else "Sin rol"
        })
    return JsonResponse({"usuarios": datos}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def obtenerUsuario(request, id):
    try:
        usuario = Usuario.objects.select_related("empleado", "rol").get(id=id)
        data = {
            "idUsuario": usuario.id,
            "nikname": usuario.nikname,
            "activo": usuario.activo,
            "empleado": {
                "idEmpleado": usuario.empleado.idEmpleado,
                "nombreCompleto": f"{usuario.empleado.persona.primerNombre} {usuario.empleado.persona.primerApellido}"
            },
            "rol": usuario.rol.nombre_rol if usuario.rol else "Sin rol"
        }
        return JsonResponse(data, status=200)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


@csrf_exempt
@require_http_methods(["DELETE"])
def eliminarUsuario(request, id):
    try:
        usuario = Usuario.objects.get(id=id)
        usuario.activo = False
        usuario.save()
        return JsonResponse({"mensaje": "Usuario desactivado correctamente"}, status=200)
    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def usuariosRol(request):
    try:
        data = json.loads(request.body)
        idRol = data.get("idRol")

        if not idRol:
            return JsonResponse({"error": "Debe proporcionar el idRol"}, status=400)

        usuarios = Usuario.objects.filter(rol_id=idRol, activo=True).select_related("empleado", "rol")

        datos = []
        for u in usuarios:
            datos.append({
                "idUsuario": u.id,
                "nikname": u.nikname,
                "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
                "activo": u.activo,
                "mail": u.empleado.persona.correo,
                "rol": u.rol.nombre_rol if u.rol else "Sin rol"
            })

        return JsonResponse({"usuarios": datos}, status=200)

    except Rol.DoesNotExist:
        return JsonResponse({"error": "Rol no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def loginUsuario(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        usuario = Usuario.objects.get(nikname=username)

        if not usuario.activo:
            return JsonResponse({"success": False, "error": "Usuario inhabilitado"}, status=403)

        if check_password(password, usuario.contrasenia):
            request.session['usuario_id'] = usuario.id 
            return JsonResponse({"success": True, "message": "Login exitoso"})
        else:
            return JsonResponse({"success": False, "error": "Contraseña incorrecta"}, status=401)

    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)


@csrf_exempt  
@require_http_methods(["POST"])
@rol_requerido("Administrador", "RRHH")
def cambiarEstado(request):
    try:
        data = json.loads(request.body)
        id_usuario = data.get("idUsuario")

        if id_usuario is None:
            return JsonResponse({"success": False, "error": "Falta el ID del usuario"}, status=400)

        usuario = Usuario.objects.filter(id=id_usuario).first()

        if usuario is None:
            return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)

        usuario.activo = not usuario.activo
        usuario.save()

        return JsonResponse({
            "success": True,
            "nuevoEstado": usuario.activo,
            "mensaje": "Usuario activado" if usuario.activo else "Usuario desactivado"
        })

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)


@csrf_exempt
@require_http_methods(["POST"])
@rol_requerido("Administrador")
def cambiarContra(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        actual = data.get("contraseniaActual")
        nueva = data.get("nuevaContrasenia")
        confirmar = data.get("confirmarContrasenia")

        if not all([username, actual, nueva, confirmar]):
            return JsonResponse({"success": False, "error": "Faltan datos"}, status=400)

        if nueva != confirmar:
            return JsonResponse({"success": False, "error": "Las contraseñas no coinciden"}, status=400)

        usuario = Usuario.objects.get(nikname=username)

        if not check_password(actual, usuario.contrasenia):
            return JsonResponse({"success": False, "error": "La contraseña actual no es válida"}, status=403)

        usuario.contrasenia = make_password(nueva)
        usuario.save()

        return JsonResponse({"success": True, "mensaje": "Contraseña actualizada correctamente"})

    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)


def listarRoles(request):
    roles = Rol.objects.all()
    data = [{"id": rol.id, "nombre": rol.nombre_rol} for rol in roles]
    return JsonResponse({"roles": data})

def listarEmpleados(request):
    empleados = Empleado.objects.annotate(
        nombre=Concat(F('persona__primerNombre'), Value(' '), F('persona__primerApellido'))
    ).exclude(idEmpleado__in=Usuario.objects.values_list('empleado_id', flat=True)) \
     .values('idEmpleado', 'nombre')

    return JsonResponse({"empleados": list(empleados)})




@csrf_exempt
@require_http_methods(["POST"])
@rol_requerido("Administrador", "RRHH")
def modificarUsuario(request):
    try:
        data = json.loads(request.body)
        id_usuario = int(data.get("idUsuario"))
        nikname = data.get("nikname")
        id_rol = int(data.get("idRol"))

        if not all([id_usuario, nikname, id_rol]):
            return JsonResponse({"success": False, "error": "Faltan datos"}, status=400)

        if Usuario.objects.exclude(pk=id_usuario).filter(nikname=nikname).exists():
            return JsonResponse({"success": False, "error": "El nombre de usuario ya está en uso"}, status=400)

        usuario = Usuario.objects.get(pk=id_usuario)
        usuario.nikname = nikname
        usuario.rol_id = id_rol
        usuario.save()

        return JsonResponse({"success": True, "mensaje": "Usuario actualizado correctamente"})

    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
@rol_requerido("Administrador", "RRHH")
def usuariosInactivos(request):
    usuarios = Usuario.objects.select_related("empleado", "rol").filter(activo=False)
    datos = []
    for u in usuarios:
        datos.append({
            "idUsuario": u.id,
            "nikname": u.nikname,
            "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
            "activo": u.activo,
            "mail": u.empleado.persona.correo,
            "rol": u.rol.nombre_rol if u.rol else "Sin rol"
        })
    return JsonResponse({"usuarios": datos}, status=200)


@csrf_exempt
@require_http_methods(["POST"])
def buscarUsuario(request):
    try:
        usuarioEntrada = json.loads(request.body).get('nikname', '').strip()

        if not usuarioEntrada:
            return JsonResponse({'error': 'Usuario requerido'}, status=400)

        u = Usuario.objects.select_related('empleado__persona', 'rol').filter(nikname__iexact=usuarioEntrada).first()

        if not u:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

        return JsonResponse({
            "idUsuario": u.id,
            "nikname": u.nikname,
            "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
            "activo": u.activo,
            "mail": u.empleado.persona.correo,
            "rol": u.rol.nombre_rol if u.rol else "Sin rol"
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    

'''
@csrf_exempt  
@require_http_methods(["POST"])
def loginUsuario(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login exitoso"})
        else:
            return JsonResponse({"success": False, "error": "Credenciales inválidas"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)
    
'''
