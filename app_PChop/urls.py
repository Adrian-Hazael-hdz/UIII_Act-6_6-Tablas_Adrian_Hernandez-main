from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_PChop, name='inicio'),
    
    # URLs de Usuario
    path('usuario/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuario/ver/', views.ver_usuarios, name='ver_usuarios'),
    path('usuario/actualizar/<int:usuario_id>/', views.actualizar_usuario, name='actualizar_usuario'),
    path('usuario/borrar/<int:usuario_id>/', views.borrar_usuario, name='borrar_usuario'),
    
    # URLs de Fabricante
    path('fabricante/agregar/', views.agregar_fabricante, name='agregar_fabricante'),
    path('fabricante/ver/', views.ver_fabricantes, name='ver_fabricantes'),
    path('fabricante/actualizar/<int:fabricante_id>/', views.actualizar_fabricante, name='actualizar_fabricante'),
    path('fabricante/borrar/<int:fabricante_id>/', views.borrar_fabricante, name='borrar_fabricante'),
    
    # URLs existentes de Categoría, Producto, Pedido
    path('categoria/agregar/', views.agregar_categoria, name='agregar_categoria'),
    path('categoria/ver/', views.ver_categorias, name='ver_categorias'),
    path('categoria/actualizar/<int:categoria_id>/', views.actualizar_categoria, name='actualizar_categoria'),
    path('categoria/borrar/<int:categoria_id>/', views.borrar_categoria, name='borrar_categoria'),
    
    path('producto/agregar/', views.agregar_producto, name='agregar_producto'),
    path('producto/ver/', views.ver_productos, name='ver_productos'),
    path('producto/actualizar/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('producto/borrar/<int:producto_id>/', views.borrar_producto, name='borrar_producto'),
    
    path('pedido/agregar/', views.agregar_pedido, name='agregar_pedido'),
    path('pedido/ver/', views.ver_pedidos, name='ver_pedidos'),
    path('pedido/actualizar/<int:pedido_id>/', views.actualizar_pedido, name='actualizar_pedido'),
    path('pedido/borrar/<int:pedido_id>/', views.borrar_pedido, name='borrar_pedido'),
    
    # URLs de DetallePedido
    path('detalle-pedido/agregar/', views.agregar_detalle_pedido, name='agregar_detalle_pedido'),
    path('detalle-pedido/ver/', views.ver_detalles_pedido, name='ver_detalles_pedido'),
    path('detalle-pedido/actualizar/<int:detalle_id>/', views.actualizar_detalle_pedido, name='actualizar_detalle_pedido'),
    path('detalle-pedido/borrar/<int:detalle_id>/', views.borrar_detalle_pedido, name='borrar_detalle_pedido'),
]