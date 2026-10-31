
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
]
