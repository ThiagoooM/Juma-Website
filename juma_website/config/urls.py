"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from Juma.views import (
    ProductoListView,
    ProductoDetailView,
    agregar_al_carrito,
    ver_carrito,
    vaciar_carrito
)


urlpatterns = [
    path('', ProductoListView.as_view(), name='lista_productos'),
    path('producto/<int:pk>/', ProductoDetailView.as_view(), name='detalle_producto'),
    path('agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('vaciar/', vaciar_carrito, name='vaciar_carrito'),
]
