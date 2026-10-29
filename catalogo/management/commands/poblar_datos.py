
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from catalogo.models import Marca, Celular, Perfil


class Command(BaseCommand):

    help = 'Carga marcas, celulares y usuarios de prueba'

    def handle(self, *args, **kwargs):

        marcas = [
            ('Samsung', 'Celulares Samsung'),
            ('Apple', 'Celulares iPhone'),
            ('Xiaomi', 'Celulares Xiaomi'),
            ('Motorola', 'Celulares Motorola'),
        ]

        for nombre, descripcion in marcas:
            Marca.objects.update_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion}
            )

        self.stdout.write('Marcas cargadas correctamente')

        celulares = [
            (
                'samsung-a55', 'Samsung Galaxy A55',
                'Samsung', 299990, 10
            ),
            (
                'samsung-s24', 'Samsung Galaxy S24',
                'Samsung', 799990, 6
            ),
            (
                'iphone-13', 'iPhone 13',
                'Apple', 449990, 8
            ),
            (
                'iphone-15', 'iPhone 15',
                'Apple', 699990, 5
            ),
            (
                'redmi-note-13', 'Redmi Note 13',
                'Xiaomi', 179990, 15
            ),
            (
                'xiaomi-13t', 'Xiaomi 13T',
                'Xiaomi', 399990, 7
            ),
            (
                'moto-g84', 'Motorola Moto G84',
                'Motorola', 199990, 12
            ),
            (
                'motorola-edge-40', 'Motorola Edge 40',
                'Motorola', 349990, 9
            ),
        ]

        for codigo, nombre, marca_nombre, precio, stock in celulares:

            marca = Marca.objects.get(nombre=marca_nombre)

            Celular.objects.update_or_create(
                codigo=codigo,
                defaults={
                    'nombre': nombre,
                    'marca': marca,
                    'descripcion': (
                        'Celular ' + nombre +
                        ' disponible en nuestra tienda.'
                    ),
                    'precio': precio,
                    'stock': stock,
                    'estado': 'disponible',
                    'activo': True,
                }
            )

        self.stdout.write('Celulares cargados correctamente')

        password_admin = os.getenv('CELUMARKET_ADMIN_PASSWORD')
        password_cliente = os.getenv('CELUMARKET_CLIENTE_PASSWORD')

        if not password_admin or not password_cliente:
            raise CommandError(
                'Debes configurar las contraseñas '
                'CELUMARKET_ADMIN_PASSWORD y '
                'CELUMARKET_CLIENTE_PASSWORD en .env'
            )

        Usuario = get_user_model()

        administrador, creado = Usuario.objects.get_or_create(
            username='admin_demo'
        )

        administrador.is_staff = True
        administrador.is_superuser = True
        administrador.is_active = True
        administrador.set_password(password_admin)
        administrador.save()

        Perfil.objects.update_or_create(
            usuario=administrador,
            defaults={'rol': 'administrador'}
        )

        cliente, creado = Usuario.objects.get_or_create(
            username='cliente_demo'
        )

        cliente.is_staff = False
        cliente.is_superuser = False
        cliente.is_active = True
        cliente.set_password(password_cliente)
        cliente.save()

        Perfil.objects.update_or_create(
            usuario=cliente,
            defaults={'rol': 'cliente'}
        )

        self.stdout.write(
            self.style.SUCCESS(
                'Datos de CeluMarket cargados correctamente'
            )
        )
