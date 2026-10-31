from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction

from .models import Perfil
from .forms import RegistroForm, PerfilForm
from .carrito import resumen_carrito
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

@login_required(login_url='catalogo:login')
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

def ver_carrito(request):

    resumen = resumen_carrito(request)

    return render(
        request,
        'catalogo/carrito.html',
        resumen
    )

@require_POST
def agregar_carrito(request, celular_id):

    celular = get_object_or_404(
        Celular,
        pk=celular_id,
        activo=True
    )

    if not celular.disponible:
        messages.error(
            request,
            'Este celular no está disponible.'
        )
        return redirect('catalogo:carrito')

    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 0

    if cantidad < 1:
        messages.error(request, 'Cantidad no válida.')
        return redirect('catalogo:carrito')

    carrito = request.session.get('carrito', {}).copy()

    clave = str(celular.pk)

    actual = int(carrito.get(clave, 0))
    nueva_cantidad = actual + cantidad

    if nueva_cantidad > celular.stock:
        messages.error(
            request,
            'No hay suficiente stock para esa cantidad.'
        )
        return redirect('catalogo:carrito')

    carrito[clave] = nueva_cantidad

    request.session['carrito'] = carrito

    messages.success(
        request,
        'Celular agregado al carrito.'
    )

    return redirect('catalogo:carrito')

@require_POST
def actualizar_carrito(request, celular_id):

    celular = get_object_or_404(
        Celular,
        pk=celular_id
    )

    try:
        cantidad = int(request.POST.get('cantidad', 1))
    except (ValueError, TypeError):
        cantidad = 0

    if cantidad < 1:
        messages.error(
            request,
            'La cantidad debe ser mayor que cero.'
        )
        return redirect('catalogo:carrito')

    if not celular.disponible or cantidad > celular.stock:
        messages.error(
            request,
            'La cantidad supera el stock disponible.'
        )
        return redirect('catalogo:carrito')

    carrito = request.session.get('carrito', {}).copy()
    clave = str(celular.pk)

    if clave in carrito:
        carrito[clave] = cantidad
        request.session['carrito'] = carrito

        messages.success(
            request,
            'Cantidad actualizada correctamente.'
        )

    return redirect('catalogo:carrito')

@require_POST
def eliminar_carrito(request, celular_id):

    carrito = request.session.get('carrito', {}).copy()

    carrito.pop(str(celular_id), None)

    request.session['carrito'] = carrito

    messages.success(
        request,
        'Celular eliminado del carrito.'
    )

    return redirect('catalogo:carrito')

@require_POST
def vaciar_carrito(request):

    request.session['carrito'] = {}

    messages.success(
        request,
        'Carrito vaciado correctamente.'
    )

    return redirect('catalogo:carrito')

@require_POST
def finalizar_carrito(request):

    resumen = resumen_carrito(request)

    if not resumen['items']:
        messages.error(
            request,
            'Tu carrito está vacío.'
        )
        return redirect('catalogo:carrito')

    if resumen['problemas']:
        messages.error(
            request,
            'Revisa los productos antes de continuar.'
        )
        return redirect('catalogo:carrito')

    comprobante = {
        'fecha': timezone.localtime().strftime(
            '%d/%m/%Y %H:%M'
        ),
        'productos': [],
        'subtotal': resumen['subtotal_formateado'],
        'iva': resumen['iva_formateado'],
        'total': resumen['total_formateado'],
    }

    for item in resumen['items']:

        comprobante['productos'].append({
            'nombre': item['celular'].nombre,
            'cantidad': item['cantidad'],
            'precio': item['celular'].precio_formateado,
            'importe': item['importe_formateado'],
        })

    request.session['ultimo_comprobante'] = comprobante

    request.session['carrito'] = {}

    messages.success(
        request,
        'Solicitud simulada generada correctamente.'
    )

    return redirect('catalogo:comprobante')

def ver_comprobante(request):

    comprobante = request.session.get(
        'ultimo_comprobante'
    )

    if not comprobante:
        messages.info(
            request,
            'Todavía no tienes un comprobante.'
        )
        return redirect('catalogo:carrito')

    return render(
        request,
        'catalogo/comprobante.html',
        {'comprobante': comprobante}
    )

def registrar_usuario(request):

    if request.user.is_authenticated:
        return redirect('catalogo:perfil')

    if request.method == 'POST':

        form = RegistroForm(request.POST)

        if form.is_valid():

            with transaction.atomic():

                usuario = form.save()

                Perfil.objects.create(
                    usuario=usuario,
                    rut=form.cleaned_data['rut'],
                    telefono=form.cleaned_data['telefono'],
                    rol='cliente'
                )

            login(request, usuario)

            messages.success(
                request,
                'Tu cuenta fue creada correctamente.'
            )

            return redirect('catalogo:perfil')

    else:
        form = RegistroForm()

    return render(
        request,
        'catalogo/registro.html',
        {'form': form}
    )

@login_required
def perfil_usuario(request):

    perfil, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={
            'rol': (
                'administrador'
                if request.user.is_staff
                else 'cliente'
            )
        }
    )

    return render(
        request,
        'catalogo/perfil.html',
        {'perfil': perfil}
    )

@login_required
def editar_perfil(request):

    perfil, creado = Perfil.objects.get_or_create(
        usuario=request.user,
        defaults={
            'rol': (
                'administrador'
                if request.user.is_staff
                else 'cliente'
            )
        }
    )

    if request.method == 'POST':

        form = PerfilForm(
            request.POST,
            instance=perfil
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Perfil actualizado correctamente.'
            )

            return redirect('catalogo:perfil')

    else:
        form = PerfilForm(instance=perfil)

    return render(
        request,
        'catalogo/editar_perfil.html',
        {'form': form}
    )
