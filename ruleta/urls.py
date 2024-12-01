from django.urls import path
from .views import RegistroClienteView, jugar_ruleta, guardar_resultado

urlpatterns = [
    path('registro/', RegistroClienteView.as_view(), name='registro_cliente'),
    path('jugar/', jugar_ruleta, name='jugar_ruleta'),
    path('guardar_resultado/', guardar_resultado, name='guardar_resultado'),
]
