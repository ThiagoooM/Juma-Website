
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('catalogo/', views.ProductoListView.as_view(), name='catalogo'),
    path('producto/<slug:slug>/', views.ProductoDetailView.as_view(), name='producto_detalle'),
    path('carrito/', views.carrito_detalle, name='carrito_detalle'),
    path('carrito/agregar/<int:pk>/', views.carrito_agregar, name='carrito_agregar'),
    path('carrito/eliminar/<int:pk>/', views.carrito_eliminar, name='carrito_eliminar'),
    path('carrito/vaciar/', views.carrito_vaciar, name='carrito_vaciar'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/exito/<int:pedido_id>/', views.checkout_exito, name='checkout_exito'),
    path('como-comprar/', views.ComoComprarView.as_view(), name='como_comprar'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('registrar/', views.registrar, name='registrar'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('mis-pedidos/', views.mis_pedidos, name='mis_pedidos'),
    path("mis-pedidos/<int:pedido_id>/", views.pedido_detalle, name="pedido_detalle"),
]
