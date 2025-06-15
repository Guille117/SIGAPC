import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from usuario.models import Usuario, UsuarioRol, Rol
from empleado.models import Empleado
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password, make_password

def usu(request):
    return render(request, 'Usuario1.html')

from django.contrib.auth.models import User

@csrf_exempt
@require_http_methods(["POST"])
def crearUsuario(request):
    try:
        data = json.loads(request.body)
        empleado = Empleado.objects.get(idEmpleado=data["idEmpleado"])

        if User.objects.filter(username=data["nikname"]).exists():
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)

        user = User.objects.create_user(
            username=data["nikname"],
            password=data["contrasenia"]
        )

        # Relaciona tu modelo Usuario si lo usás adicionalmente
        usuario = Usuario.objects.create(
            empleado=empleado,
            nikname=user.username,
            contrasenia=user.password  # o simplemente user
        )

        rol = Rol.objects.get(id=data["idRol"])
        UsuarioRol.objects.create(usuario=usuario, rol=rol)

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
    usuarios = Usuario.objects.select_related("empleado").all()
    datos = []
    for u in usuarios:
        rol = UsuarioRol.objects.filter(usuario=u, activo=True).first()
        datos.append({
            "idUsuario": u.id,
            "nikname": u.nikname,
            "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
            "activo": u.activo,
            "mail":u.empleado.persona.correo,
            "rol": rol.rol.nombre_rol if rol else "Sin rol"
        })
    return JsonResponse({"usuarios": datos}, status=200)


@csrf_exempt
@require_http_methods(["GET"])
def obtenerUsuario(request, id):
    try:
        usuario = Usuario.objects.select_related("empleado").get(id=id)
        rol = UsuarioRol.objects.filter(usuario=usuario, activo=True).first()
        data = {
            "idUsuario": usuario.id,
            "nikname": usuario.nikname,
            "activo": usuario.activo,
            "empleado": {
                "idEmpleado": usuario.empleado.idEmpleado,
                "nombreCompleto": f"{usuario.empleado.persona.primerNombre} {usuario.empleado.persona.primerApellido}"
            },
            "rol": rol.rol.nombre_rol if rol else "Sin rol"
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

        rol = Rol.objects.get(id=idRol)

        # Filtrar relaciones activas de ese rol
        relaciones = UsuarioRol.objects.filter(rol=rol, activo=True).select_related("usuario__empleado__persona", "rol")

        datos = []
        for rel in relaciones:
            usuario = rel.usuario
            datos.append({
                "idUsuario": usuario.id,
                "nikname": usuario.nikname,
                "empleado": f"{usuario.empleado.persona.primerNombre} {usuario.empleado.persona.primerApellido}",
                "activo": usuario.activo,
                "mail": usuario.empleado.persona.correo,
                "rol": rel.rol.nombre_rol
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

        # Buscar directamente en tu modelo personalizado
        usuario = Usuario.objects.get(nikname=username)

        if check_password(password, usuario.contrasenia):
            # Aquí puedes guardar en sesión si deseas
            return JsonResponse({"success": True, "message": "Login exitoso"})
        else:
            return JsonResponse({"success": False, "error": "Contraseña incorrecta"}, status=401)

    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)



@csrf_exempt  
@require_http_methods(["POST"])
def cambiarEstado(request):
    try:
        data = json.loads(request.body)
        id_usuario = data.get("idUsuario")

        if id_usuario is None:
            return JsonResponse({"success": False, "error": "Falta el ID del usuario"}, status=400)

        usuario = Usuario.objects.filter(id=id_usuario).first()

        if usuario is None:
            return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)

        usuario.activo = not usuario.activo  # invierte el estado
        usuario.save()

        return JsonResponse({
            "success": True,
            "nuevoEstado": usuario.activo,
            "mensaje": "Usuario activado" if usuario.activo else "Usuario desactivado"
        })

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)

from django.contrib.auth.hashers import check_password, make_password
from .models import Usuario  # Asegúrate de importar tu modelo correcto

@csrf_exempt
@require_http_methods(["POST"])
def cambiarContra(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")  # Este debe ser tu "nikname"
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

@csrf_exempt
@require_http_methods(["POST"])
def modificarUsuario(request):
    try:
        data = json.loads(request.body)
        id_usuario = int(data.get("idUsuario"))
        nikname = data.get("nikname")
        id_rol = int(data.get("idRol"))

        print("Datos recibidos:", data)
        print("idUsuario:", id_usuario, "nikname:", nikname, "idRol:", id_rol)

        if not all([id_usuario, nikname, id_rol]):
            return JsonResponse({"success": False, "error": "Faltan datos"}, status=400)

        # Validar si el nikname ya está en uso por otro usuario
        if Usuario.objects.exclude(pk=id_usuario).filter(nikname=nikname).exists():
            return JsonResponse({"success": False, "error": "El nombre de usuario ya está en uso"}, status=400)

        usuario = Usuario.objects.get(pk=id_usuario)

        # Actualizar el nombre de usuario
        usuario.nikname = nikname
        usuario.save()

        # Desactivar todos los roles anteriores
        UsuarioRol.objects.filter(usuario=usuario).update(activo=False)

        # Reactivar o crear nuevo rol
        usuario_rol, created = UsuarioRol.objects.get_or_create(usuario=usuario, rol_id=id_rol)
        usuario_rol.activo = True
        usuario_rol.save()

        return JsonResponse({"success": True, "mensaje": "Usuario actualizado correctamente"})

    except Usuario.DoesNotExist:
        return JsonResponse({"success": False, "error": "Usuario no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def usuariosInactivos(request):
    usuarios = Usuario.objects.select_related("empleado").filter(activo=False)
    datos = []
    for u in usuarios:
        rol = UsuarioRol.objects.filter(usuario=u, activo=True).first()
        datos.append({
            "idUsuario": u.id,
            "nikname": u.nikname,
            "empleado": f"{u.empleado.persona.primerNombre} {u.empleado.persona.primerApellido}",
            "activo": u.activo,
            "mail": u.empleado.persona.correo,
            "rol": rol.rol.nombre_rol if rol else "Sin rol"
        })
    return JsonResponse({"usuarios": datos}, status=200)


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
