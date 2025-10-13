# Juma/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('lista/', views.ProductoListView.as_view(), name='lista_productos'),
    path('producto/<int:pk>/', views.ProductoDetailView.as_view(), name='detalle_producto'),
    path('carrito/', views.ver_carrito, name='ver_carrito'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/vaciar/', views.vaciar_carrito, name='vaciar_carrito'),

    # 🔒 Secciones de administración (solo admin)
    path('admin/crear/', views.crear_producto, name='crear_producto'),
    path('admin/editar/<int:pk>/', views.editar_producto, name='editar_producto'),

        # Login / perfil
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('editar-perfil/', views.editar_perfil, name='editar_perfil'),

        # Finalizar pedido
    path('finalizar-compra/', views.finalizar_compra, name='finalizar_compra'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),


]
