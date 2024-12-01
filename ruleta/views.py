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
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import user_passes_test


class RegistroClienteView(View):
    def get(self, request):
        form = ClienteForm()
        return render(request, 'ruleta/registro_cliente.html', {'form': form})

    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()  # Guardar el cliente en la base de datos
            # Guardar el ID del cliente en la sesión (opcional)
            request.session['cliente_id'] = cliente.id
            # Redirigir a la página de jugar con el cliente_id
            return redirect('jugar_ruleta', cliente_id=cliente.id)
        return render(request, 'ruleta/registro_cliente.html', {'form': form})



@login_required(login_url='/ruleta/registro/')
def jugar_ruleta(request, cliente_id=None):
    if cliente_id is None:
        messages.error(request, 'Por favor, regístrate para jugar')
        return redirect('registro_cliente')

    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente no válido. Por favor, regístrate.')
        return redirect('registro_cliente')

    # Verificar si el cliente ya tiene un resultado
    resultado = request.session.get('resultado')

    if not resultado and request.method == 'POST':
        premios = Premio.objects.filter(estado=True).values('nombre', 'probabilidad')
        resultado = seleccionar_premio(premios)
        request.session['resultado'] = resultado

        if resultado != "Gracias por participar":
            try:
                premio = Premio.objects.get(nombre=resultado)
                Ganador.objects.create(cliente=cliente, premio=premio)
            except Premio.DoesNotExist:
                pass

    return render(request, 'ruleta/jugar.html', {'cliente': cliente, 'resultado': resultado})






@csrf_exempt
def guardar_resultado(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            premio_nombre = data.get("premio")

            # Verificar si el premio no es "Gracias por participar"
            if premio_nombre == "Gracias por participar":
                return JsonResponse({
                    "status": "info",
                    "message": "Sin premio, no se registra ningún ganador."
                })

            # Verificar si el cliente está en la sesión
            cliente_id = request.session.get('cliente_id')
            if not cliente_id:
                return JsonResponse({"status": "error", "message": "Cliente no autenticado."}, status=403)

            # Buscar el cliente en la base de datos
            try:
                cliente = Cliente.objects.get(id=cliente_id)
            except Cliente.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Cliente no encontrado."}, status=404)

            # Buscar el premio en la base de datos
            try:
                premio = Premio.objects.get(nombre=premio_nombre, estado=True)
            except Premio.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Premio no encontrado."}, status=404)

            # Crear registro en la tabla Ganador
            Ganador.objects.create(
                cliente=cliente,
                premio=premio
            )
            return JsonResponse({"status": "success", "message": f"Premio registrado: {premio_nombre}"})

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Error al procesar el JSON."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)




def redirect_to_admin_login(request):
    return redirect('/admin/login/')

def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

# Dashboard para superusuarios
@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_ganadores = Ganador.objects.count()
    premios_entregados = Ganador.objects.values('premio__nombre').count()
    context = {
        'total_clientes': total_clientes,
        'total_ganadores': total_ganadores,
        'premios_entregados': premios_entregados,
    }
    return render(request, 'admin/dashboard.html', context)

# CRUD Views
class PremiosCRUDView(UserPassesTestMixin, ListView):
    model = Premio
    template_name = 'admin/premios_crud.html'
    
    def test_func(self):
        return self.request.user.is_superuser

class ClientesCRUDView(UserPassesTestMixin, ListView):
    model = Cliente
    template_name = 'admin/clientes_crud.html'

    def test_func(self):
        return self.request.user.is_superuser

class GanadoresListView(UserPassesTestMixin, ListView):
    model = Ganador
    template_name = 'admin/ganadores_list.html'

    def test_func(self):
        return self.request.user.is_superuser