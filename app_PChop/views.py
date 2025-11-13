from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Categoria, Pedido, Usuario, DetallePedido, Fabricante

def inicio_PChop(request):
    return render(request, 'inicio.html')

def agregar_categoria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        slug = request.POST.get('slug')
        prioridad = request.POST.get('prioridad')
        
        # Manejar la imagen - ESTA LÍNEA ES IMPORTANTE
        imagen = request.FILES.get('imagen')  # Usar FILES en lugar de POST
        
        categoria = Categoria(
            nombre=nombre,
            descripcion=descripcion,
            slug=slug,
            prioridad=prioridad
        )
        
        if imagen:
            categoria.imagen = imagen
            
        categoria.save()
        return redirect('ver_categorias')
    
    return render(request, 'categoria/agregar_categoria.html')

def ver_categorias(request):
    categorias = Categoria.objects.all()
    return render(request, 'categoria/ver_categorias.html', {'categorias': categorias})

def actualizar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        categoria.nombre = request.POST.get('nombre')
        categoria.descripcion = request.POST.get('descripcion')
        categoria.slug = request.POST.get('slug')
        categoria.prioridad = request.POST.get('prioridad')
        
        # MANEJAR LA NUEVA IMAGEN - ESTO ES IMPORTANTE
        nueva_imagen = request.FILES.get('imagen')  # Usar FILES, no POST
        if nueva_imagen:
            # Eliminar la imagen anterior si existe
            if categoria.imagen:
                categoria.imagen.delete(save=False)
            categoria.imagen = nueva_imagen
            
        categoria.save()
        return redirect('ver_categorias')
    
    return render(request, 'categoria/actualizar_categoria.html', {'categoria': categoria})

def borrar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    
    if request.method == 'POST':
        categoria.delete()
        return redirect('ver_categorias')
    
    return render(request, 'categoria/borrar_categoria.html', {'categoria': categoria})

# VISTAS PARA PRODUCTO
def agregar_producto(request):
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()  # NUEVO: Obtener fabricantes
    
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        fabricante_id = request.POST.get('fabricante')  # NUEVO: Obtener fabricante
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        marca = request.POST.get('marca')
        imagen = request.FILES.get('imagen')
        sku = request.POST.get('sku')  # NUEVO
        garantia_meses = request.POST.get('garantia_meses')  # NUEVO
        
        categoria = Categoria.objects.get(id=categoria_id)
        fabricante = Fabricante.objects.get(id=fabricante_id) if fabricante_id else None  # NUEVO
        
        producto = Producto(
            categoria=categoria,
            fabricante=fabricante,  # NUEVO: Asignar fabricante
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock,
            marca=marca,
            sku=sku,
            garantia_meses=garantia_meses
        )
        
        if imagen:
            producto.imagen = imagen
            
        producto.save()
        return redirect('ver_productos')
    
    return render(request, 'producto/agregar_producto.html', {
        'categorias': categorias,
        'fabricantes': fabricantes  # NUEVO: Pasar fabricantes al template
    })
def ver_productos(request):
    productos = Producto.objects.all().select_related('categoria')
    return render(request, 'producto/ver_productos.html', {'productos': productos})

def actualizar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    categorias = Categoria.objects.all()
    fabricantes = Fabricante.objects.all()  # NUEVO: Obtener fabricantes
    
    if request.method == 'POST':
        producto.categoria_id = request.POST.get('categoria')
        producto.fabricante_id = request.POST.get('fabricante')  # NUEVO: Actualizar fabricante
        producto.nombre = request.POST.get('nombre')
        producto.descripcion = request.POST.get('descripcion')
        producto.precio = request.POST.get('precio')
        producto.stock = request.POST.get('stock')
        producto.marca = request.POST.get('marca')
        producto.sku = request.POST.get('sku')  # NUEVO
        producto.garantia_meses = request.POST.get('garantia_meses')  # NUEVO
        
        nueva_imagen = request.FILES.get('imagen')
        if nueva_imagen:
            if producto.imagen:
                producto.imagen.delete(save=False)
            producto.imagen = nueva_imagen
            
        producto.save()
        return redirect('ver_productos')
    
    return render(request, 'producto/actualizar_producto.html', {
        'producto': producto,
        'categorias': categorias,
        'fabricantes': fabricantes  # NUEVO: Pasar fabricantes al template
    })

def borrar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        producto.delete()
        return redirect('ver_productos')
    
    return render(request, 'producto/borrar_producto.html', {'producto': producto})

# VISTAS PARA PEDIDO
def agregar_pedido(request):
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        cliente = request.POST.get('cliente')
        direccion_envio = request.POST.get('direccion_envio')
        total = request.POST.get('total')
        estado = request.POST.get('estado')
        metodo_pago = request.POST.get('metodo_pago')
        observaciones = request.POST.get('observaciones')
        productos_seleccionados = request.POST.getlist('productos')
        
        # Crear el pedido
        pedido = Pedido(
            cliente=cliente,
            direccion_envio=direccion_envio,
            total=total,
            estado=estado,
            metodo_pago=metodo_pago,
            observaciones=observaciones
        )
        pedido.save()
        
        # Agregar productos al pedido (relación muchos a muchos)
        for producto_id in productos_seleccionados:
            producto = Producto.objects.get(id=producto_id)
            pedido.productos.add(producto)
            
        return redirect('ver_pedidos')
    
    return render(request, 'pedido/agregar_pedido.html', {'productos': productos})

def ver_pedidos(request):
    pedidos = Pedido.objects.all().prefetch_related('productos')
    return render(request, 'pedido/ver_pedidos.html', {'pedidos': pedidos})

def actualizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        pedido.cliente = request.POST.get('cliente')
        pedido.direccion_envio = request.POST.get('direccion_envio')
        pedido.total = request.POST.get('total')
        pedido.estado = request.POST.get('estado')
        pedido.metodo_pago = request.POST.get('metodo_pago')
        pedido.observaciones = request.POST.get('observaciones')
        
        # Actualizar productos del pedido
        productos_seleccionados = request.POST.getlist('productos')
        pedido.productos.clear()
        for producto_id in productos_seleccionados:
            producto = Producto.objects.get(id=producto_id)
            pedido.productos.add(producto)
            
        pedido.save()
        return redirect('ver_pedidos')
    
    return render(request, 'pedido/actualizar_pedido.html', {
        'pedido': pedido,
        'productos': productos
    })
def borrar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        pedido.delete()
        return redirect('ver_pedidos')
    
    return render(request, 'pedido/borrar_pedido.html', {'pedido': pedido})

def agregar_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        tipo_usuario = request.POST.get('tipo_usuario')
        password = request.POST.get('password')
        imagen_perfil = request.FILES.get('imagen_perfil')
        
        usuario = Usuario(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            telefono=telefono,
            direccion=direccion,
            tipo_usuario=tipo_usuario
        )
        usuario.set_password(password)
        
        if imagen_perfil:
            usuario.imagen_perfil = imagen_perfil
            
        usuario.save()
        return redirect('ver_usuarios')
    
    return render(request, 'usuario/agregar_usuario.html')

def ver_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'usuario/ver_usuarios.html', {'usuarios': usuarios})

def actualizar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        usuario.username = request.POST.get('username')
        usuario.email = request.POST.get('email')
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.telefono = request.POST.get('telefono')
        usuario.direccion = request.POST.get('direccion')
        usuario.tipo_usuario = request.POST.get('tipo_usuario')
        
        nueva_imagen = request.FILES.get('imagen_perfil')
        if nueva_imagen:
            if usuario.imagen_perfil:
                usuario.imagen_perfil.delete(save=False)
            usuario.imagen_perfil = nueva_imagen
            
        usuario.save()
        return redirect('ver_usuarios')
    
    return render(request, 'usuario/actualizar_usuario.html', {'usuario': usuario})

def borrar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    
    if request.method == 'POST':
        usuario.delete()
        return redirect('ver_usuarios')
    
    return render(request, 'usuario/borrar_usuario.html', {'usuario': usuario})

# VISTAS PARA FABRICANTE
def agregar_fabricante(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        direccion = request.POST.get('direccion')
        logo = request.FILES.get('logo')
        
        fabricante = Fabricante(
            nombre=nombre,
            descripcion=descripcion,
            telefono=telefono,
            email=email,
            direccion=direccion
        )
        
        if logo:
            fabricante.logo = logo
            
        fabricante.save()
        return redirect('ver_fabricantes')
    
    return render(request, 'fabricante/agregar_fabricante.html')

def ver_fabricantes(request):
    fabricantes = Fabricante.objects.all()
    return render(request, 'fabricante/ver_fabricantes.html', {'fabricantes': fabricantes})

def actualizar_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    
    if request.method == 'POST':
        fabricante.nombre = request.POST.get('nombre')
        fabricante.descripcion = request.POST.get('descripcion')
        fabricante.telefono = request.POST.get('telefono')
        fabricante.email = request.POST.get('email')
        fabricante.direccion = request.POST.get('direccion')
        
        nuevo_logo = request.FILES.get('logo')
        if nuevo_logo:
            if fabricante.logo:
                fabricante.logo.delete(save=False)
            fabricante.logo = nuevo_logo
            
        fabricante.save()
        return redirect('ver_fabricantes')
    
    return render(request, 'fabricante/actualizar_fabricante.html', {'fabricante': fabricante})

def borrar_fabricante(request, fabricante_id):
    fabricante = get_object_or_404(Fabricante, id=fabricante_id)
    
    if request.method == 'POST':
        fabricante.delete()
        return redirect('ver_fabricantes')
    
    return render(request, 'fabricante/borrar_fabricante.html', {'fabricante': fabricante})

# VISTAS PARA DETALLE_PEDIDO
def agregar_detalle_pedido(request):
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        pedido_id = request.POST.get('pedido')
        producto_id = request.POST.get('producto')
        cantidad = request.POST.get('cantidad')
        precio_unitario = request.POST.get('precio_unitario')
        
        pedido = Pedido.objects.get(id=pedido_id)
        producto = Producto.objects.get(id=producto_id)
        
        # Crear el detalle (el save() se encargará de convertir los tipos)
        detalle = DetallePedido(
            pedido=pedido,
            producto=producto,
            cantidad=cantidad,  # Se convertirá en el save()
            precio_unitario=precio_unitario  # Se convertirá en el save()
        )
        detalle.save()
        
        return redirect('ver_detalles_pedido')
    
    return render(request, 'detalle_pedido/agregar_detalle_pedido.html', {
        'pedidos': pedidos,
        'productos': productos
    })
def ver_detalles_pedido(request):
    detalles = DetallePedido.objects.all().select_related('pedido', 'producto')
    return render(request, 'detalle_pedido/ver_detalles_pedido.html', {'detalles': detalles})

def actualizar_detalle_pedido(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    pedidos = Pedido.objects.all()
    productos = Producto.objects.all()
    
    if request.method == 'POST':
        detalle.pedido_id = request.POST.get('pedido')
        detalle.producto_id = request.POST.get('producto')
        detalle.cantidad = request.POST.get('cantidad')
        detalle.precio_unitario = request.POST.get('precio_unitario')
        detalle.save()  # El save() se encargará de la conversión
        
        return redirect('ver_detalles_pedido')
    
    return render(request, 'detalle_pedido/actualizar_detalle_pedido.html', {
        'detalle': detalle,
        'pedidos': pedidos,
        'productos': productos
    })

def borrar_detalle_pedido(request, detalle_id):
    detalle = get_object_or_404(DetallePedido, id=detalle_id)
    
    if request.method == 'POST':
        detalle.delete()
        return redirect('ver_detalles_pedido')
    
    return render(request, 'detalle_pedido/borrar_detalle_pedido.html', {'detalle': detalle})