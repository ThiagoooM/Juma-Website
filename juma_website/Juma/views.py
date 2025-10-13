import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .models import Producto, Carrito, ItemCarrito
from .forms import EditarPerfilForm, ProductoForm
from django.contrib.auth import logout


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

        # Guardar historial en la carpeta Juma/historial_carritos
        archivo = os.path.join(settings.HISTORIAL_DIR, f'{request.user.username}_carrito.txt')
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


# 🔒 Verifica si el usuario es administrador
def es_admin(user):
    return user.is_staff or user.is_superuser


# 🧱 CREAR PRODUCTO (solo admin)
@login_required
@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/crear_producto.html', {'form': form})


# ✏️ EDITAR PRODUCTO (solo admin)
@login_required
@user_passes_test(es_admin)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto editado correctamente.')
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})


# 🧍 REGISTRO DE USUARIOS
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cuenta creada con éxito. Ahora puedes iniciar sesión.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


# 👤 PERFIL DE USUARIO
@login_required
def profile(request):
    return render(request, 'registration/profile.html')


# ⚙️ EDITAR PERFIL
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu perfil fue actualizado correctamente.')
            return redirect('profile')
    else:
        form = EditarPerfilForm(instance=request.user)

    return render(request, 'registration/editar_perfil.html', {'form': form})


def logout_view(request):
    """
    Cierra la sesión del usuario y redirige al login.
    """
    logout(request)  # 🔐 elimina la sesión del usuario
    messages.success(request, "Sesión cerrada correctamente.")
    return redirect('login')