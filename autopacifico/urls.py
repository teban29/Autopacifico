"""
URL configuration for autopacifico project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ruleta import views  # Cambia "ruleta" por el nombre de tu aplicación si es diferente.

urlpatterns = [
    path('', views.redirect_to_admin_login, name='redirect_to_admin_login'),  # Redirige al login
    path('dashboard/', views.dashboard, name='dashboard'),  # Ruta para el dashboard
    path('ruleta/', include('ruleta.urls')),  # Rutas de la aplicación
    path('admin/', admin.site.urls),  # Rutas del admin
]
