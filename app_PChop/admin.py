from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Fabricante, Categoria, Producto, Pedido, DetallePedido

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'tipo_usuario', 'activo']
    list_filter = ['tipo_usuario', 'activo', 'fecha_registro']
    search_fields = ['username', 'email', 'first_name', 'last_name']

@admin.register(Fabricante)
class FabricanteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'telefono', 'email', 'activo', 'fecha_registro']
    list_filter = ['activo', 'fecha_registro']
    search_fields = ['nombre', 'email']

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activa', 'prioridad', 'fecha_creacion']
    list_filter = ['activa', 'fecha_creacion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'fabricante', 'precio', 'stock', 'marca']
    list_filter = ['categoria', 'fabricante', 'marca']
    search_fields = ['nombre', 'marca', 'sku']

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'total', 'estado', 'metodo_pago', 'fecha_pedido']
    list_filter = ['estado', 'metodo_pago', 'fecha_pedido']
    search_fields = ['cliente']

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad', 'precio_unitario', 'subtotal']
    list_filter = ['pedido']
    search_fields = ['producto__nombre']