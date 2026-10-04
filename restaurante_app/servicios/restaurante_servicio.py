from servicios.archivo_servicio import ArchivoServicio
from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta


class RestauranteServicio:
    def __init__(self, archivo_servicio: ArchivoServicio) -> None:
        self.archivo_servicio = archivo_servicio
        self.usuarios: list[Usuario] = []
        self.productos: list[Producto] = []
        self.ventas: list[Venta] = []
        self.cargar_datos()

    def cargar_datos(self) -> None:
        usuarios_json = self.archivo_servicio.leer_json("usuarios.json")
        productos_json = self.archivo_servicio.leer_json("productos.json")
        ventas_json = self.archivo_servicio.leer_json("ventas.json")

        self.usuarios = [
            Usuario(
                datos.get("identificador", ""),
                datos.get("nombre", ""),
                datos.get("usuario", ""),
                datos.get("contraseña", ""),
                datos.get("rol", "Cliente"),
            )
            for datos in usuarios_json
        ]

        self.productos = [
            Producto(
                datos.get("codigo", datos.get("id", "")),
                datos.get("nombre", ""),
                datos.get("precio", 0),
            )
            for datos in productos_json
        ]

        self.ventas = [
            Venta(
                identificador=datos.get("identificador", ""),
                usuario_id=datos.get("usuario_id", ""),
                producto_codigo=datos.get("producto_codigo", ""),
                fecha=datos.get("fecha", ""),
            )
            for datos in ventas_json
        ]

    def guardar_usuarios(self) -> None:
        self.archivo_servicio.guardar_usuarios(
            [
                {
                    "identificador": usuario.identificador,
                    "nombre": usuario.nombre,
                    "usuario": usuario.usuario,
                    "contraseña": usuario.contraseña,
                    "rol": usuario.rol,
                }
                for usuario in self.usuarios
            ],
            "usuarios.json",
        )

    def validar_login(self, usuario: str, contraseña: str) -> Usuario | None:
        return next(
            (
                usuario_registrado
                for usuario_registrado in self.usuarios
                if usuario_registrado.usuario == usuario
                and usuario_registrado.contraseña == contraseña
            ),
            None,
        )

    def get_all_users(self) -> list[Usuario]:
        return self.usuarios

    def get_all_usuarios(self) -> list[Usuario]:
        return self.usuarios

    def get_all_products(self) -> list[Producto]:
        return self.productos

    def get_all_sales(self) -> list[Venta]:
        return self.ventas

    def registrar_usuario(self, usuario: Usuario) -> Usuario:
        if any(item.identificador == usuario.identificador for item in self.usuarios):
            raise ValueError(f"El identificador {usuario.identificador} ya existe.")

        if any(item.usuario.lower() == usuario.usuario.lower() for item in self.usuarios):
            raise ValueError(f"El usuario {usuario.usuario} ya existe en el sistema.")

        self.usuarios.append(usuario)
        self.guardar_usuarios()
        return usuario

    def actualizar_usuario(self, usuario: Usuario) -> Usuario:
        for indice, usuario_actual in enumerate(self.usuarios):
            if usuario_actual.identificador == usuario.identificador:
                self.usuarios[indice] = usuario
                self.guardar_usuarios()
                return usuario

        raise ValueError(f"No se encontró un usuario con el identificador {usuario.identificador}.")

    def eliminar_usuario(self, identificador: str) -> None:
        usuario = self.buscar_usuario_por_identificador(identificador)
        if usuario is None:
            raise ValueError(f"No se encontró un usuario con el identificador {identificador}.")

        self.usuarios = [item for item in self.usuarios if item.identificador != identificador]
        self.guardar_usuarios()

    def buscar_usuario_por_identificador(self, identificador: str) -> Usuario | None:
        identificador = str(identificador).strip()
        return next(
            (usuario for usuario in self.usuarios if usuario.identificador == identificador),
            None,
        )

    def buscar_producto_por_codigo(self, codigo: str) -> Producto | None:
        codigo = str(codigo).strip()
        return next((producto for producto in self.productos if producto.codigo == codigo), None)

    def add_product(self, producto: Producto) -> Producto:
        return self.registrar_producto(producto)

    def registrar_producto(self, producto: Producto) -> Producto:
        if any(item.codigo == producto.codigo for item in self.productos):
            raise ValueError(f"El código {producto.codigo} ya existe en el sistema.")

        self.productos.append(producto)
        self.archivo_servicio.guardar_productos(self.productos, "productos.json")
        return producto

    def actualizar_producto(self, producto: Producto) -> Producto:
        for indice, producto_actual in enumerate(self.productos):
            if producto_actual.codigo == producto.codigo:
                self.productos[indice] = producto
                self.archivo_servicio.guardar_productos(self.productos, "productos.json")
                return producto

        raise ValueError(f"No se encontró el producto con código {producto.codigo}.")

    def eliminar_producto(self, codigo: str) -> None:
        producto = self.buscar_producto_por_codigo(codigo)
        if producto is None:
            raise ValueError(f"No se encontró el producto con código {codigo}.")

        self.productos = [item for item in self.productos if item.codigo != codigo]
        self.archivo_servicio.guardar_productos(self.productos, "productos.json")

    def registrar_venta(self, venta: Venta) -> Venta:
        usuario = self.buscar_usuario_por_identificador(venta.usuario_id)
        if usuario is None:
            raise ValueError(f"El usuario con identificador {venta.usuario_id} no existe.")

        producto = self.buscar_producto_por_codigo(venta.producto_codigo)
        if producto is None:
            raise ValueError(f"El producto con código {venta.producto_codigo} no existe.")

        if any(item.identificador == venta.identificador for item in self.ventas):
            raise ValueError(f"La venta con identificador {venta.identificador} ya existe.")

        self.ventas.append(venta)
        self.archivo_servicio.guardar_ventas(
            [
                {
                    "identificador": item.identificador,
                    "usuario_id": item.usuario_id,
                    "producto_codigo": item.producto_codigo,
                    "fecha": item.fecha,
                }
                for item in self.ventas
            ],
            "ventas.json",
        )
        return venta

    def obtener_producto_por_codigo(self, codigo: str) -> Producto | None:
        return self.buscar_producto_por_codigo(codigo)