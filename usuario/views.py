import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from usuario.models import Usuario, UsuarioRol, Rol
from empleado.models import Empleado
from django.contrib.auth import authenticate, login

def usu(request):
    return render(request, 'Usuario1.html')

@csrf_exempt
@require_http_methods(["POST"])
def crearUsuario(request):
    try:
        data = json.loads(request.body)
        empleado = Empleado.objects.get(idEmpleado=data["idEmpleado"])

        if Usuario.objects.filter(nikname=data["nikname"]).exists():
            return JsonResponse({"error": "El nombre de usuario ya existe"}, status=400)

        usuario = Usuario.objects.create(
            empleado=empleado,
            nikname=data["nikname"],
            contrasenia=make_password(data["contrasenia"])
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
@require_http_methods(["PUT"])
def modificarUsuario(request):
    try:
        data = json.loads(request.body)
        id_usuario = data.get("idUsuario")

        if not id_usuario:
            return JsonResponse({"error": "Debe proporcionar el idUsuario"}, status=400)

        usuario = Usuario.objects.get(id=id_usuario)

        if "nikname" in data:
            usuario.nikname = data["nikname"]
        if "contrasenia" in data:
            usuario.contrasenia = make_password(data["contrasenia"])
        usuario.save()

        if "idRol" in data:
            UsuarioRol.objects.filter(usuario=usuario).update(activo=False)
            nuevo_rol = Rol.objects.get(id=data["idRol"])
            UsuarioRol.objects.get_or_create(usuario=usuario, rol=nuevo_rol, defaults={"activo": True})

        return JsonResponse({"mensaje": "Usuario modificado correctamente"}, status=200)

    except Usuario.DoesNotExist:
        return JsonResponse({"error": "Usuario no encontrado"}, status=404)
    except Rol.DoesNotExist:
        return JsonResponse({"error": "Rol no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
        relaciones = UsuarioRol.objects.filter(rol=rol, activo=True).select_related("usuario")

        datos = []
        for rel in relaciones:
            usuario = rel.usuario
            datos.append({
                "idUsuario": usuario.id,
                "nikname": usuario.nikname,
                "activo": usuario.activo,
                "empleado": f"{usuario.empleado.persona.primerNombre} {usuario.empleado.persona.primerApellido}"
            })

        return JsonResponse({"rol": rol.nombre_rol, "usuarios": datos}, status=200)

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

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "message": "Login exitoso"})
        else:
            return JsonResponse({"success": False, "error": "Credenciales inválidas"}, status=401)

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "error": "JSON inválido"}, status=400)