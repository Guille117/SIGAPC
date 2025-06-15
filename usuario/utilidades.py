from django.http import JsonResponse
from functools import wraps
from usuario.models import Usuario

def rol_requerido(*roles_permitidos):
    def decorador(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            usuario_id = request.session.get('usuario_id')

            if not usuario_id:
                return JsonResponse({'error': 'No autenticado'}, status=401)

            try:
                usuario = Usuario.objects.select_related('rol').get(id=usuario_id)

                if usuario.rol and usuario.rol.nombre_rol in roles_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    return JsonResponse({'error': 'Acceso denegado'}, status=403)

            except Usuario.DoesNotExist:
                return JsonResponse({'error': 'Usuario inválido'}, status=403)

        return _wrapped_view
    return decorador
