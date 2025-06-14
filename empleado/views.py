import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import Empleado, Persona, Departamento
from django.core.exceptions import ObjectDoesNotExist

@csrf_exempt
@require_http_methods(["POST"])
def crearEmpleado(request):
    try:
        data = json.loads(request.body)

        # Crear Persona
        persona = Persona.objects.create(
            primerNombre=data["primerNombre"],
            segundoNombre=data["segundoNombre"],
            tercerNombre=data["tercerNombre"],
            primerApellido=data["primerApellido"],
            segundoApellido=data["segundoApellido"],
            telefono=data["telefono"],
            correo=data["correo"],
            CUI=data["CUI"],
            fechaNac=data["fechaNac"]
        )

        # Crear Empleado
        departamento = Departamento.objects.get(idDepartamento=data["departamentoId"])

        empleado = Empleado.objects.create(
            persona=persona,
            departamento=departamento,
            puesto=data["puesto"],
            fechaContratacion=data["fechaContratacion"],
            salarioBase=data["salarioBase"]
        )

        return JsonResponse({"mensaje": "Empleado creado correctamente", "idEmpleado": empleado.idEmpleado}, status=201)

    except KeyError as e:
        return JsonResponse({"error": f"Campo faltante: {str(e)}"}, status=400)
    except Departamento.DoesNotExist:
        return JsonResponse({"error": "Departamento no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def listarEmpleados(request):
    empleados = Empleado.objects.select_related("persona", "departamento").all()
    datos = []
    for emp in empleados:
        datos.append({
            "idEmpleado": emp.idEmpleado,
            "nombreCompleto": f"{emp.persona.primerNombre} {emp.persona.primerApellido}",
            "departamento": emp.departamento.nombreDepa,
            "puesto": emp.puesto,
            "estado": emp.estado,
        })
    return JsonResponse({"empleados": datos}, status=200)

@csrf_exempt
@require_http_methods(["PUT"])
def actualizarEmpleado(request, id):
    try:
        data = json.loads(request.body)
        empleado = Empleado.objects.select_related("persona").get(idEmpleado=id)

        # Actualizar Persona
        p = empleado.persona
        p.primerNombre = data["primerNombre"]
        p.segundoNombre = data["segundoNombre"]
        p.tercerNombre = data["tercerNombre"]
        p.primerApellido = data["primerApellido"]
        p.segundoApellido = data["segundoApellido"]
        p.telefono = data["telefono"]
        p.correo = data["correo"]
        p.CUI = data["CUI"]
        p.fechaNac = data["fechaNac"]
        p.save()

        # Actualizar Empleado
        empleado.puesto = data["puesto"]
        empleado.fechaContratacion = data["fechaContratacion"]
        empleado.salarioBase = data["salarioBase"]
        if "departamentoId" in data:
            empleado.departamento = Departamento.objects.get(idDepartamento=data["departamentoId"])
        empleado.save()

        return JsonResponse({"mensaje": "Empleado actualizado correctamente"}, status=200)

    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
    except Departamento.DoesNotExist:
        return JsonResponse({"error": "Departamento no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["DELETE"])
def eliminarEmpleado(request, id):
    try:
        empleado = Empleado.objects.get(idEmpleado=id)
        empleado.estado = "Inactivo"
        empleado.save()
        return JsonResponse({"mensaje": "Empleado desactivado (eliminación lógica)"}, status=200)
    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)

@csrf_exempt
@require_http_methods(["PATCH"])
def cambiarEstadoEmpleado(request, id):
    try:
        data = json.loads(request.body)
        nuevo_estado = data.get("estado")
        if nuevo_estado not in ['Activo', 'Inactivo', 'Suspendido', 'Vacaciones']:
            return JsonResponse({"error": "Estado inválido"}, status=400)

        empleado = Empleado.objects.get(idEmpleado=id)
        empleado.estado = nuevo_estado
        empleado.save()
        return JsonResponse({"mensaje": f"Estado cambiado a {nuevo_estado}"}, status=200)

    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def listarEmpleadosDepartamento(request):
    try:
        data = json.loads(request.body)
        departamento_id = data.get("idDepartamento")

        if not departamento_id:
            return JsonResponse({"error": "Debe proporcionar el idDepartamento"}, status=400)

        try:
            departamento = Departamento.objects.get(idDepartamento=departamento_id)
        except Departamento.DoesNotExist:
            return JsonResponse({"error": "Departamento no encontrado"}, status=404)

        empleados = Empleado.objects.filter(departamento=departamento).select_related("persona")
        lista = []

        for emp in empleados:
            lista.append({
                "idEmpleado": emp.idEmpleado,
                "nombreCompleto": f"{emp.persona.primerNombre} {emp.persona.primerApellido}",
                "puesto": emp.puesto,
                "estado": emp.estado
            })

        return JsonResponse({"departamento": departamento.nombreDepa, "empleados": lista}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def obtenerEmpleado(request, id):
    try:
        empleado = Empleado.objects.select_related("persona", "departamento").get(idEmpleado=id)

        datos = {
            "idEmpleado": empleado.idEmpleado,
            "puesto": empleado.puesto,
            "fechaContratacion": empleado.fechaContratacion,
            "salarioBase": float(empleado.salarioBase),
            "estado": empleado.estado,
            "departamento": {
                "id": empleado.departamento.idDepartamento,
                "nombre": empleado.departamento.nombreDepa
            },
            "persona": {
                "idPersona": empleado.persona.idPersona,
                "primerNombre": empleado.persona.primerNombre,
                "segundoNombre": empleado.persona.segundoNombre,
                "tercerNombre": empleado.persona.tercerNombre,
                "primerApellido": empleado.persona.primerApellido,
                "segundoApellido": empleado.persona.segundoApellido,
                "telefono": empleado.persona.telefono,
                "correo": empleado.persona.correo,
                "CUI": empleado.persona.CUI,
                "fechaNac": empleado.persona.fechaNac,
                "fechaRegistro": empleado.persona.fechaRegistro,
            }
        }

        return JsonResponse(datos, status=200)

    except Empleado.DoesNotExist:
        return JsonResponse({"error": "Empleado no encontrado"}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)