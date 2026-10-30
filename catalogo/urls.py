from django.urls import path
from . import views

app_name = 'catalogo'

urlpatterns = [
    path('', views.catalogo, name='inicio'),

    path(
        'celular/<slug:codigo>/',
        views.detalle_celular,
        name='detalle'
    ),
]
