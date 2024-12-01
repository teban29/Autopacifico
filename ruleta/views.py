from django.shortcuts import render, redirect
from django.views import View
from .forms import ClienteForm
from .models import Cliente, Premio, Ganador
from .utils import seleccionar_premio
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

class RegistroClienteView(View):
    def get(self, request):
        form = ClienteForm()
        return render(request, 'ruleta/registro_cliente.html', {'form': form})

    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('jugar_ruleta')  # Redirigir a la página de la ruleta
        return render(request, 'ruleta/registro_cliente.html', {'form': form})

@login_required
def jugar_ruleta(request):
    if request.method == 'POST':
        # Obtener premios activos
        premios = Premio.objects.filter(estado=True).values('nombre', 'probabilidad', 'estado')
        resultado = seleccionar_premio(premios)

        # Registrar ganador si no es "Sin premio"
        if resultado != "Sin premio":
            Ganador.objects.create(
                cliente=request.user.cliente,
                premio=Premio.objects.get(nombre=resultado),
                fecha=now()
            )

        return render(request, 'ruleta/resultado.html', {'resultado': resultado})
    return render(request, 'ruleta/jugar.html')

@csrf_exempt
def guardar_resultado(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            premio_nombre = data.get("premio")

            # Si el premio no es "Gracias por participar", registrarlo
            if premio_nombre != "Gracias por participar":
                # Busca el cliente relacionado con el usuario autenticado
                cliente = Cliente.objects.get(user=request.user)
                premio = Premio.objects.get(nombre=premio_nombre)

                # Crear registro en la tabla Ganador
                Ganador.objects.create(
                    cliente=cliente,
                    premio=premio
                )
                return JsonResponse({"status": "success", "message": f"Premio registrado: {premio_nombre}"})
            else:
                return JsonResponse({"status": "info", "message": "Sin premio, no se registra nada."})
        except Cliente.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Cliente no encontrado."}, status=404)
        except Premio.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Premio no encontrado."}, status=404)
        except Exception as e:
            print(f"Error: {str(e)}")  # Log temporal
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

