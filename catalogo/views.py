
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import CelularForm

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

def es_administrador(usuario):
    return usuario.is_staff

@login_required(login_url='/admin/login/')
@user_passes_test(
    es_administrador,
    login_url='catalogo:inicio',
    redirect_field_name=None
)
def gestion_celulares(request):

    celulares = Celular.objects.select_related(
        'marca'
    ).order_by('nombre')

    return render(
        request,
        'catalogo/gestion.html',
        {'celulares': celulares}
    )

@login_required(login_url='/admin/login/')
@user_passes_test(
    es_administrador,
    login_url='catalogo:inicio',
    redirect_field_name=None
)
def crear_celular(request):

    if request.method == 'POST':

        form = CelularForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Celular agregado correctamente.'
            )

            return redirect('catalogo:gestion')

    else:
        form = CelularForm()

    return render(
        request,
        'catalogo/formulario_celular.html',
        {
            'form': form,
            'titulo': 'Agregar celular',
            'boton': 'Guardar celular'
        }
    )

@login_required(login_url='/admin/login/')
@user_passes_test(
    es_administrador,
    login_url='catalogo:inicio',
    redirect_field_name=None
)
def editar_celular(request, codigo):

    celular = get_object_or_404(
        Celular,
        codigo=codigo
    )

    if request.method == 'POST':

        form = CelularForm(
            request.POST,
            request.FILES,
            instance=celular
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Celular actualizado correctamente.'
            )

            return redirect('catalogo:gestion')

    else:
        form = CelularForm(instance=celular)

    return render(
        request,
        'catalogo/formulario_celular.html',
        {
            'form': form,
            'titulo': 'Editar celular',
            'boton': 'Guardar cambios'
        }
    )

@login_required(login_url='/admin/login/')
@user_passes_test(
    es_administrador,
    login_url='catalogo:inicio',
    redirect_field_name=None
)
def desactivar_celular(request, codigo):

    celular = get_object_or_404(
        Celular,
        codigo=codigo
    )

    if request.method == 'POST':

        celular.activo = False
        celular.save(update_fields=['activo'])

        messages.success(
            request,
            'Celular desactivado correctamente.'
        )

        return redirect('catalogo:gestion')

    return render(
        request,
        'catalogo/confirmar_desactivacion.html',
        {'celular': celular}
    )
