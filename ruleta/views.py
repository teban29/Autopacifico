from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
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
from django.urls import reverse_lazy, reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from collections import Counter
from django.db.models import Count
from django.db.models.functions import TruncDay


class RegistroClienteView(View):
    def get(self, request):
        form = ClienteForm()
        return render(request, 'ruleta/registro_cliente.html', {'form': form})

    def post(self, request):
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            request.session['cliente_id'] = cliente.id
            return redirect('jugar_ruleta', cliente_id=cliente.id)
        else:
            messages.error(request, 'Error al registrar cliente. Verifica los datos ingresados.')
        return render(request, 'ruleta/registro_cliente.html', {'form': form})



@login_required
def obtener_premios(request):
    premios = list(Premio.objects.filter(estado=True).values('nombre', 'probabilidad'))
    return JsonResponse({'premios': premios})

@login_required(login_url='/ruleta/registro/')
def jugar_ruleta(request, cliente_id=None):
    cliente_id = cliente_id or request.session.get('cliente_id')
    if not cliente_id:
        messages.error(request, 'Por favor, regístrate para jugar.')
        return redirect('registro_cliente')

    try:
        cliente = Cliente.objects.get(id=cliente_id)
    except Cliente.DoesNotExist:
        messages.error(request, 'Cliente no válido. Por favor, regístrate.')
        return redirect('registro_cliente')

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
    return redirect('/admin/login/?next=/dashboard/')


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@user_passes_test(lambda u: u.is_superuser, login_url='/admin/login/')
def dashboard(request):
    total_clientes = Cliente.objects.count()
    total_ganadores = Ganador.objects.count()

    # Premio más popular
    premios_populares = (
        Ganador.objects.values('premio__nombre')
        .annotate(count=Count('premio'))
        .order_by('-count')
    )
    premio_mas_popular = premios_populares[0]['premio__nombre'] if premios_populares else "N/A"

    # Clientes registrados por día
    registros_por_fecha = Cliente.objects.annotate(date=TruncDay('fecha_creacion')).values('date').annotate(count=Count('id')).order_by('date')
    registros_por_fecha_labels = [str(item['date']) for item in registros_por_fecha]
    registros_por_fecha_data = [item['count'] for item in registros_por_fecha]

    # Distribución de premios
    premios_distribucion = Counter(Ganador.objects.values_list('premio__nombre', flat=True))
    premios_labels = list(premios_distribucion.keys())
    premios_data = list(premios_distribucion.values())

    context = {
        'total_clientes': total_clientes,
        'total_premios': total_ganadores,
        'premio_mas_popular': premio_mas_popular,
        'registros_por_fecha': {
            'labels': registros_por_fecha_labels,
            'data': registros_por_fecha_data,
        },
        'premios_distribucion': {
            'labels': premios_labels,
            'data': premios_data,
        },
    }
    return render(request, 'admin/dashboard.html', context)

# CRUD Views
#CRUD premios
class PremiosCRUDView(UserPassesTestMixin, ListView):
    model = Premio
    template_name = 'admin/premios_crud.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
class CrearPremioView(UserPassesTestMixin, CreateView):
    model = Premio
    fields = ['nombre', 'descripcion', 'probabilidad', 'estado']
    template_name = 'admin/crear_premio.html'
    success_url = reverse_lazy('premios_crud')  # Redirige al CRUD de premios después de crear

    def test_func(self):
        return self.request.user.is_superuser  # Solo superusuarios pueden acceder
    
class EditarPremioView(UserPassesTestMixin, UpdateView):
    model = Premio
    fields = ['nombre', 'descripcion', 'probabilidad', 'estado']
    template_name = 'admin/editar_premio.html'
    success_url = reverse_lazy('premios_crud')

    def test_func(self):
        return self.request.user.is_superuser

class EliminarPremioView(UserPassesTestMixin, DeleteView):
    model = Premio
    template_name = 'admin/eliminar_premio.html'  # Crea esta plantilla si es necesario
    success_url = reverse_lazy('premios_crud')

    def test_func(self):
        # Permitir acceso solo a usuarios superusuarios
        return self.request.user.is_superuser

class ClientesListView(UserPassesTestMixin, ListView):
    model = Cliente
    template_name = 'admin/clientes_crud.html'
    context_object_name = 'clientes'

    def test_func(self):
        return self.request.user.is_superuser

# Crear cliente
class CrearClienteView(UserPassesTestMixin, CreateView):
    model = Cliente
    fields = ['cedula', 'nombre', 'apellidos', 'numero_telefono', 'numero_factura']
    template_name = 'admin/crear_cliente.html'
    success_url = reverse_lazy('clientes_crud')

    def test_func(self):
        return self.request.user.is_superuser

# Editar cliente
class EditarClienteView(UserPassesTestMixin, UpdateView):
    model = Cliente
    fields = ['cedula', 'nombre', 'apellidos', 'numero_telefono','numero_factura']
    template_name = 'admin/editar_cliente.html'
    success_url = reverse_lazy('clientes_crud')

    def test_func(self):
        return self.request.user.is_superuser

# Eliminar cliente
class EliminarClienteView(UserPassesTestMixin, DeleteView):
    model = Cliente
    template_name = 'admin/eliminar_cliente.html'
    success_url = reverse_lazy('clientes_crud')

    def test_func(self):
        return self.request.user.is_superuser



#CRUD ganadores

from django.urls import reverse_lazy

# Listar ganadores
class GanadoresListView(UserPassesTestMixin, ListView):
    model = Ganador
    template_name = 'admin/ganadores_crud.html'
    context_object_name = 'ganadores'

    def test_func(self):
        return self.request.user.is_superuser

# Eliminar ganador
class EliminarGanadorView(UserPassesTestMixin, DeleteView):
    model = Ganador
    template_name = 'admin/eliminar_ganador.html'
    success_url = reverse_lazy('ganadores_crud')

    def test_func(self):
        return self.request.user.is_superuser


@require_POST
@csrf_exempt
def toggle_estado_premio(request, pk):
    premio = get_object_or_404(Premio, pk=pk)
    premio.estado = not premio.estado  # Cambia el estado del premio
    premio.save()
    return JsonResponse({'status': 'success'})