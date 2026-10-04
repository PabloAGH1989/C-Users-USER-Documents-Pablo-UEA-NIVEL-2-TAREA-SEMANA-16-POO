import tkinter as tk
from datetime import date
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Callable, cast

from modelos.producto import Producto
from modelos.usuario import Usuario
from modelos.venta import Venta
from servicios.restaurante_servicio import RestauranteServicio


class MainView(tk.Frame):
    def __init__(
        self,
        parent: tk.Misc,
        servicio: RestauranteServicio,
        usuario_actual: Usuario,
        callback: Callable[[], None],
    ):
        super().__init__(parent, bg="#edf3f8")
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.callback = callback
        self.ruta_assets = Path(__file__).resolve().parents[1] / "assets"
        self._configurar_estilo_tablas()
        self.imagen_fondo = tk.PhotoImage(file=str(self.ruta_assets / "login.png")).subsample(3, 3)
        self._imagenes = {
            "logo": tk.PhotoImage(file=str(self.ruta_assets / "login.png")).subsample(3, 3),
            "productos": tk.PhotoImage(file=str(self.ruta_assets / "products.png")).subsample(23, 23),
            "usuarios": tk.PhotoImage(file=str(self.ruta_assets / "users.png")).subsample(18, 18),
            "ventas": tk.PhotoImage(file=str(self.ruta_assets / "products.png")).subsample(20, 20),
            "guardar": tk.PhotoImage(file=str(self.ruta_assets / "save.png")).subsample(24, 24),
            "eliminar": tk.PhotoImage(file=str(self.ruta_assets / "delete.png")).subsample(10, 10),
            "espacio": tk.PhotoImage(width=18, height=18),
        }
        self.crear_widgets()
        self.mostrar_panel_productos()

    def _configurar_estilo_tablas(self):
        estilo = ttk.Style()
        estilo.configure(
            "TablaSeparada.Treeview",
            rowheight=28,
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#1f2d3d",
            borderwidth=1,
            relief="solid",
            padding=(6, 4),
        )
        estilo.configure(
            "TablaSeparada.Treeview.Heading",
            background="#edf2f7",
            foreground="#1f2d3d",
            font=("Arial", 10, "bold"),
            borderwidth=1,
            relief="solid",
            padding=(8, 6),
        )
        estilo.map("TablaSeparada.Treeview", background=[("selected", "#dfeaf7")])

    def crear_widgets(self):
        topbar = tk.Frame(self, bg="#2b3d4e", height=40)
        topbar.pack(fill="x")

        tk.Label(topbar, text="● ● ●", bg="#2b3d4e", fg="#d2d9df", font=("Arial", 18)).place(x=18, y=8)

        perfil = tk.Frame(topbar, bg="#2b3d4e")
        perfil.pack(side="right", padx=18, pady=8)
        tk.Label(perfil, text="◉", bg="#2b3d4e", fg="#f1f5f9", font=("Arial", 12)).pack(side="left")
        tk.Label(perfil, text=self.usuario_actual.nombre, bg="#2b3d4e", fg="#f1f5f9", font=("Arial", 10)).pack(side="left", padx=(6, 0))
        tk.Label(perfil, text="▼", bg="#2b3d4e", fg="#f1f5f9", font=("Arial", 9)).pack(side="left", padx=(6, 0))

        contenido = tk.Frame(self, bg="#dfe7ee")
        contenido.pack(fill="both", expand=True)

        nav = tk.Frame(contenido, bg="#2f4454", width=210)
        nav.pack(side="left", fill="y")
        nav.pack_propagate(False)
        self._botones_nav: dict[str, tk.Button] = {}

        logo_frame = tk.Frame(nav, bg="#2f4454")
        logo_frame.pack(pady=(18, 12), padx=18, fill="x")
        tk.Label(logo_frame, image=self._imagenes["logo"], bg="#2f4454").pack(side="left")
        tk.Label(
            logo_frame,
            text="Sistema\nde Ventas",
            bg="#2f4454",
            fg="#ffffff",
            font=("Arial", 16, "bold"),
            justify="left",
        ).pack(side="left", padx=(10, 0))

        self._crear_boton_nav(nav, "Inicio", self.mostrar_panel_productos, self._imagenes["productos"], activo=False)
        self._crear_boton_nav(nav, "Ventas", self.mostrar_panel_ventas, self._imagenes["ventas"], activo=False)
        self._crear_boton_nav(nav, "Productos", self.mostrar_panel_productos, self._imagenes["productos"], activo=True)
        self._crear_boton_nav(nav, "Usuarios", self.mostrar_panel_usuarios, self._imagenes["usuarios"], activo=False)
        self._crear_boton_nav(nav, "Reportes", self.mostrar_panel_productos, self._imagenes["guardar"], activo=False)

        if self.usuario_actual.rol != "Administrador":
            self._botones_nav["Usuarios"].configure(state="disabled")
        tk.Button(
            nav,
            text="Cerrar sesión",
            width=12,
            height=2,
            bg="#d9534f",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.cerrar_sesion,
        ).pack(side="bottom", pady=(0, 18), padx=18, fill="x")

        self.area_trabajo = tk.Frame(contenido, bg="#edf3f8")
        self.area_trabajo.pack(side="left", fill="both", expand=True, padx=18, pady=18)

        self.panel_productos = tk.Frame(self.area_trabajo, bg="#edf3f8")
        self.panel_usuarios = tk.Frame(self.area_trabajo, bg="#edf3f8")
        self.panel_ventas = tk.Frame(self.area_trabajo, bg="#edf3f8")

        self.crear_panel_productos()
        self.crear_panel_usuarios()
        self.crear_panel_ventas()

    def _crear_boton_nav(
        self,
        contenedor: tk.Misc,
        texto: str,
        comando: Callable[[], None],
        imagen: tk.PhotoImage,
        activo: bool = False,
    ) -> None:
        color_fondo = "#4e8db8" if activo else "#2f4454"
        color_texto = "#ffffff" if activo else "#dfeaf7"
        boton = tk.Button(
            contenedor,
            text=texto,
            height=38,
            bg=color_fondo,
            fg=color_texto,
            font=("Arial", 11, "bold"),
            compound="left",
            padx=8,
            anchor="w",
            image=imagen,
            command=lambda: self._seleccionar_nav(texto, comando),
            bd=0,
        )
        self._botones_nav[texto] = boton
        boton.pack(pady=(0, 3), padx=12, fill="x")

    def _seleccionar_nav(self, texto: str, comando: Callable[[], None]) -> None:
        for nombre, boton in self._botones_nav.items():
            activo = nombre == texto
            boton.configure(
                bg="#4e8db8" if activo else "#2f4454",
                fg="#ffffff" if activo else "#dfeaf7",
            )
        comando()

    def _crear_boton_producto(
        self,
        contenedor: tk.Misc,
        texto: str,
        comando: Callable[[], None],
        imagen: tk.PhotoImage,
    ) -> tk.Button:
        boton = tk.Button(
            contenedor,
            text=texto,
            image=imagen,
            compound="left",
            command=comando,
            width=128,
            height=42,
            padx=6,
            pady=4,
        )
        boton.pack(side="left", padx=5)
        return boton

    def _crear_campo_producto(
        self,
        contenedor: tk.Misc,
        etiqueta: str,
        fila: int,
        ancho: int,
    ) -> tk.Entry:
        tk.Label(
            contenedor,
            text=etiqueta,
            bg="#ffffff",
            width=12,
            anchor="w",
        ).grid(row=fila, column=0, sticky="w", padx=(0, 12), pady=7)
        entrada = tk.Entry(contenedor, width=ancho)
        entrada.grid(row=fila, column=1, padx=0, pady=7, sticky="w")
        return entrada

    def crear_panel_productos(self):
        self.panel_productos.pack(fill="both", expand=True, padx=16, pady=16)

        titulo_frame = tk.Frame(self.panel_productos, bg="#ffffff")
        titulo_frame.pack(anchor="w", pady=(0, 10))
        tk.Label(titulo_frame, image=self._imagenes["productos"], bg="#ffffff").pack(side="left")
        titulo = tk.Label(
            titulo_frame,
            text="Sección de productos",
            bg="#ffffff",
            fg="#1f2d3d",
            font=("Arial", 16, "bold"),
            anchor="w",
        )
        titulo.pack(side="left", padx=(8, 0))

        form = tk.LabelFrame(self.panel_productos, text="Formulario de producto", bg="#ffffff", font=("Arial", 11, "bold"))
        form.pack(fill="x", padx=4, pady=(0, 10))

        campos = tk.Frame(form, bg="#ffffff")
        campos.pack(fill="x", padx=14, pady=(4, 0))

        self.codigo_entry = self._crear_campo_producto(campos, "Código", 0, 24)
        self.nombre_entry = self._crear_campo_producto(campos, "Nombre", 1, 30)
        self.precio_entry = self._crear_campo_producto(campos, "Precio", 2, 24)

        botones = tk.Frame(form, bg="#ffffff")
        botones.pack(anchor="w", padx=14, pady=(8, 12))

        self._crear_boton_producto(botones, "Registrar", self.registrar_producto, self._imagenes["guardar"])
        self._crear_boton_producto(botones, "Consultar", self.consultar_producto, self._imagenes["espacio"])
        self._crear_boton_producto(botones, "Actualizar", self.actualizar_producto, self._imagenes["guardar"])
        self._crear_boton_producto(botones, "Eliminar", self.eliminar_producto, self._imagenes["eliminar"])
        self._crear_boton_producto(botones, "Limpiar", self.limpiar_formulario, self._imagenes["espacio"])

        productos_disponibles = tk.LabelFrame(
            self.panel_productos,
            text="Productos disponibles",
            bg="#ffffff",
            font=("Arial", 11, "bold"),
        )
        productos_disponibles.pack(fill="both", expand=True)

        self.productos_tabla = ttk.Treeview(
            productos_disponibles,
            columns=("codigo", "nombre", "precio"),
            show="headings",
            style="TablaSeparada.Treeview",
        )
        self.productos_tabla.heading("codigo", text="codigo")
        self.productos_tabla.heading("nombre", text="nombre")
        self.productos_tabla.heading("precio", text="precio")
        self.productos_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self._separadores_productos: list[tk.Frame] = []
        self.productos_tabla.bind("<Configure>", lambda _: self._dibujar_separadores_productos())
        self.actualizar_resultado_productos()

    def crear_panel_usuarios(self):
        self.panel_usuarios.pack_forget()
        self.panel_usuarios.pack(fill="both", expand=True, padx=16, pady=16)

        titulo_frame = tk.Frame(self.panel_usuarios, bg="#ffffff")
        titulo_frame.pack(anchor="w", pady=(0, 10))
        tk.Label(titulo_frame, image=self._imagenes["usuarios"], bg="#ffffff").pack(side="left")
        titulo = tk.Label(
            titulo_frame,
            text="Gestión de usuarios",
            bg="#ffffff",
            fg="#1f2d3d",
            font=("Arial", 16, "bold"),
            anchor="w",
        )
        titulo.pack(side="left", padx=(8, 0))

        form = tk.LabelFrame(self.panel_usuarios, text="Formulario de usuario", bg="#ffffff", font=("Arial", 11, "bold"))
        form.pack(fill="x", padx=4, pady=(0, 10))

        campos = tk.Frame(form, bg="#ffffff")
        campos.pack(fill="x", padx=14, pady=(10, 0))

        col_izquierda = tk.Frame(campos, bg="#ffffff")
        col_izquierda.pack(side="left", fill="both", expand=True, padx=(0, 20))
        col_derecha = tk.Frame(campos, bg="#ffffff")
        col_derecha.pack(side="left", fill="both", expand=True)

        tk.Label(col_izquierda, text="Identificador", bg="#ffffff", width=14, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=6)
        self.identificador_usuario_entry = tk.Entry(col_izquierda, width=28)
        self.identificador_usuario_entry.grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(col_izquierda, text="Nombre", bg="#ffffff", width=14, anchor="w", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=6)
        self.nombre_usuario_entry = tk.Entry(col_izquierda, width=28)
        self.nombre_usuario_entry.grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(col_izquierda, text="Usuario", bg="#ffffff", width=14, anchor="w", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", pady=6)
        self.usuario_entry = tk.Entry(col_izquierda, width=28)
        self.usuario_entry.grid(row=2, column=1, sticky="w", pady=6)

        tk.Label(col_derecha, text="Contraseña", bg="#ffffff", width=16, anchor="w", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", pady=6)
        self.password_entry = tk.Entry(col_derecha, width=28, show="*")
        self.password_entry.grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(col_derecha, text="Rol", bg="#ffffff", width=16, anchor="w", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w", pady=6)
        self.rol_var = tk.StringVar(value="Cliente")
        self.rol_combo = ttk.Combobox(
            col_derecha,
            textvariable=self.rol_var,
            values=["Cliente", "Empleado", "Administrador"],
            state="readonly",
            width=26,
        )
        self.rol_combo.grid(row=1, column=1, sticky="w", pady=6)
        self.rol_combo.bind("<<ComboboxSelected>>", self.cambiar_rol_usuario)

        self.rol_combo.set("Cliente")
        self.panel_usuarios.bind("<Escape>", lambda event: self.limpiar_formulario_usuario())

        for campo in (
            self.identificador_usuario_entry,
            self.nombre_usuario_entry,
            self.usuario_entry,
            self.password_entry,
        ):
            campo.bind("<Return>", lambda event: self.registrar_usuario())

        botones = tk.Frame(form, bg="#ffffff")
        botones.pack(fill="x", padx=14, pady=(8, 16))

        tk.Button(botones, text="Registrar", width=12, bg="#2d7ff9", fg="white", font=("Arial", 10, "bold"), command=self.registrar_usuario).pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Actualizar", width=12, bg="#f0ad4e", fg="white", font=("Arial", 10, "bold"), command=self.actualizar_usuario).pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Eliminar", width=12, bg="#d9534f", fg="white", font=("Arial", 10, "bold"), command=self.eliminar_usuario).pack(side="left", padx=(0, 8))
        tk.Button(botones, text="Limpiar", width=12, bg="#6c757d", fg="white", font=("Arial", 10, "bold"), command=self.limpiar_formulario_usuario).pack(side="left")

        usuarios_registrados = tk.LabelFrame(
            self.panel_usuarios,
            text="Usuarios registrados",
            bg="#ffffff",
            font=("Arial", 11, "bold"),
        )
        usuarios_registrados.pack(fill="both", expand=True)

        self.usuarios_tabla = ttk.Treeview(
            usuarios_registrados,
            columns=("identificador", "nombre", "usuario", "rol"),
            show="headings",
            style="TablaSeparada.Treeview",
        )
        self.usuarios_tabla.heading("identificador", text="Identificador")
        self.usuarios_tabla.heading("nombre", text="Nombre")
        self.usuarios_tabla.heading("usuario", text="Usuario")
        self.usuarios_tabla.heading("rol", text="Rol")
        self.usuarios_tabla.column("identificador", width=110, anchor="center", stretch=False)
        self.usuarios_tabla.column("nombre", width=180, anchor="w", stretch=True)
        self.usuarios_tabla.column("usuario", width=160, anchor="w", stretch=True)
        self.usuarios_tabla.column("rol", width=140, anchor="center", stretch=False)
        self.usuarios_tabla.pack(fill="both", expand=True, padx=10, pady=10)
        self.usuarios_tabla.bind("<<TreeviewSelect>>", self.cargar_usuario_seleccionado)
        self.actualizar_tabla_usuarios()

    def cambiar_rol_usuario(self, _event=None):
        if hasattr(self, "rol_var"):
            self.rol_var.set(self.rol_combo.get())

    def limpiar_formulario_usuario(self):
        self.identificador_usuario_entry.delete(0, tk.END)
        self.nombre_usuario_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.rol_combo.set("Cliente")
        if hasattr(self, "usuarios_tabla"):
            for fila in list(self.usuarios_tabla.selection()):
                self.usuarios_tabla.selection_remove(fila)

    def cargar_usuario_seleccionado(self, _event=None):
        seleccion = self.usuarios_tabla.selection()
        if not seleccion:
            return

        identificador = self.usuarios_tabla.item(seleccion[0], "values")[0]
        usuario = self.servicio.buscar_usuario_por_identificador(identificador)
        if usuario is None:
            return

        self.identificador_usuario_entry.delete(0, tk.END)
        self.nombre_usuario_entry.delete(0, tk.END)
        self.usuario_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)

        self.identificador_usuario_entry.insert(0, usuario.identificador)
        self.nombre_usuario_entry.insert(0, usuario.nombre)
        self.usuario_entry.insert(0, usuario.usuario)
        self.password_entry.insert(0, usuario.contraseña)
        self.rol_combo.set(usuario.rol)

    def registrar_usuario(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el administrador puede gestionar usuarios.")
            return

        try:
            usuario = Usuario(
                self.identificador_usuario_entry.get().strip(),
                self.nombre_usuario_entry.get().strip(),
                self.usuario_entry.get().strip(),
                self.password_entry.get().strip(),
                self.rol_var.get().strip(),
            )
            self.servicio.registrar_usuario(usuario)
            self.limpiar_formulario_usuario()
            self.actualizar_tabla_usuarios()
            messagebox.showinfo("Registro", "Usuario registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Validación", str(error))

    def actualizar_usuario(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el administrador puede gestionar usuarios.")
            return

        try:
            usuario = Usuario(
                self.identificador_usuario_entry.get().strip(),
                self.nombre_usuario_entry.get().strip(),
                self.usuario_entry.get().strip(),
                self.password_entry.get().strip(),
                self.rol_var.get().strip(),
            )
            self.servicio.actualizar_usuario(usuario)
            self.actualizar_tabla_usuarios()
            messagebox.showinfo("Actualización", "Usuario actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Actualización", str(error))

    def eliminar_usuario(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning("Permisos", "Solo el administrador puede gestionar usuarios.")
            return

        identificador = self.identificador_usuario_entry.get().strip()
        if not identificador:
            seleccion = self.usuarios_tabla.selection()
            if not seleccion:
                messagebox.showwarning("Eliminación", "Seleccione un usuario para eliminar.")
                return
            identificador = self.usuarios_tabla.item(seleccion[0], "values")[0]

        if identificador == self.usuario_actual.identificador:
            messagebox.showwarning("Eliminación", "No puede eliminar la cuenta administrativa actualmente autenticada.")
            return

        try:
            if not messagebox.askyesno("Confirmación", "¿Desea eliminar este usuario?"):
                return
            self.servicio.eliminar_usuario(identificador)
            self.limpiar_formulario_usuario()
            self.actualizar_tabla_usuarios()
            messagebox.showinfo("Eliminación", "Usuario eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Eliminación", str(error))

    def actualizar_tabla_usuarios(self):
        if not hasattr(self, "usuarios_tabla"):
            return

        for fila in self.usuarios_tabla.get_children():
            self.usuarios_tabla.delete(fila)

        for usuario in self.servicio.get_all_users():
            self.usuarios_tabla.insert(
                "",
                "end",
                values=(usuario.identificador, usuario.nombre, usuario.usuario, usuario.rol),
            )

    def crear_panel_ventas(self):
        self.panel_ventas.pack_forget()
        self.panel_ventas.pack(fill="both", expand=True)

        encabezado = tk.Frame(self.panel_ventas, bg="#edf3f8")
        encabezado.pack(fill="x", pady=(0, 16))
        tk.Label(
            encabezado,
            text="Nueva Venta",
            bg="#edf3f8",
            fg="#22364a",
            font=("Arial", 26, "bold"),
            anchor="w",
        ).pack(anchor="w")

        form = tk.Frame(self.panel_ventas, bg="#edf3f8")
        form.pack(fill="x")

        campos = tk.Frame(form, bg="#edf3f8")
        campos.pack(fill="x")

        col_izq = tk.Frame(campos, bg="#edf3f8")
        col_izq.pack(side="left", fill="both", expand=True, padx=(0, 12))
        col_der = tk.Frame(campos, bg="#edf3f8")
        col_der.pack(side="left", fill="both", expand=True)

        self.usuario_combo = self.crear_selector_venta(
            col_izq,
            "Cliente",
            0,
            self.obtener_opciones_usuarios(),
        )

        self.producto_combo = self.crear_selector_venta(
            col_der,
            "Producto",
            0,
            self.obtener_opciones_productos(),
        )
        self.producto_combo.bind("<<ComboboxSelected>>", lambda _: self.actualizar_precio_venta())

        fila_baja = tk.Frame(form, bg="#edf3f8")
        fila_baja.pack(fill="x", pady=(18, 8))

        cant = tk.Frame(fila_baja, bg="#edf3f8")
        cant.pack(side="left", fill="both", expand=True, padx=(0, 12))
        self.cantidad_venta = self.crear_selector_venta(
            cant,
            "Cantidad",
            0,
            self.obtener_opciones_cantidad(),
            ancho=12,
        )
        self.cantidad_venta.current(0)

        precio = tk.Frame(fila_baja, bg="#edf3f8")
        precio.pack(side="left", fill="both", expand=True)
        tk.Label(precio, text="Precio unitario", bg="#edf3f8", fg="#2c3e50", font=("Arial", 11, "bold")).pack(anchor="w", pady=(0, 6))
        self.precio_venta_var = tk.StringVar(value="0.00")
        self.precio_venta = tk.Entry(precio, textvariable=self.precio_venta_var, font=("Arial", 10), width=25)
        self.precio_venta.pack(fill="x")

        tk.Button(
            form,
            text="Registrar venta",
            bg="#2aa39a",
            fg="white",
            font=("Arial", 12, "bold"),
            command=self.registrar_venta,
            width=20,
            height=2,
        ).pack(anchor="e", pady=(12, 20))

        ventas_disponibles = tk.LabelFrame(
            self.panel_ventas,
            text="Ventas registradas",
            bg="#ffffff",
            font=("Arial", 12, "bold"),
            bd=1,
        )
        ventas_disponibles.pack(fill="both", expand=True)

        self.ventas_tabla = ttk.Treeview(
            ventas_disponibles,
            columns=("identificador", "fecha", "cliente", "producto"),
            show="headings",
            height=12,
            style="TablaSeparada.Treeview",
        )
        self.ventas_tabla.heading("identificador", text="Código")
        self.ventas_tabla.heading("fecha", text="Fecha")
        self.ventas_tabla.heading("cliente", text="Cliente")
        self.ventas_tabla.heading("producto", text="Producto")
        self.ventas_tabla.column("identificador", width=90, anchor="center", stretch=False)
        self.ventas_tabla.column("fecha", width=120, anchor="center", stretch=False)
        self.ventas_tabla.column("cliente", width=160, anchor="w", stretch=True)
        self.ventas_tabla.column("producto", width=180, anchor="w", stretch=True)
        self.ventas_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.cargar_ventas_combo()
        self.actualizar_tabla_ventas()

    def cerrar_sesion(self):
        self.callback()

    def limpiar_formulario(self):
        self.codigo_entry.delete(0, tk.END)
        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)

    def registrar_producto(self):
        try:
            producto = Producto(
                self.codigo_entry.get().strip(),
                self.nombre_entry.get().strip(),
                self.precio_entry.get().strip(),
            )
            self.servicio.registrar_producto(producto)
            self.limpiar_formulario()
            self.actualizar_resultado_productos()
            self.cargar_ventas_combo()
            messagebox.showinfo("Registro", "Producto registrado correctamente.")
        except ValueError as error:
            messagebox.showerror("Validación", str(error))

    def consultar_producto(self):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Consulta", "Debe ingresar el código del producto.")
            return

        producto = self.servicio.buscar_producto_por_codigo(codigo)
        if producto is None:
            messagebox.showwarning("Consulta", f"No existe un producto con el código {codigo}.")
            return

        self.nombre_entry.delete(0, tk.END)
        self.precio_entry.delete(0, tk.END)
        self.nombre_entry.insert(0, producto.nombre)
        self.precio_entry.insert(0, str(producto.precio))
        self.actualizar_resultado_productos()

    def actualizar_producto(self):
        try:
            producto = Producto(
                self.codigo_entry.get().strip(),
                self.nombre_entry.get().strip(),
                self.precio_entry.get().strip(),
            )
            self.servicio.actualizar_producto(producto)
            self.actualizar_resultado_productos()
            self.cargar_ventas_combo()
            messagebox.showinfo("Actualización", "Producto actualizado correctamente.")
        except ValueError as error:
            messagebox.showerror("Actualización", str(error))

    def eliminar_producto(self):
        codigo = self.codigo_entry.get().strip()
        if not codigo:
            messagebox.showwarning("Eliminación", "Debe ingresar el código del producto.")
            return

        try:
            self.servicio.eliminar_producto(codigo)
            self.limpiar_formulario()
            self.actualizar_resultado_productos()
            self.cargar_ventas_combo()
            messagebox.showinfo("Eliminación", "Producto eliminado correctamente.")
        except ValueError as error:
            messagebox.showerror("Eliminación", str(error))

    def mostrar_panel_productos(self):
        self.panel_usuarios.pack_forget()
        self.panel_ventas.pack_forget()
        self.panel_productos.pack(fill="both", expand=True, padx=16, pady=16)

    def mostrar_panel_usuarios(self):
        if self.usuario_actual.rol != "Administrador":
            messagebox.showwarning("Acceso", "Solo el administrador puede gestionar usuarios.")
            self.mostrar_panel_productos()
            return

        self.panel_productos.pack_forget()
        self.panel_ventas.pack_forget()
        self.panel_usuarios.pack(fill="both", expand=True, padx=16, pady=16)

    def mostrar_panel_ventas(self):
        self.panel_productos.pack_forget()
        self.panel_usuarios.pack_forget()
        self.panel_ventas.pack(fill="both", expand=True, padx=16, pady=16)
        self.cargar_ventas_combo()

    def crear_selector_venta(
        self,
        contenedor: tk.Misc,
        etiqueta: str,
        fila: int,
        opciones: list[str],
        ancho: int = 24,
    ) -> ttk.Combobox:
        tk.Label(
            contenedor,
            text=etiqueta,
            bg="#edf3f8",
            fg="#2c3e50",
            font=("Arial", 11, "bold"),
        ).grid(row=fila, column=0, sticky="w", pady=(0, 8), padx=(0, 10))

        contenedor.grid_columnconfigure(1, weight=1)
        selector = ttk.Combobox(
            contenedor,
            values=list(opciones),
            state="readonly",
            width=ancho,
            font=("Arial", 10),
        )
        selector.grid(row=fila, column=1, sticky="ew", pady=(0, 8))
        return selector

    def obtener_opciones_usuarios(self) -> list[str]:
        return [
            f"{usuario.identificador} - {usuario.nombre}"
            for usuario in self.servicio.get_all_users()
        ]

    def obtener_opciones_productos(self) -> list[str]:
        return [
            f"{producto.codigo} - {producto.nombre}"
            for producto in self.servicio.get_all_products()
        ]

    def obtener_opciones_cantidad(self) -> list[str]:
        return [str(cantidad) for cantidad in range(1, 6)]

    def cargar_ventas_combo(self):
        valores_usuarios = self.obtener_opciones_usuarios()
        valores_productos = self.obtener_opciones_productos()

        self.usuario_combo["values"] = valores_usuarios
        self.producto_combo["values"] = valores_productos

        if valores_usuarios:
            self.usuario_combo.current(0)
        else:
            self.usuario_combo.set("")

        if valores_productos:
            self.producto_combo.current(0)
            self.actualizar_precio_venta()
        else:
            self.producto_combo.set("")
            self.precio_venta_var.set("0.00")

    def actualizar_precio_venta(self) -> None:
        producto_seleccionado = self.producto_combo.get().strip()
        if not producto_seleccionado:
            self.precio_venta_var.set("0.00")
            return

        codigo = producto_seleccionado.split(" - ", 1)[0]
        producto = self.servicio.buscar_producto_por_codigo(codigo)
        self.precio_venta_var.set(f"{producto.precio:.2f}" if producto else "0.00")

    def registrar_venta(self):
        usuario_seleccionado = self.usuario_combo.get().strip()
        producto_seleccionado = self.producto_combo.get().strip()

        if not usuario_seleccionado or not producto_seleccionado:
            messagebox.showwarning("Venta", "Debe seleccionar un usuario y un producto para registrar la venta.")
            return

        try:
            usuario_id, producto_codigo = self._extraer_datos_venta(
                usuario_seleccionado,
                producto_seleccionado,
            )
            venta = Venta(
                identificador=self._generar_identificador_venta(),
                usuario_id=usuario_id,
                producto_codigo=producto_codigo,
                fecha=date.today().isoformat(),
            )
            self.servicio.registrar_venta(venta)
            self.actualizar_tabla_ventas()
            messagebox.showinfo("Registro", "Venta registrada correctamente.")
        except AttributeError:
            messagebox.showerror("Venta", "El servicio no soporta la gestión de ventas.")
        except ValueError as error:
            messagebox.showerror("Validación", str(error))

    def _generar_identificador_venta(self):
        ventas = self.servicio.get_all_sales()
        numero = len(ventas) + 1
        return f"V{numero:03d}"

    @staticmethod
    def _extraer_datos_venta(usuario: str, producto: str) -> tuple[str, str]:
        return usuario.split(" - ", 1)[0], producto.split(" - ", 1)[0]

    def actualizar_resultado_productos(self):
        if hasattr(self, "productos_tabla"):
            for fila in self.productos_tabla.get_children():
                self.productos_tabla.delete(fila)

            for producto in self.servicio.get_all_products():
                self.productos_tabla.insert(
                    "",
                    "end",
                    values=(producto.codigo, producto.nombre, f"${producto.precio:.2f}"),
                )
            self._dibujar_separadores_productos()

    def _dibujar_separadores_productos(self) -> None:
        for separador in self._separadores_productos:
            separador.destroy()
        self._separadores_productos.clear()

        columnas = ("codigo", "nombre", "precio")
        filas_visibles: list[tuple[str, tuple[int, int, int, int]]] = []
        for fila in self.productos_tabla.get_children():
            caja = self.productos_tabla.bbox(fila, columnas[0])
            if isinstance(caja, tuple):
                filas_visibles.append((fila, caja))

        if not filas_visibles:
            return

        primera_fila, primera_caja = filas_visibles[0]
        ultima_caja = filas_visibles[-1][1]
        inicio_y = primera_caja[1]
        fin_y = ultima_caja[1] + ultima_caja[3]
        color_linea = "#c8d0d8"

        for columna in columnas[:-1]:
            caja = self.productos_tabla.bbox(primera_fila, columna)
            if isinstance(caja, tuple):
                separador = tk.Frame(self.productos_tabla, bg=color_linea, bd=0, highlightthickness=0)
                separador.place(x=caja[0] + caja[2] - 1, y=inicio_y, width=1, height=fin_y - inicio_y)
                self._separadores_productos.append(separador)

        for fila, caja in filas_visibles:
            ultima_celda = self.productos_tabla.bbox(fila, columnas[-1])
            if isinstance(ultima_celda, tuple):
                separador = tk.Frame(self.productos_tabla, bg=color_linea, bd=0, highlightthickness=0)
                separador.place(
                    x=caja[0],
                    y=caja[1] + caja[3] - 1,
                    width=ultima_celda[0] + ultima_celda[2] - caja[0],
                    height=1,
                )
                self._separadores_productos.append(separador)

    def mostrar_usuarios(self):
        if not hasattr(self, "usuarios_text"):
            return

        self.usuarios_text.delete("1.0", tk.END)
        usuarios = self.servicio.get_all_users()
        if not usuarios:
            self.usuarios_text.insert(tk.END, "No hay usuarios registrados.")
            return

        for indice, usuario in enumerate(usuarios):
            self.usuarios_text.insert(
                tk.END,
                f"Identificador: {usuario.identificador}\nNombre: {usuario.nombre}\nUsuario: {usuario.usuario}\n",
            )
            if indice < len(usuarios) - 1:
                self.usuarios_text.insert(tk.END, "-" * 72 + "\n")

    def actualizar_tabla_ventas(self):
        if not hasattr(self, "ventas_tabla"):
            return

        for fila in self.ventas_tabla.get_children():
            self.ventas_tabla.delete(fila)

        ventas = self.servicio.get_all_sales()
        for venta in ventas:
            usuario = self.servicio.buscar_usuario_por_identificador(venta.usuario_id)
            producto = self.servicio.buscar_producto_por_codigo(venta.producto_codigo)
            nombre_usuario = usuario.nombre if usuario else venta.usuario_id
            nombre_producto = producto.nombre if producto else venta.producto_codigo
            self.ventas_tabla.insert(
                "",
                "end",
                values=(venta.identificador, venta.fecha, nombre_usuario, nombre_producto),
            )
