from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('registro/', views.RegistroClienteView.as_view(), name='registro_cliente'),
    path('jugar/<int:cliente_id>/', views.jugar_ruleta, name='jugar_ruleta'),  # Jugar con cliente_id
    path('jugar/', views.jugar_ruleta, name='jugar_ruleta'),  # Jugar sin cliente_id
    path('guardar_resultado/', views.guardar_resultado, name='guardar_resultado'),
    
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Ruta para logout

    # Rutas del CRUD para admin
    
    #CRUD premios
    path('admin/premios/', views.PremiosCRUDView.as_view(), name='premios_crud'),
    path('admin/premios/editar/<int:pk>/', views.EditarPremioView.as_view(), name='editar_premio'),
    path('admin/premios/crear/', views.CrearPremioView.as_view(), name='crear_premio'),
    path('admin/premios/eliminar/<int:pk>/', views.EliminarPremioView.as_view(), name='eliminar_premio'),
    path('premios/toggle/<int:pk>/', views.toggle_estado_premio, name='toggle_estado_premio'),
    
    
    # CRUD de clientes
    path('admin/clientes/', views.ClientesListView.as_view(), name='clientes_crud'),
    path('admin/clientes/crear/', views.CrearClienteView.as_view(), name='crear_cliente'),
    path('admin/clientes/editar/<int:pk>/', views.EditarClienteView.as_view(), name='editar_cliente'),
    path('admin/clientes/eliminar/<int:pk>/', views.EliminarClienteView.as_view(), name='eliminar_cliente'),

    path('admin/ganadores/', views.GanadoresListView.as_view(), name='ganadores_crud'),
    path('admin/ganadores/eliminar/<int:pk>/', views.EliminarGanadorView.as_view(), name='eliminar_ganador'),
    path('dashboard/', views.dashboard, name='dashboard'),
]