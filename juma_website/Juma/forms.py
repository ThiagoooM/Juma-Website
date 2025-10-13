from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Producto, ImagenProducto


# 🟢 Formulario para crear o editar productos
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio_compra', 'precio_venta', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del producto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del producto'
            }),
            'precio_compra': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'precio_venta': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control'
            }),
        }


# 🖼️ Formulario para subir imágenes de productos
class ImagenProductoForm(forms.ModelForm):
    class Meta:
        model = ImagenProducto
        fields = ['imagen', 'principal']
        widgets = {
            'principal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# 👤 Formulario para editar perfil del usuario
class EditarPerfilForm(UserChangeForm):
    password = None  # Ocultamos el campo de contraseña

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }
