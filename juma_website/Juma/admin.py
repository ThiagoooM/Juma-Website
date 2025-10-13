from django.contrib import admin
from .models import Categoria, Producto, ImagenProducto, Carrito, ItemCarrito


class ImagenProductoInline(admin.TabularInline):  # o StackedInline si querés en columnas
    model = ImagenProducto
    extra = 1  # cantidad de formularios vacíos listos para cargar


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria_padre')
    search_fields = ('nombre',)
    list_filter = ('categoria_padre',)

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_venta', 'stock')
    list_filter = ('categoria',)
    search_fields = ('nombre',)

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
