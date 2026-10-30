
from django.shortcuts import render, get_object_or_404
from .models import Celular


def catalogo(request):

    celulares = Celular.objects.filter(
        activo=True
    ).select_related('marca').order_by('nombre')

    return render(
        request,
        'catalogo/catalogo.html',
        {'celulares': celulares}
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
