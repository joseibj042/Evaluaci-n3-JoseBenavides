
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Celular, Marca


def catalogo(request):

    busqueda = request.GET.get('buscar', '').strip()

    marca_texto = request.GET.get('marca', '')

    orden = request.GET.get('orden', 'nombre')

    celulares = Celular.objects.filter(
        activo=True
    ).select_related('marca')

    if busqueda:
        celulares = celulares.filter(
            Q(nombre__icontains=busqueda) |
            Q(codigo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda)
        )

    marca_actual = None

    if marca_texto.isdigit():
        marca_actual = int(marca_texto)
        celulares = celulares.filter(
            marca_id=marca_actual
        )

    opciones_orden = {
        'nombre': 'nombre',
        'precio_asc': 'precio',
        'precio_desc': '-precio',
    }

    if orden not in opciones_orden:
        orden = 'nombre'

    celulares = celulares.order_by(
        opciones_orden[orden],
        'id'
    )

    paginador = Paginator(celulares, 6)

    numero_pagina = request.GET.get('page')

    page_obj = paginador.get_page(numero_pagina)

    marcas = Marca.objects.all().order_by('nombre')

    contexto = {
        'celulares': page_obj,
        'page_obj': page_obj,
        'marcas': marcas,
        'busqueda': busqueda,
        'marca_actual': marca_actual,
        'orden_actual': orden,
    }

    return render(
        request,
        'catalogo/catalogo.html',
        contexto
    )

def detalle_celular(request, codigo):

    celular = get_object_or_404(
        Celular.objects.select_related('marca'),
        codigo=codigo,
        activo=True
    )

    return render(
        request,
        'catalogo/detalle.html',
        {'celular': celular}
    )
