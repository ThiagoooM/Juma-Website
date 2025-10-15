
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.urls import reverse
from decimal import Decimal

from .models import Producto, Categoria, Pedido, ItemPedido, DireccionEnvio, MetodoEnvio, Perfil
from .forms import CheckoutForm, RegisterForm, PerfilForm
from .cart import Cart

class HomeView(TemplateView):
    template_name = "core/home.html"

class ComoComprarView(TemplateView):
    template_name = "core/como_comprar.html"

class ContactoView(TemplateView):
    template_name = "core/contacto.html"

class ProductoListView(ListView):
    model = Producto
    template_name = "core/product_list.html"
    context_object_name = "productos"
    paginate_by = 12
    def get_queryset(self):
        qs = Producto.objects.filter(activo=True).select_related("categoria")
        cat = self.request.GET.get("cat")
        if cat: qs = qs.filter(categoria__slug=cat)
        q = self.request.GET.get("q")
        if q: qs = qs.filter(nombre__icontains=q)
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["categorias"] = Categoria.objects.all()
        return ctx

class ProductoDetailView(DetailView):
    model = Producto
    template_name = "core/product_detail.html"
    context_object_name = "producto"
    slug_field = "slug"
    slug_url_kwarg = "slug"

def carrito_agregar(request, pk):
    cart = Cart(request); cart.add(product_id=pk, quantity=1)
    messages.success(request, "Producto agregado al carrito.")
    return redirect(request.META.get("HTTP_REFERER") or reverse("catalogo"))

def carrito_eliminar(request, pk):
    cart = Cart(request); cart.remove(product_id=pk)
    messages.info(request, "Producto eliminado del carrito.")
    return redirect("carrito_detalle")

def carrito_vaciar(request):
    cart = Cart(request); cart.clear()
    messages.info(request, "Carrito vacío.")
    return redirect("carrito_detalle")

def carrito_detalle(request):
    cart = Cart(request)
    return render(request, "core/cart.html", {"cart": list(cart), "total": cart.get_total_price()})

def registrar(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            Perfil.objects.get_or_create(usuario=user)
            login(request, user)
            messages.success(request, "Cuenta creada exitosamente.")
            return redirect("home")
    else:
        form = RegisterForm()
    return render(request, "core/register.html", {"form": form})

@login_required
def perfil(request):
    perfil, _ = Perfil.objects.get_or_create(usuario=request.user)
    if request.method == "POST":
        form = PerfilForm(request.POST, instance=perfil)
        if form.is_valid():
            form.save(); messages.success(request, "Perfil actualizado."); return redirect("perfil")
    else:
        form = PerfilForm(instance=perfil)
    return render(request, "core/perfil.html", {"form": form})

@login_required
def mis_pedidos(request):
    pedidos = Pedido.objects.filter(usuario=request.user).order_by("-creado_en")
    return render(request, "core/mis_pedidos.html", {"pedidos": pedidos})

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect("catalogo")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión para continuar.")
                return redirect("login")

            metodo = form.cleaned_data["metodo_envio"]
            pedido = Pedido.objects.create(usuario=request.user, metodo_envio=metodo)

            if metodo == "envio":
                direccion = DireccionEnvio.objects.create(
                    usuario=request.user,
                    nombre=form.cleaned_data["nombre"],
                    telefono=form.cleaned_data["telefono"],
                    calle=form.cleaned_data["calle"],
                    numero=form.cleaned_data["numero"],
                    ciudad=form.cleaned_data["ciudad"],
                    provincia=form.cleaned_data["provincia"],
                    codigo_postal=form.cleaned_data["codigo_postal"],
                    aclaraciones=form.cleaned_data["aclaraciones"],
                )
                pedido.direccion_envio = direccion
                pedido.nombre_receptor = form.cleaned_data["nombre"]
                pedido.telefono_receptor = form.cleaned_data["telefono"]
                pedido.save()

            total = Decimal("0.00")
            for item in cart:
                ItemPedido.objects.create(
                    pedido=pedido,
                    producto=item["product"],
                    cantidad=item["quantity"],
                    precio_unitario=item["price"],
                    subtotal=item["subtotal"]
                )
                total += item["subtotal"]

            pedido.total = total
            pedido.save()

            for item in cart:
                p = item["product"]
                p.stock = max(0, p.stock - item["quantity"])
                p.save()

            cart.clear()
            messages.success(request, "¡Pedido creado exitosamente!")
            return redirect("checkout_exito", pedido_id=pedido.id)
    else:
        form = CheckoutForm(initial={"metodo_envio": "retiro"})

    return render(request, "core/checkout.html", {
        "form": form,
        "cart": list(cart),
        "total": cart.get_total_price(),
    })

@login_required
def checkout_exito(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    return render(request, "core/checkout_success.html", {"pedido": pedido})

@login_required
def pedido_detalle(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id, usuario=request.user)
    items = pedido.items.select_related('producto')  # evita consultas repetidas
    return render(request, "core/pedido_detalle.html", {
        "pedido": pedido,
        "items": items,
    })