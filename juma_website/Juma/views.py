from django.shortcuts import render
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Producto, Carrito, ItemCarrito


# 🟢 LISTADO DE PRODUCTOS
class ProductoListView(ListView):
    model = Producto
    template_name = 'productos/lista_productos.html'
    context_object_name = 'productos'


# 🟠 DETALLE DE PRODUCTO
class ProductoDetailView(DetailView):
    model = Producto
    template_name = 'productos/detalle_producto.html'
    context_object_name = 'producto'


# 🛒 AGREGAR AL CARRITO
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    # Si el usuario está logueado -> guardar en base de datos
    if request.user.is_authenticated:
        carrito, _ = Carrito.objects.get_or_create(usuario=request.user, activo=True)
        item, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto)
        if not created:
            item.cantidad += 1
        item.save()

        # Crear historial en txt
        historial_path = os.path.join(settings.BASE_DIR, 'historial_carritos')
        os.makedirs(historial_path, exist_ok=True)
        archivo = os.path.join(historial_path, f'{request.user.username}_carrito.txt')

        with open(archivo, 'a', encoding='utf-8') as f:
            f.write(f'Producto agregado: {producto.nombre} (${producto.precio_venta})\n')

        return redirect('ver_carrito')

    # Si NO está logueado -> usar carrito en sesión
    carrito = request.session.get('carrito', {})
    pid = str(producto.id)
    if pid in carrito:
        carrito[pid]['cantidad'] += 1
    else:
        carrito[pid] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio_venta),
            'cantidad': 1,
            'imagen': producto.imagenes.first().imagen.url if producto.imagenes.exists() else '',
        }
    request.session['carrito'] = carrito
    request.session.modified = True

    return redirect('ver_carrito')


# 🧺 VER CARRITO
def ver_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
        items = carrito.items.all() if carrito else []
        total = carrito.total() if carrito else 0
    else:
        carrito = request.session.get('carrito', {})
        items = carrito.values()
        total = sum(item['precio'] * item['cantidad'] for item in carrito.values())

    return render(request, 'productos/carrito.html', {'items': items, 'total': total})


# ❌ VACIAR CARRITO
def vaciar_carrito(request):
    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(usuario=request.user, activo=True).first()
        if carrito:
            carrito.items.all().delete()
    else:
        request.session['carrito'] = {}
        request.session.modified = True
    return redirect('ver_carrito')
