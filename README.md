# TIENDA DE CELULARES
Evaluación 3 Back End.

## Ficha de la propuesta

| Campo | Información |
|---|---|
| Plataforma | **CeluMarket** |
| Giro | Tienda de celulares con catálogo y compra simulada |
| Integrantes y RUT | José Benavides (RUT no proporcionado). Si corresponde, registrar el segundo integrante y su RUT con información real antes de la entrega. |
| Entidad de agrupación (Django ORM) | `Marca` |
| Entidad principal gestionable (Django ORM) | `Celular` |
| Propósito de `request.session` | Carrito temporal para agregar, actualizar y eliminar celulares, controlar el stock y calcular el desglose económico y un comprobante simulado |
| Validación de la propuesta por el docente | Pendiente de confirmar por el equipo con el docente. |

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
