
from django.contrib import admin
from .models import Categoria, Producto, Pedido, ItemPedido, DireccionEnvio, Perfil

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    search_fields = ["nombre"]

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre","precio","stock","activo","categoria")
    list_filter = ("activo","categoria")
    search_fields = ("nombre",)
    prepopulated_fields = {"slug": ("nombre",)}

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    readonly_fields = ("precio_unitario","subtotal")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id","usuario","estado","metodo_envio","total","creado_en")
    list_filter = ("estado","metodo_envio","creado_en")
    inlines = [ItemPedidoInline]

@admin.register(DireccionEnvio)
class DireccionEnvioAdmin(admin.ModelAdmin):
    list_display = ("usuario","calle","numero","ciudad","provincia","codigo_postal")
    search_fields = ("usuario__username","calle","ciudad","provincia")

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ("usuario","telefono","documento")
