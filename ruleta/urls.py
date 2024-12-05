from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Registro y ruleta
    path('registro/', views.RegistroClienteView.as_view(), name='registro_cliente'),
    path('jugar/', views.jugar_ruleta, name='jugar_ruleta'),  # Maneja cliente_id desde la sesión

    # Guardar resultado
    path('guardar_resultado/', views.guardar_resultado, name='guardar_resultado'),
    
    # Logout
    path('admin/login/', views.AdminLoginView.as_view(), name='admin_login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # CRUD premios
    path('admin/premios/', views.PremiosCRUDView.as_view(), name='premios_crud'),
    path('admin/premios/editar/<int:pk>/', views.EditarPremioView.as_view(), name='editar_premio'),
    path('admin/premios/crear/', views.CrearPremioView.as_view(), name='crear_premio'),
    path('admin/premios/eliminar/<int:pk>/', views.EliminarPremioView.as_view(), name='eliminar_premio'),
    path('premios/toggle/<int:pk>/', views.toggle_estado_premio, name='toggle_estado_premio'),

    # CRUD clientes
    path('admin/clientes/', views.ClientesListView.as_view(), name='clientes_crud'),
    path('admin/clientes/crear/', views.CrearClienteView.as_view(), name='crear_cliente'),
    path('admin/clientes/editar/<int:pk>/', views.EditarClienteView.as_view(), name='editar_cliente'),
    path('admin/clientes/eliminar/<int:pk>/', views.EliminarClienteView.as_view(), name='eliminar_cliente'),

    # CRUD ganadores
    path('admin/ganadores/', views.GanadoresListView.as_view(), name='ganadores_crud'),
    path('admin/ganadores/eliminar/<int:pk>/', views.EliminarGanadorView.as_view(), name='eliminar_ganador'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
