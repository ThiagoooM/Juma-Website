from django.contrib import admin
from .models import Producto, ImagenProducto, Carrito, ItemCarrito


class ImagenProductoInline(admin.TabularInline):  # o StackedInline si querés en columnas
    model = ImagenProducto
    extra = 1  # cantidad de formularios vacíos listos para cargar


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio_venta', 'stock')
    search_fields = ('nombre',)
    list_filter = ('precio_venta',)
    ordering = ('nombre',)
    inlines = [ImagenProductoInline]  # 👈 esta línea es la clave


@admin.register(ImagenProducto)
class ImagenProductoAdmin(admin.ModelAdmin):
    list_display = ('producto', 'principal')
    list_filter = ('principal',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado_en', 'activo')
    list_filter = ('activo', 'creado_en')


@admin.register(ItemCarrito)
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'producto', 'cantidad')
