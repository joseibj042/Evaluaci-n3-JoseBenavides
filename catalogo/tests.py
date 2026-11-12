from django.test import TestCase

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Marca, Celular, Perfil
from .forms import CelularForm

class PruebasTienda(TestCase):

    def setUp(self):

        self.marca = Marca.objects.create(
            nombre='Samsung',
            descripcion='Celulares Samsung'
        )

        self.otra_marca = Marca.objects.create(
            nombre='Apple',
            descripcion='Celulares Apple'
        )

        self.celular = Celular.objects.create(
            marca=self.marca,
            codigo='samsung-prueba',
            nombre='Samsung de prueba',
            descripcion='Bateria especial de prueba',
            precio=119000,
            stock=5,
            estado='disponible',
            activo=True
        )

        self.otro_celular = Celular.objects.create(
            marca=self.otra_marca,
            codigo='iphone-prueba',
            nombre='iPhone de prueba',
            descripcion='Celular Apple de prueba',
            precio=219000,
            stock=3,
            estado='disponible',
            activo=True
        )

        self.admin = User.objects.create_user(
            username='admin_prueba',
            password='ClaveSegura2026!',
            is_staff=True
        )

        self.cliente = User.objects.create_user(
            username='cliente_prueba',
            password='ClaveSegura2026!'
        )

    def datos_celular(self, **cambios):

        datos = {
            'marca': self.marca.pk,
            'codigo': self.celular.codigo,
            'nombre': self.celular.nombre,
            'descripcion': self.celular.descripcion,
            'precio': self.celular.precio,
            'stock': self.celular.stock,
            'estado': 'disponible',
            'activo': 'on',
        }

        datos.update(cambios)
        return datos

    def test_catalogo(self):

        respuesta = self.client.get(
            reverse('catalogo:catalogo')
        )

        self.assertEqual(respuesta.status_code, 200)

        self.assertContains(
            respuesta, 'Samsung de prueba'
        )

    def test_celular_desactivado(self):

        self.celular.activo = False
        self.celular.save()

        respuesta = self.client.get(
            reverse('catalogo:catalogo')
        )

        self.assertNotContains(
            respuesta, 'Samsung de prueba'
        )

    def test_busqueda(self):

        for texto in [
            'Samsung',
            'samsung-prueba',
            'Bateria especial'
        ]:

            with self.subTest(busqueda=texto):

                respuesta = self.client.get(
                    reverse('catalogo:catalogo'),
                    {'buscar': texto}
                )

                self.assertContains(
                    respuesta, 'Samsung de prueba'
                )

    def test_filtro_marca(self):

        respuesta = self.client.get(
            reverse('catalogo:catalogo'),
            {'marca': self.marca.id}
        )

        self.assertContains(
            respuesta, 'Samsung de prueba'
        )

        self.assertNotContains(
            respuesta, 'iPhone de prueba'
        )

    def test_paginacion(self):

        for numero in range(5):

            Celular.objects.create(
                marca=self.marca,
                codigo=f'extra-{numero}',
                nombre=f'Celular extra {numero}',
                descripcion='Producto de prueba',
                precio=100000,
                stock=2,
                estado='disponible',
                activo=True
            )

        pagina1 = self.client.get(
            reverse('catalogo:catalogo')
        )

        pagina2 = self.client.get(
            reverse('catalogo:catalogo'),
            {'page': 2}
        )

        self.assertEqual(
            len(pagina1.context['page_obj'].object_list),
            6
        )

        self.assertEqual(
            len(pagina2.context['page_obj'].object_list),
            1
        )

    def test_precio_formateado(self):

        self.assertEqual(
            self.celular.precio_formateado,
            '119.000'
        )

    def test_codigo_duplicado(self):

        formulario = CelularForm(
            data=self.datos_celular()
        )

        self.assertFalse(formulario.is_valid())
        self.assertIn('codigo', formulario.errors)

    def test_precio_negativo(self):

        formulario = CelularForm(
            data=self.datos_celular(
                codigo='celular-negativo',
                precio=-100
            )
        )

        self.assertFalse(formulario.is_valid())
        self.assertIn('precio', formulario.errors)

    def test_proteger_gestion(self):

        url = reverse('catalogo:gestion')

        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 302)

        self.client.force_login(self.cliente)
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 302)

        self.client.force_login(self.admin)
        respuesta = self.client.get(url)
        self.assertEqual(respuesta.status_code, 200)

    def test_crear_celular(self):

        self.client.force_login(self.admin)

        respuesta = self.client.post(
            reverse('catalogo:crear'),
            self.datos_celular(
                codigo='nuevo-celular',
                nombre='Nuevo celular'
            )
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertTrue(
            Celular.objects.filter(
                codigo='nuevo-celular'
            ).exists()
        )

    def test_editar_celular(self):

        self.client.force_login(self.admin)

        respuesta = self.client.post(
            reverse(
                'catalogo:editar',
                args=[self.celular.codigo]
            ),
            self.datos_celular(precio=150000)
        )

        self.assertEqual(respuesta.status_code, 302)

        self.celular.refresh_from_db()

        self.assertEqual(
            self.celular.precio,
            150000
        )

    def test_desactivar_celular(self):

        self.client.force_login(self.admin)

        url = reverse(
            'catalogo:desactivar',
            args=[self.celular.codigo]
        )

        self.client.get(url)
        self.celular.refresh_from_db()
        self.assertTrue(self.celular.activo)

        self.client.post(url)

        self.celular.refresh_from_db()
        self.assertFalse(self.celular.activo)

    def test_agregar_carrito(self):

        self.client.post(
            reverse(
                'catalogo:agregar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 2}
        )

        carrito = self.client.session.get('carrito', {})

        self.assertEqual(
            carrito[str(self.celular.id)],
            2
        )

    def test_limite_stock(self):

        self.client.post(
            reverse(
                'catalogo:agregar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 10}
        )

        carrito = self.client.session.get('carrito', {})

        self.assertEqual(carrito, {})

    def test_actualizar_y_eliminar_carrito(self):

        self.client.post(
            reverse(
                'catalogo:agregar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 1}
        )

        self.client.post(
            reverse(
                'catalogo:actualizar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 3}
        )

        self.assertEqual(
            self.client.session['carrito'][
                str(self.celular.id)
            ],
            3
        )

        self.client.post(
            reverse(
                'catalogo:eliminar_carrito',
                args=[self.celular.id]
            )
        )

        self.assertEqual(
            self.client.session['carrito'],
            {}
        )

    def test_calculo_iva(self):

        self.client.post(
            reverse(
                'catalogo:agregar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 1}
        )

        respuesta = self.client.get(
            reverse('catalogo:carrito')
        )

        self.assertContains(respuesta, '$100.000')
        self.assertContains(respuesta, '$19.000')
        self.assertContains(respuesta, '$119.000')

    def test_comprobante(self):

        self.client.post(
            reverse(
                'catalogo:agregar_carrito',
                args=[self.celular.id]
            ),
            {'cantidad': 1}
        )

        respuesta = self.client.post(
            reverse('catalogo:finalizar_carrito')
        )

        self.assertEqual(respuesta.status_code, 302)

        sesion = self.client.session

        self.assertEqual(sesion['carrito'], {})

        self.assertEqual(
            sesion['ultimo_comprobante']['total'],
            '119.000'
        )

        self.celular.refresh_from_db()
        self.assertEqual(self.celular.stock, 4)

    def test_registro_usuario(self):

        respuesta = self.client.post(
            reverse('catalogo:registro'),
            {
                'username': 'nuevo_cliente',
                'rut': 'TEST-001',
                'password1': 'ClaveSegura2026!',
                'password2': 'ClaveSegura2026!',
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        perfil = Perfil.objects.get(
            usuario__username='nuevo_cliente'
        )

        self.assertEqual(perfil.rol, 'cliente')
        self.assertFalse(perfil.usuario.is_staff)
        self.assertEqual(perfil.telefono, '')

    def test_editar_perfil(self):

        self.client.force_login(self.cliente)

        respuesta = self.client.post(
            reverse('catalogo:editar_perfil'),
            {
                'rut': 'TEST-002',
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        perfil = Perfil.objects.get(
            usuario=self.cliente
        )

        self.assertEqual(perfil.rut, 'TEST-002')
        self.assertEqual(perfil.telefono, '')

    def test_login_logout(self):

        respuesta = self.client.post(
            reverse('catalogo:login'),
            {
                'username': 'cliente_prueba',
                'password': 'ClaveSegura2026!'
            }
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertIn(
            '_auth_user_id',
            self.client.session
        )

        respuesta = self.client.post(
            reverse('catalogo:logout')
        )

        self.assertEqual(respuesta.status_code, 302)

        self.assertNotIn(
            '_auth_user_id',
            self.client.session
        )

    def test_inicio_presenta_marcas(self):
        respuesta = self.client.get(reverse('catalogo:inicio'))
        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, 'Samsung')
        self.assertContains(respuesta, 'Apple')
        self.assertContains(
            respuesta,
            f"{reverse('catalogo:catalogo')}?marca={self.marca.id}"
        )

    def test_pagina_catalogo_por_marca(self):
        respuesta = self.client.get(
            reverse('catalogo:catalogo'),
            {'marca': self.otra_marca.pk}
        )
        self.assertContains(respuesta, 'iPhone de prueba')
        self.assertNotContains(respuesta, 'Samsung de prueba')

    def test_registro_y_perfil_sin_telefono(self):
        respuesta = self.client.get(reverse('catalogo:registro'))
        self.assertNotContains(respuesta, 'Teléfono')
        self.client.force_login(self.cliente)
        respuesta = self.client.get(reverse('catalogo:perfil'))
        self.assertNotContains(respuesta, 'Teléfono')
        respuesta = self.client.get(reverse('catalogo:editar_perfil'))
        self.assertNotContains(respuesta, 'Teléfono')

    def test_stock_por_cantidad_y_sin_repetir_comprobante(self):
        self.client.post(
            reverse('catalogo:agregar_carrito', args=[self.celular.pk]),
            {'cantidad': 3}
        )
        self.client.post(reverse('catalogo:finalizar_carrito'))
        self.celular.refresh_from_db()
        self.assertEqual(self.celular.stock, 2)
        self.client.post(reverse('catalogo:finalizar_carrito'))
        self.celular.refresh_from_db()
        self.assertEqual(self.celular.stock, 2)

    def test_stock_insuficiente_no_descontar_otros(self):
        self.client.post(
            reverse('catalogo:agregar_carrito', args=[self.celular.pk]),
            {'cantidad': 2}
        )
        self.client.post(
            reverse('catalogo:agregar_carrito', args=[self.otro_celular.pk]),
            {'cantidad': 2}
        )
        self.otro_celular.stock = 1
        self.otro_celular.save(update_fields=['stock'])
        self.client.post(reverse('catalogo:finalizar_carrito'))
        self.celular.refresh_from_db()
        self.otro_celular.refresh_from_db()
        self.assertEqual(self.celular.stock, 5)
        self.assertEqual(self.otro_celular.stock, 1)
        self.assertNotEqual(self.client.session.get('carrito'), {})

    def test_registro_mensajes_django_en_espanol(self):
        respuesta = self.client.get(reverse('catalogo:registro'))
        self.assertContains(respuesta, 'Nombre de usuario')
        self.assertContains(respuesta, 'Confirmar contraseña')

    def test_compra_varios_celulares_descontando_cantidades(self):
        self.client.post(
            reverse('catalogo:agregar_carrito', args=[self.celular.pk]),
            {'cantidad': 2}
        )
        self.client.post(
            reverse('catalogo:agregar_carrito', args=[self.otro_celular.pk]),
            {'cantidad': 3}
        )
        respuesta = self.client.post(reverse('catalogo:finalizar_carrito'))
        self.assertEqual(respuesta.status_code, 302)
        self.celular.refresh_from_db()
        self.otro_celular.refresh_from_db()
        self.assertEqual(self.celular.stock, 3)
        self.assertEqual(self.otro_celular.stock, 0)
        self.assertEqual(len(self.client.session['ultimo_comprobante']['productos']), 2)
