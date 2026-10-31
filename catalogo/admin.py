from django.contrib import admin
from .models import Marca, Celular, Perfil

admin.site.site_header = 'CeluMarket - Panel de Control'
admin.site.site_title = 'CeluMarket Admin'
admin.site.index_title = 'Gestión de Celulares'

@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):

    list_display = (
        'nombre',
        'descripcion'
    )

    search_fields = (
        'nombre',
    )

@admin.register(Celular)
class CelularAdmin(admin.ModelAdmin):

    list_display = (
        'codigo',
        'nombre',
        'marca',
        'precio',
        'stock',
        'estado',
        'activo',
    )

    list_filter = (
        'marca',
        'estado',
        'activo',
    )

    search_fields = (
        'codigo',
        'nombre',
        'descripcion',
    )

    list_editable = (
        'precio',
        'stock',
        'estado',
        'activo',
    )

    list_select_related = (
        'marca',
    )

    fieldsets = (

        ('Información del celular', {
            'fields': (
                'marca',
                'codigo',
                'nombre',
                'descripcion',
            )
        }),

        ('Precio y disponibilidad', {
            'fields': (
                'precio',
                'stock',
                'estado',
                'activo',
            )
        }),

        ('Fotografía', {
            'fields': (
                'imagen',
            )
        }),

    )

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):

    list_display = (
        'usuario',
        'rut',
        'telefono',
        'rol',
    )

    list_filter = (
        'rol',
    )

    search_fields = (
        'usuario__username',
        'rut',
    )
