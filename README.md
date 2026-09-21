# Restaurante App - Semana 14

## Estudiante
Bryan Jair Grefa Alvarado

## Propósito
Evolución de la aplicación gráfica `restaurante_app` mediante el uso de **componentes, contenedores y gestores de geometría de Tkinter/ttk**, garantizando una interfaz ordenada, modular y desacoplada de la lógica de negocio y persistencia.

## Estructura del Proyecto




restaurante_app/
├── datos/
│   ├── productos.json
│   └── usuarios.json
├── modelos/
│   ├── init.py
│   ├── producto.py
│   └── usuario.py
├── servicios/
│   ├── init.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── init.py
│   ├── login_view.py
│   └── main_view.py
├── main.py
└── README.md



## Componentes y Contenedores Utilizados
- **Contenedores:** `Notebook` (pestañas principal/secundarias), `LabelFrame` (agrupación de formularios y tablas), `Frame` (paneles estructurados).
- **Componentes Formulario:** `Entry`, `Combobox` (para categorías), `Checkbutton` (para disponibilidad).
- **Componentes Presentación/Acciones:** `Treeview` (tablas con scrollbar vertical), `Button` vinculados mediante el parámetro `command=`.

## Operaciones de Productos Implementadas
1. **Registrar:** Agrega nuevos productos previa validación de campos obligatorios y formato.
2. **Cargar / Consultar:** Carga la información de un producto en los campos editables mediante su `ID`.
3. **Actualizar:** Modifica la información del producto manteniendo las reglas de negocio.
4. **Eliminar:** Remueve el registro previa confirmación de usuario.

## Pasos para Ejecutar
1. Ejecutar el archivo principal desde la raíz del proyecto:
   ```bash
   python main.py