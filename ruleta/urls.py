from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.RegistroClienteView.as_view(), name='registro_cliente'),
    path('jugar/<int:cliente_id>/', views.jugar_ruleta, name='jugar_ruleta'),
    path('guardar_resultado/', views.guardar_resultado, name='guardar_resultado'),
]
