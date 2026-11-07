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



