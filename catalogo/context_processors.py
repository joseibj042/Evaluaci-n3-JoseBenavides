def contador_carrito(request):
    carrito = request.session.get('carrito', {})

    total = sum(carrito.values())

    return {'cantidad_carrito': total}