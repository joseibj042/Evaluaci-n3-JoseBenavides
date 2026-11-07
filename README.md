# TIENDA DE CELULARES
Evaluación 3 Back End.

## Integrante
- José Benavides

## Ficha de la propuesta

| Campo | Información |
|---|---|
| Plataforma | **CeluMarket** |
| Giro | Tienda de celulares con catálogo y compra simulada |
| Integrantes y RUT | José Benavides — **[completar RUT]**; **[completar segundo integrante y RUT]** |
| Entidad de agrupación (Django ORM) | `Marca` |
| Entidad principal gestionable (Django ORM) | `Celular` |
| Propósito de `request.session` | Carrito temporal para agregar, actualizar y eliminar celulares, controlar el stock y calcular el desglose económico y un comprobante simulado |
| Validación de la propuesta por el docente | **[completar según aprobación real]** |

## Descripción

CeluMarket es una aplicación web de catálogo y gestión de teléfonos celulares. La portada presenta las marcas y permite acceder al catálogo filtrado. Cada producto tiene una ficha con su fotografía, descripción, precio en pesos chilenos y disponibilidad. La aplicación permite generar una compra simulada y consultar su comprobante.

El objetivo académico es implementar modelos relacionados, consultas con Django ORM, operaciones CRUD, sesiones HTTP, formularios, autenticación y control de acceso.

## Herramientas utilizadas

- Python 3 y Django 5.2.8.
- SQLite y Django ORM.
- HTML, CSS y Bootstrap 5.
- Pillow para las imágenes de productos.
- python-dotenv para las variables de entorno.
- Git y GitHub para el historial de versiones.

Las versiones exactas de las dependencias de Python están en `requirements.txt`.

## Modelo de datos

- **Marca:** nombre y descripción de cada fabricante.
- **Celular:** código único, marca asociada por `ForeignKey(on_delete=PROTECT)`, nombre, descripción, precio, stock, estado con opciones definidas, imagen y campo `activo` para baja lógica. Los valores numéricos se validan para impedir negativos.
- **Perfil:** relación uno a uno con el usuario de Django; incluye RUT, teléfono opcional y rol. El número de teléfono se conserva en el modelo y se administra desde Django Admin; por decisión de interfaz no se solicita ni se muestra en el registro o perfil público. Los permisos efectivos de administración dependen de `is_staff`, no del texto del rol.

## Funcionalidades

**Catálogo público:** portada por marcas, fichas de productos, búsqueda por nombre/código/descripción con `Q`, filtro por marca, ordenamiento por precio y nombre, y paginación de seis celulares por página.

**Panel de gestión:** crear y editar productos con `ModelForm`, imágenes con `request.FILES` y `multipart/form-data`, validaciones con `clean_()`, y desactivar productos con confirmación y baja lógica. Django Admin incluye `list_display`, `list_filter`, `search_fields`, `list_editable` y `fieldsets`.

**Carrito y comprobante:** productos y cantidades almacenados en `request.session`, validación de disponibilidad y stock, modificación y eliminación de productos, total, desglose del IVA incluido del 19 %, contador global mediante `context_processors`, y generación de comprobante simulado. Al confirmar se descuenta el stock de manera controlada. No existe una pasarela de pago real ni se emiten documentos tributarios.

**Usuarios:** registro, inicio de sesión, cierre de sesión por POST, consulta y modificación del perfil, protección de rutas administrativas con `login_required` y `user_passes_test`, y tokens CSRF en formularios POST.

**Diseño:** plantilla compartida `base.html`, Bootstrap 5, navegación adaptada a teléfonos y mensajes del sistema con Django Messages.

## Instalación local en Windows (PowerShell)

1. Descarga y descomprime el proyecto o clona el repositorio con `git clone https://github.com/joseibj042/Evaluaci-n3-JoseBenavides.git`.
2. Abre la carpeta donde se encuentra `manage.py`.
3. Crea el entorno virtual:

   ```powershell
   py -m venv .venv
   ```

4. Actívalo:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

5. Instala las dependencias:

   ```powershell
   python -m pip install -r requirements.txt
   ```

6. Copia el archivo de configuración:

   ```powershell
   Copy-Item .env.example .env
   ```

7. Genera una clave para `DJANGO_SECRET_KEY`:

   ```powershell
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```

   Sustituye `CAMBIAR_POR_CLAVE_GENERADA` en `.env` por la clave generada. Define también `CELUMARKET_ADMIN_PASSWORD` y `CELUMARKET_CLIENTE_PASSWORD` con dos contraseñas de prueba propias. No publiques ese archivo.

8. Prepara la base de datos y carga los productos de demostración:

   ```powershell
   python manage.py migrate
   python manage.py poblar_datos
   ```

   El comando carga **6 marcas, 30 celulares y 2 cuentas de prueba**. En una instalación nueva copia también las fotografías de demostración a `media/celulares/`. Si lo ejecutas de nuevo, **no sobreescribe** precios, stock, fotografías ni contraseñas de registros existentes.

9. Inicia el servidor:

   ```powershell
   python manage.py runserver
   ```

10. Abre `http://127.0.0.1:8000/`.

### Accesos de prueba

| Acceso | Dirección / usuario |
|---|---|
| Portada | `http://127.0.0.1:8000/` |
| Catálogo | `http://127.0.0.1:8000/catalogo/` |
| Carrito | `http://127.0.0.1:8000/carrito/` |
| Gestión | `http://127.0.0.1:8000/gestion/` |
| Django Admin | `http://127.0.0.1:8000/admin/` |
| Administrador de prueba | `admin_demo` |
| Cliente de prueba | `cliente_demo` |

Las contraseñas se establecen localmente en `.env`. Si los usuarios ya existen, `poblar_datos` no cambia sus contraseñas; para restablecer una se utiliza `python manage.py changepassword nombre_usuario`.

## Pruebas

```powershell
python manage.py check
python manage.py test catalogo
```

La aplicación contiene pruebas automatizadas para el catálogo, filtros, precios, CRUD, control de roles, sesiones, cálculo de IVA, registro y actualización de stock. Las pruebas de Django utilizan una base de datos temporal independiente de `db.sqlite3`.

**Resultado final en el equipo de entrega:** **[completar tras ejecutar los comandos]**.

## Bitácora de consultas técnicas con IA

Se documentan tres consultas utilizadas durante el desarrollo, con sus orientaciones y las decisiones adoptadas al integrarlas al proyecto.

### Caso 1 — Propuesta y modelos

**Consulta:** «debo realizar q tenga cosas correspondiente a mi nivel de conocimiento que sea de venta de celulares».

**Orientación técnica:** organizar el sistema como una tienda con marcas, celulares y usuarios; utilizar Django y SQLite, relacionando las entidades mediante el ORM.

**Aplicación y revisión:** se definieron `Marca`, `Celular` y `Perfil`. Los productos tienen código único, relación con una marca, campos validados y soporte para fotografías. La estructura se revisó respecto a los criterios de la pauta.

### Caso 2 — Consultas del catálogo

**Consulta:** «Terminé el quinto commit de CeluMarket y ya puedo ver el catálogo y los detalles de celulares. Guíame paso a paso para el sexto commit: agregar buscador por nombre, código y descripción con Q, filtros por marca, ordenar por precio y paginación con Paginator, siguiendo la pauta».

**Orientación técnica:** utilizar expresiones `Q` para la búsqueda en varios campos, `select_related('marca')` para consultar la relación de manera eficiente, `order_by` para el ordenamiento y `Paginator` para limitar los elementos visibles.

**Aplicación y revisión:** se añadieron búsqueda y filtros a la vista de catálogo; se ajustó la paginación a seis productos por página y se comprobó que los filtros siguieran operando con las distintas marcas.

### Caso 3 — Autenticación y permisos

**Consulta:** «Terminé el octavo commit de CeluMarket con carrito, request.session, stock, IVA y comprobante simulado. Guíame paso a paso para el noveno commit con registro de usuarios, inicio y cierre de sesión, perfil con RUT y teléfono, roles y seguridad, siguiendo mi pauta y sin perder las funciones anteriores».

**Orientación técnica:** aprovechar `UserCreationForm`, `LoginView`, `LogoutView`, `login_required`, `user_passes_test` y la protección CSRF de Django para implementar autenticación y rutas protegidas.

**Aplicación y revisión:** se crearon las páginas de registro y perfil y se aplicó la restricción `is_staff` a la gestión de productos. El perfil mantiene el teléfono como campo opcional de administración, sin solicitarlo en el formulario público.

## Control de versiones y entrega

El repositorio debe reflejar las etapas de configuración, modelos, carga de datos, catálogo, consultas y filtros, CRUD, carrito, usuarios, diseño, pruebas y documentación. Los commits publicados en GitHub constituyen el historial verificable de las contribuciones del equipo.

**Repositorio:** https://github.com/joseibj042/Evaluaci-n3-JoseBenavides

La entrega institucional requiere el enlace del repositorio y un ZIP del proyecto sin `.venv`, `.env` ni base de datos local. Las imágenes de demostración están incluidas en `catalogo/management/data/imagenes/` y se copian a la carpeta `media/` cuando se ejecuta `poblar_datos`.

Antes de la entrega, se deben completar los datos de los integrantes, verificar la aprobación del tema y registrar el resultado real de las pruebas.
