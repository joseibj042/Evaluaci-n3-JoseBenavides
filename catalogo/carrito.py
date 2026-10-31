from .models import Celular

def formato_pesos(valor):
    return f"{valor:,}".replace(",", ".")


def resumen_carrito(request):

    carrito = request.session.get('carrito', {})

    items = []
    problemas = []
    total = 0

    ids = [
        int(clave)
        for clave in carrito
        if str(clave).isdigit()
    ]

    celulares = Celular.objects.in_bulk(ids)

    for clave, cantidad_guardada in carrito.items():

        try:
            celular_id = int(clave)
            cantidad = int(cantidad_guardada)
        except (ValueError, TypeError):
            problemas.append('Hay un producto no válido.')
            continue

        celular = celulares.get(celular_id)

        if celular is None:
            problemas.append(
                'Un celular del carrito ya no existe.'
            )
            continue

        if cantidad < 1:
            problemas.append(
                f'Cantidad no válida para {celular.nombre}.'
            )
            continue

        if not celular.disponible or cantidad > celular.stock:
            problemas.append(
                f'Revisa la disponibilidad de {celular.nombre}.'
            )

        importe = celular.precio * cantidad
        total += importe

        items.append({
            'celular': celular,
            'cantidad': cantidad,
            'importe_formateado': formato_pesos(importe),
        })

    iva = (total * 19 + 59) // 119
    subtotal = total - iva

    return {
        'items': items,
        'problemas': problemas,
        'subtotal_formateado': formato_pesos(subtotal),
        'iva_formateado': formato_pesos(iva),
        'total_formateado': formato_pesos(total),
    }
