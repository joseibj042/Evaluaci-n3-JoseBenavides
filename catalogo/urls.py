
from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [

    path(
        '',
        views.catalogo,
        name='inicio'
    ),

    path(
        'celular/<slug:codigo>/',
        views.detalle_celular,
        name='detalle'
    ),

    path(
        'gestion/',
        views.gestion_celulares,
        name='gestion'
    ),

    path(
        'gestion/nuevo/',
        views.crear_celular,
        name='crear'
    ),

    path(
        'gestion/<slug:codigo>/editar/',
        views.editar_celular,
        name='editar'
    ),

    path(
        'gestion/<slug:codigo>/desactivar/',
        views.desactivar_celular,
        name='desactivar'
    ),

    path(
        'carrito/',
        views.ver_carrito,
        name='carrito'
    ),

    path(
        'carrito/agregar/<int:celular_id>/',
        views.agregar_carrito,
        name='agregar_carrito'
    ),

    path(
        'carrito/actualizar/<int:celular_id>/',
        views.actualizar_carrito,
        name='actualizar_carrito'
    ),

    path(
        'carrito/eliminar/<int:celular_id>/',
        views.eliminar_carrito,
        name='eliminar_carrito'
    ),

    path(
        'carrito/vaciar/',
        views.vaciar_carrito,
        name='vaciar_carrito'
    ),

    path(
        'carrito/finalizar/',
        views.finalizar_carrito,
        name='finalizar_carrito'
    ),

    path(
        'carrito/comprobante/',
        views.ver_comprobante,
        name='comprobante'
    ),
]
