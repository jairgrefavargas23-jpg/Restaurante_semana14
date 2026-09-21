import tkinter as tk
from tkinter import ttk, messagebox

class MainView(tk.Frame):
    def __init__(self, parent, usuario_actual, servicio):
        super().__init__(parent)
        self.parent = parent
        self.usuario_actual = usuario_actual
        self.servicio = servicio

        self.pack(fill=tk.BOTH, expand=True)
        self._configurar_estilos()
        self._crear_layout()

    def _configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')

    def _crear_layout(self):
        # 1. Header / Barra superior
        header_frame = ttk.Frame(self, padding=10, relief=tk.RAISED)
        header_frame.pack(side=tk.TOP, fill=tk.X)

        lbl_bienvenida = ttk.Label(
            header_frame, 
            text=f"Restaurante App | Usuario: {self.usuario_actual.nombre} ({self.usuario_actual.rol})", 
            font=("Helvetica", 11, "bold")
        )
        lbl_bienvenida.pack(side=tk.LEFT)

        # 2. Contenedor del Notebook (Pestañas)
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestaña Productos
        tab_productos = ttk.Frame(notebook)
        notebook.add(tab_productos, text=" Gestión de Productos ")
        self._construir_pestana_productos(tab_productos)

        # Pestaña Usuarios
        tab_usuarios = ttk.Frame(notebook)
        notebook.add(tab_usuarios, text=" Consulta de Usuarios ")
        self._construir_pestana_usuarios(tab_usuarios)

    # -------------------------------------------------------------------------
    # PESTAÑA: PRODUCTOS
    # -------------------------------------------------------------------------
    def _construir_pestana_productos(self, parent):
        # Panel Izquierdo: Formulario y Acciones
        frame_izq = ttk.LabelFrame(parent, text=" Formulario de Producto ", padding=10)
        frame_izq.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 5), pady=10)

        # Campos
        ttk.Label(frame_izq, text="ID Producto:").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.ent_id = ttk.Entry(frame_izq, width=22)
        self.ent_id.grid(row=0, column=1, pady=4)

        ttk.Label(frame_izq, text="Nombre:").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.ent_nombre = ttk.Entry(frame_izq, width=22)
        self.ent_nombre.grid(row=1, column=1, pady=4)

        ttk.Label(frame_izq, text="Categoría:").grid(row=2, column=0, sticky=tk.W, pady=4)
        self.cmb_categoria = ttk.Combobox(
            frame_izq, 
            values=["Plato Fuerte", "Bebidas", "Postres", "Entradas"], 
            state="readonly", 
            width=20
        )
        self.cmb_categoria.current(0)
        self.cmb_categoria.grid(row=2, column=1, pady=4)

        ttk.Label(frame_izq, text="Precio ($):").grid(row=3, column=0, sticky=tk.W, pady=4)
        self.ent_precio = ttk.Entry(frame_izq, width=22)
        self.ent_precio.grid(row=3, column=1, pady=4)

        self.var_disponible = tk.BooleanVar(value=True)
        chk_disp = ttk.Checkbutton(frame_izq, text="Disponible para venta", variable=self.var_disponible)
        chk_disp.grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=8)

        # Botones de Acción
        frame_botones = ttk.Frame(frame_izq)
        frame_botones.grid(row=5, column=0, columnspan=2, pady=10)

        btn_registrar = ttk.Button(frame_botones, text="Registrar", command=self._registrar_producto)
        btn_registrar.grid(row=0, column=0, padx=2, pady=2)

        btn_consultar = ttk.Button(frame_botones, text="Cargar/Consultar", command=self._consultar_producto)
        btn_consultar.grid(row=0, column=1, padx=2, pady=2)

        btn_actualizar = ttk.Button(frame_botones, text="Actualizar", command=self._actualizar_producto)
        btn_actualizar.grid(row=1, column=0, padx=2, pady=2)

        btn_eliminar = ttk.Button(frame_botones, text="Eliminar", command=self._eliminar_producto)
        btn_eliminar.grid(row=1, column=1, padx=2, pady=2)

        btn_limpiar = ttk.Button(frame_izq, text="Limpiar Campos", command=self._limpiar_formulario)
        btn_limpiar.grid(row=6, column=0, columnspan=2, sticky=tk.EW, pady=(5, 0))

        # Panel Derecho: Tabla de Productos (Treeview)
        frame_der = ttk.LabelFrame(parent, text=" Catálogo de Productos ", padding=10)
        frame_der.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 10), pady=10)

        columnas = ("id", "nombre", "categoria", "precio", "disponible")
        self.tabla_prod = ttk.Treeview(frame_der, columns=columnas, show="headings")
        
        self.tabla_prod.heading("id", text="ID")
        self.tabla_prod.heading("nombre", text="Nombre")
        self.tabla_prod.heading("categoria", text="Categoría")
        self.tabla_prod.heading("precio", text="Precio")
        self.tabla_prod.heading("disponible", text="Disponible")

        self.tabla_prod.column("id", width=60, anchor=tk.CENTER)
        self.tabla_prod.column("nombre", width=160, anchor=tk.W)
        self.tabla_prod.column("categoria", width=100, anchor=tk.W)
        self.tabla_prod.column("precio", width=70, anchor=tk.E)
        self.tabla_prod.column("disponible", width=80, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(frame_der, orient=tk.VERTICAL, command=self.tabla_prod.yview)
        self.tabla_prod.configure(yscroll=scrollbar.set)

        self.tabla_prod.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self._refrescar_tabla_productos()

    def _limpiar_formulario(self):
        self.ent_id.delete(0, tk.END)
        self.ent_nombre.delete(0, tk.END)
        self.ent_precio.delete(0, tk.END)
        self.cmb_categoria.current(0)
        self.var_disponible.set(True)

    def _refrescar_tabla_productos(self):
        for item in self.tabla_prod.get_children():
            self.tabla_prod.delete(item)

        for p in self.servicio.obtener_productos():
            estado = "Sí" if p.disponible else "No"
            self.tabla_prod.insert("", tk.END, values=(p.id_producto, p.nombre, p.categoria, f"${p.precio:.2f}", estado))

    def _validar_precio(self) -> float | None:
        try:
            val = float(self.ent_precio.get().strip())
            return val
        except ValueError:
            messagebox.showerror("Error de entrada", "El precio debe ser un número válido.")
            return None

    def _registrar_producto(self):
        precio = self._validar_precio()
        if precio is None:
            return

        exito, msg = self.servicio.registrar_producto(
            id_producto=self.ent_id.get().strip(),
            nombre=self.ent_nombre.get().strip(),
            categoria=self.cmb_categoria.get(),
            precio=precio,
            disponible=self.var_disponible.get()
        )

        if exito:
            messagebox.showinfo("Éxito", msg)
            self._refrescar_tabla_productos()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", msg)

    def _consultar_producto(self):
        id_search = self.ent_id.get().strip()
        if not id_search:
            messagebox.showwarning("Atención", "Ingrese un ID de producto en el formulario para buscar.")
            return

        prod = self.servicio.buscar_producto_por_id(id_search)
        if prod:
            self._limpiar_formulario()
            self.ent_id.insert(0, prod.id_producto)
            self.ent_nombre.insert(0, prod.nombre)
            self.cmb_categoria.set(prod.categoria)
            self.ent_precio.insert(0, str(prod.precio))
            self.var_disponible.set(prod.disponible)
            messagebox.showinfo("Producto Encontrado", f"Datos cargados para '{prod.nombre}'.")
        else:
            messagebox.showerror("Sin resultados", f"No se encontró el producto con ID '{id_search}'.")

    def _actualizar_producto(self):
        precio = self._validar_precio()
        if precio is None:
            return

        exito, msg = self.servicio.actualizar_producto(
            id_producto=self.ent_id.get().strip(),
            nombre=self.ent_nombre.get().strip(),
            categoria=self.cmb_categoria.get(),
            precio=precio,
            disponible=self.var_disponible.get()
        )

        if exito:
            messagebox.showinfo("Éxito", msg)
            self._refrescar_tabla_productos()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", msg)

    def _eliminar_producto(self):
        id_prod = self.ent_id.get().strip()
        if not id_prod:
            messagebox.showwarning("Atención", "Ingrese o consulte el ID del producto que desea eliminar.")
            return

        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar el producto {id_prod}?"):
            exito, msg = self.servicio.eliminar_producto(id_prod)
            if exito:
                messagebox.showinfo("Éxito", msg)
                self._refrescar_tabla_productos()
                self._limpiar_formulario()
            else:
                messagebox.showerror("Error", msg)

    # -------------------------------------------------------------------------
    # PESTAÑA: USUARIOS
    # -------------------------------------------------------------------------
    def _construir_pestana_usuarios(self, parent):
        frame_user = ttk.LabelFrame(parent, text=" Usuarios Registrados ", padding=10)
        frame_user.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columnas = ("username", "nombre", "rol")
        tabla_users = ttk.Treeview(frame_user, columns=columnas, show="headings")

        tabla_users.heading("username", text="Usuario")
        tabla_users.heading("nombre", text="Nombre Completo")
        tabla_users.heading("rol", text="Rol")

        tabla_users.column("username", width=120)
        tabla_users.column("nombre", width=220)
        tabla_users.column("rol", width=120)

        scrollbar = ttk.Scrollbar(frame_user, orient=tk.VERTICAL, command=tabla_users.yview)
        tabla_users.configure(yscroll=scrollbar.set)

        tabla_users.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for u in self.servicio.obtener_usuarios():
            tabla_users.insert("", tk.END, values=(u.username, u.nombre, u.rol))