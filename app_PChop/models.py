from django.db import models
from django.contrib.auth.models import AbstractUser

# MODELO: USUARIO (Extiende AbstractUser)
class Usuario(AbstractUser):
    TIPO_USUARIO = [
        ('admin', 'Administrador'),
        ('cliente', 'Cliente'),
        ('vendedor', 'Vendedor'),
        ('almacen', 'Almacén'),
    ]
    
    telefono = models.CharField(max_length=15, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    tipo_usuario = models.CharField(max_length=10, choices=TIPO_USUARIO, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    imagen_perfil = models.ImageField(upload_to='usuarios/', blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.get_tipo_usuario_display()}"

# MODELO: FABRICANTE
class Fabricante(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    logo = models.ImageField(upload_to='fabricantes/', blank=True, null=True)

    def __str__(self):
        return self.nombre

# MODELO: CATEGORIA (Existente)
class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activa = models.BooleanField(default=True)
    imagen = models.ImageField(upload_to='categorias/', blank=True, null=True)
    slug = models.SlugField(unique=True)
    prioridad = models.IntegerField(default=1)

    def __str__(self):
        return self.nombre

# MODELO: PRODUCTO (Modificado para incluir fabricante)
class Producto(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos')
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE, related_name='productos', null=True, blank=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    marca = models.CharField(max_length=100)
    fecha_agregado = models.DateTimeField(auto_now_add=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    garantia_meses = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

# MODELO: PEDIDO (Existente)
class Pedido(models.Model):
    ESTADOS_PEDIDO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('preparacion', 'En preparación'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    ]
    
    METODOS_PAGO = [
        ('efectivo', 'Efectivo'),
        ('tarjeta_credito', 'Tarjeta de Crédito'),
        ('tarjeta_debito', 'Tarjeta de Débito'),
        ('transferencia', 'Transferencia'),
        ('paypal', 'PayPal'),
    ]
    
    # RELACIÓN MANY TO MANY CON PRODUCTOS (RESTAURADA)
    productos = models.ManyToManyField(Producto, related_name='pedidos')
    
    cliente = models.CharField(max_length=100)
    direccion_envio = models.TextField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS_PEDIDO, default='pendiente')
    metodo_pago = models.CharField(max_length=20, choices=METODOS_PAGO, default='efectivo')
    observaciones = models.TextField(blank=True, null=True)
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')

    def __str__(self):
        return f"Pedido #{self.id} - {self.cliente}"

# MODELO: DETALLE_PEDIDO
class DetallePedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='detalles_pedidos')
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Convertir a números antes de calcular
        cantidad = int(self.cantidad)
        precio_unitario = float(self.precio_unitario)
        self.subtotal = cantidad * precio_unitario
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle {self.id} - Pedido #{self.pedido.id}"