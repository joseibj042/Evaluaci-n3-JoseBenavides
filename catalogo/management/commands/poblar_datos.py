import json
import os
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from catalogo.models import Celular, Marca, Perfil


class Command(BaseCommand):
    help = 'Carga las marcas, los celulares y las cuentas de prueba'

    def handle(self, *args, **kwargs):
        password_admin = os.getenv('CELUMARKET_ADMIN_PASSWORD', '').strip()
        password_cliente = os.getenv('CELUMARKET_CLIENTE_PASSWORD', '').strip()

        if not password_admin or not password_cliente:
            raise CommandError(
                'Configura CELUMARKET_ADMIN_PASSWORD y '
                'CELUMARKET_CLIENTE_PASSWORD en .env'
            )

        carpeta_datos = Path(__file__).resolve().parent.parent / 'data'
        archivo = carpeta_datos / 'catalogo_inicial.json'
        with archivo.open(encoding='utf-8') as entrada:
            datos = json.load(entrada)

        with transaction.atomic():
            marcas = {}
            for elemento in datos['marcas']:
                marca, _ = Marca.objects.get_or_create(
                    nombre=elemento['nombre'],
                    defaults={'descripcion': elemento['descripcion']}
                )
                marcas[marca.nombre] = marca

            nuevos = 0
            for elemento in datos['celulares']:
                valores = {
                    'nombre': elemento['nombre'],
                    'descripcion': elemento['descripcion'],
                    'marca': marcas[elemento['marca']],
                    'precio': elemento['precio'],
                    'stock': elemento['stock'],
                    'estado': elemento['estado'],
                    'imagen': elemento['imagen'],
                    'activo': elemento['activo'],
                }
                _, creado = Celular.objects.get_or_create(
                    codigo=elemento['codigo'], defaults=valores
                )
                if creado:
                    nuevos += 1

            Usuario = get_user_model()
            usuarios = [
                ('admin_demo', password_admin, True, 'administrador'),
                ('cliente_demo', password_cliente, False, 'cliente'),
            ]
            for nombre, clave, administrador, rol in usuarios:
                usuario, creado = Usuario.objects.get_or_create(
                    username=nombre,
                    defaults={
                        'is_staff': administrador,
                        'is_superuser': administrador,
                        'is_active': True,
                    }
                )
                if creado:
                    usuario.set_password(clave)
                    usuario.save(update_fields=['password'])
                Perfil.objects.get_or_create(
                    usuario=usuario, defaults={'rol': rol}
                )

        for elemento in datos['celulares']:
            if not elemento['imagen']:
                continue
            origen = carpeta_datos / 'imagenes' / elemento['imagen']
            destino = Path(settings.MEDIA_ROOT) / elemento['imagen']
            if not origen.is_file():
                raise CommandError(f'Falta la imagen de ejemplo: {origen}')
            destino.parent.mkdir(parents=True, exist_ok=True)
            if not destino.exists():
                shutil.copy2(origen, destino)

        self.stdout.write(self.style.SUCCESS(
            f'Carga terminada: {len(marcas)} marcas, '
            f'{nuevos} celulares nuevos, 2 cuentas de prueba verificadas.'
        ))
        self.stdout.write('Los registros existentes no se modificaron.')
