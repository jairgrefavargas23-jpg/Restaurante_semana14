import os
from modelos.producto import Producto
from modelos.usuario import Usuario
from servicios.archivo_servicio import ArchivoServicio


class RestauranteServicio:
    # Carpeta base = "restaurante_app" (2 niveles arriba de este archivo: servicios/ -> restaurante_app/)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RUTA_PRODUCTOS = os.path.join(BASE_DIR, "datos", "productos.json")
    RUTA_USUARIOS = os.path.join(BASE_DIR, "datos", "usuarios.json")

    def __init__(self):
        self.productos = []
        self.usuarios = []
        self._cargar_datos()

    def _cargar_datos(self):
        raw_prod = ArchivoServicio.cargar_json(self.RUTA_PRODUCTOS)
        self.productos = [Producto.from_dict(p) for p in raw_prod]

        raw_user = ArchivoServicio.cargar_json(self.RUTA_USUARIOS)
        self.usuarios = [Usuario.from_dict(u) for u in raw_user]

    def _guardar_productos(self) -> bool:
        datos = [p.to_dict() for p in self.productos]
        return ArchivoServicio.guardar_json(self.RUTA_PRODUCTOS, datos)

    # --- Métodos de Usuario ---
    def autenticar(self, username, password) -> Usuario | None:
        for u in self.usuarios:
            if u.username == username and u.password == password:
                return u
        return None

    def obtener_usuarios(self) -> list[Usuario]:
        return self.usuarios

    # --- Métodos de CRUD Producto ---
    def obtener_productos(self) -> list[Producto]:
        return self.productos

    def buscar_producto_por_id(self, id_producto: str) -> Producto | None:
        for p in self.productos:
            if p.id_producto == str(id_producto).strip():
                return p
        return None

    def registrar_producto(self, id_producto: str, nombre: str, categoria: str, precio: float, disponible: bool) -> tuple[bool, str]:
        if not id_producto or not nombre:
            return False, "El ID y el nombre son obligatorios."
        if self.buscar_producto_por_id(id_producto):
            return False, f"Ya existe un producto con el ID {id_producto}."
        if precio < 0:
            return False, "El precio no puede ser negativo."

        nuevo = Producto(id_producto, nombre, categoria, precio, disponible)
        self.productos.append(nuevo)
        if self._guardar_productos():
            return True, "Producto registrado correctamente."
        return False, "Error al guardar los datos en disco."

    def actualizar_producto(self, id_producto: str, nombre: str, categoria: str, precio: float, disponible: bool) -> tuple[bool, str]:
        prod = self.buscar_producto_por_id(id_producto)
        if not prod:
            return False, f"No existe un producto con el ID {id_producto}."
        if not nombre:
            return False, "El nombre no puede estar vacío."
        if precio < 0:
            return False, "El precio no puede ser negativo."

        prod.nombre = nombre.strip()
        prod.categoria = categoria.strip()
        prod.precio = precio
        prod.disponible = disponible

        if self._guardar_productos():
            return True, "Producto actualizado correctamente."
        return False, "Error al actualizar la persistencia."

    def eliminar_producto(self, id_producto: str) -> tuple[bool, str]:
        prod = self.buscar_producto_por_id(id_producto)
        if not prod:
            return False, f"No se encontró el producto con ID {id_producto}."

        self.productos.remove(prod)
        if self._guardar_productos():
            return True, "Producto eliminado exitosamente."
        return False, "Error al guardar los cambios."