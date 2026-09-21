



# Restaurante App - Semana 14: Componentes y contenedores

Nombre del estudiante: Bryan Jair Grefa Alvarado


Proyecto de la asignatura **Programación Orientada a Objetos**. Es la evolución de la aplicación gráfica `restaurante_app` de la semana anterior: se mantiene la arquitectura modular y se mejora la capa de interfaz usando componentes, contenedores y gestores de geometría de Tkinter/ttk.

## Propósito de la Semana 14

Aplicar correctamente componentes y contenedores de Tkinter para construir una interfaz clara y ordenada, donde el usuario pueda consultar usuarios y gestionar productos del restaurante. La lógica y las validaciones permanecen en el servicio, no en la interfaz.

## Estructura del proyecto

```
restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md
```

| Capa | Responsabilidad |
|------|-----------------|
| `datos/` | Archivos JSON con los productos y los usuarios. |
| `modelos/` | Clases `Producto` y `Usuario`, con conversión a y desde diccionarios. |
| `servicios/` | `ArchivoServicio` lee y escribe los JSON. `RestauranteServicio` contiene la autenticación, las validaciones y las operaciones sobre productos. |
| `ui/` | `LoginView` (inicio de sesión) y `MainView` (interfaz principal). Solo presentan datos y piden las operaciones al servicio. |
| `main.py` | Punto de entrada: crea el servicio, muestra el login y abre la vista principal. |

## Componentes y contenedores utilizados

**Contenedores**
- `tk.Tk`: ventana principal de la aplicación.
- `tk.Toplevel`: ventana de inicio de sesión.
- `tk.Frame` y `ttk.Frame`: agrupan zonas de la interfaz (encabezado, botones, pestañas).
- `ttk.LabelFrame`: separa el formulario de producto, el catálogo y la lista de usuarios.
- `ttk.Notebook`: navegación por pestañas entre "Gestión de Productos" y "Consulta de Usuarios".

**Componentes**
- `ttk.Label`: títulos y etiquetas de campos.
- `ttk.Entry`: captura de ID, nombre, precio, usuario y contraseña (esta última con `show="*"`).
- `ttk.Combobox`: selección de la categoría del producto.
- `ttk.Checkbutton`: indica si el producto está disponible para la venta.
- `ttk.Button`: acciones mediante `command=`.
- `ttk.Treeview` con `ttk.Scrollbar`: tablas de productos y de usuarios.

**Gestores de geometría**
- `pack`: distribución de las zonas principales (encabezado, pestañas, panel izquierdo y derecho).
- `grid`: alineación de las etiquetas, campos y botones dentro del formulario.

## Mejoras realizadas en la interfaz

- Encabezado con el nombre y el rol del usuario que inició sesión.
- Navegación por pestañas para separar productos y usuarios.
- Pestaña de productos dividida en dos zonas: formulario con acciones a la izquierda y catálogo a la derecha.
- Tablas con encabezados, alineación por columna y barra de desplazamiento.
- La tabla de productos se actualiza después de cada operación.
- Ventana de login centrada; si se cierra sin iniciar sesión, la aplicación termina.

## Operaciones sobre productos

Todas se ejecutan con botones (`command=`) y se delegan a `RestauranteServicio`:

- **Registrar:** crea un producto nuevo.
- **Cargar/Consultar:** busca un producto por su ID y carga sus datos en el formulario.
- **Actualizar:** modifica nombre, categoría, precio y disponibilidad de un producto existente.
- **Eliminar:** borra un producto, con confirmación previa.
- **Limpiar Campos:** vacía el formulario.

Validaciones realizadas en el servicio: ID y nombre obligatorios, ID no repetido, categoría válida, precio numérico y no negativo, y existencia del producto para consultar, actualizar o eliminar.

## Persistencia

Los productos se guardan en `datos/productos.json` a través de `ArchivoServicio`, invocado desde `RestauranteServicio`. La interfaz nunca lee ni escribe archivos directamente. Los cambios se conservan al cerrar y volver a abrir la aplicación. Los usuarios se leen desde `datos/usuarios.json`.

## Cómo ejecutar

Requisitos: Python 3.10 o superior. No se necesitan librerías externas (solo la biblioteca estándar, con Tkinter incluido).

```bash
cd restaurante_app
python main.py
```

Usuarios de prueba incluidos en `datos/usuarios.json`:

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| `admin` | `123` | Administrador |
| `mesero1` | `123` | Mesero | 
 