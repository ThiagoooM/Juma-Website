
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from decimal import Decimal
User = get_user_model()

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True)
    class Meta: ordering = ["nombre"]
    def __str__(self): return self.nombre

class Producto(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.SET_NULL, null=True, related_name='productos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    stock = models.PositiveIntegerField(default=0)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    slug = models.SlugField(unique=True)
    class Meta: ordering = ["nombre"]
    def __str__(self): return self.nombre

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=30, blank=True)
    documento = models.CharField(max_length=30, blank=True)
    def __str__(self): return f"Perfil de {self.usuario}"

class MetodoEnvio(models.TextChoices):
    RETIRO = "retiro", "Retiro en el local"
    ENVIO = "envio", "Envío a domicilio"

class DireccionEnvio(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="direcciones_envio")
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=30, blank=True)
    calle = models.CharField(max_length=120)
    numero = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=80)
    provincia = models.CharField(max_length=80)
    codigo_postal = models.CharField(max_length=20)
    aclaraciones = models.CharField(max_length=200, blank=True)
    def __str__(self): return f"{self.calle} {self.numero}, {self.ciudad}"

class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="pedidos")
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    metodo_envio = models.CharField(max_length=10, choices=MetodoEnvio.choices, default=MetodoEnvio.RETIRO)
    direccion_envio = models.ForeignKey('DireccionEnvio', null=True, blank=True, on_delete=models.SET_NULL)
    nombre_receptor = models.CharField(max_length=100, blank=True)
    telefono_receptor = models.CharField(max_length=30, blank=True)
    ESTADOS = [("pendiente","Pendiente"),("pagado","Pagado"),("en_preparacion","En preparación"),("enviado","Enviado"),("entregado","Entregado"),("cancelado","Cancelado")]
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    def __str__(self): return f"Pedido #{self.id} - {self.get_estado_display()}"
    def calcular_total(self):
        t = sum(i.subtotal for i in self.items.all()); self.total = t; return t

class ItemPedido(models.Model):
    pedido = models.ForeignKey('Pedido', on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey('Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self): return f"{self.cantidad} x {self.producto.nombre}"
    def save(self, *args, **kwargs):
        if not self.precio_unitario: self.precio_unitario = self.producto.precio
        self.subtotal = Decimal(self.cantidad) * Decimal(self.precio_unitario)
        super().save(*args, **kwargs)
