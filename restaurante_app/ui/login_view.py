import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from typing import Callable

from modelos.usuario import Usuario
from servicios.restaurante_servicio import RestauranteServicio


class LoginView(tk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        servicio: RestauranteServicio,
        callback: Callable[[Usuario], None],
    ):
        super().__init__(master, bg="#dfeaf7")
        self.servicio = servicio
        self.callback = callback
        ruta_assets = Path(__file__).resolve().parents[1] / "assets"
        self.imagen_logo = tk.PhotoImage(file=str(ruta_assets / "login.png")).subsample(2, 2)
        self.crear_widgets()

    def crear_widgets(self):
        contenedor = tk.Frame(self, bg="#ffffff", padx=26, pady=24)
        contenedor.place(relx=0.5, rely=0.5, anchor="center")

        logo = tk.Label(contenedor, image=self.imagen_logo, bg="#ffffff")
        logo.pack(pady=(0, 10))

        tk.Label(
            contenedor,
            text="Restaurante App",
            font=("Arial", 22, "bold"),
            bg="#ffffff",
            fg="#243b53",
        ).pack(pady=(0, 18))

        tk.Label(contenedor, text="Usuario", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w")
        self.entry_usuario = tk.Entry(contenedor, width=32, font=("Arial", 11))
        self.entry_usuario.pack(pady=(6, 12))
        self.entry_usuario.bind("<Return>", lambda _: self.validar_credenciales())

        tk.Label(contenedor, text="Contraseña", bg="#ffffff", font=("Arial", 11, "bold")).pack(anchor="w")
        self.entry_password = tk.Entry(contenedor, width=32, show="*", font=("Arial", 11))
        self.entry_password.pack(pady=(6, 18))
        self.entry_password.bind("<Return>", lambda _: self.validar_credenciales())

        tk.Button(
            contenedor,
            text="Ingresar",
            width=22,
            height=2,
            bg="#2d7ff9",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.validar_credenciales,
        ).pack()

    def validar_credenciales(self):
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Validación", "Debe ingresar usuario y contraseña.")
            return

        usuario_validado: Usuario | None = self.servicio.validar_login(usuario, password)
        if usuario_validado is None:
            messagebox.showerror("Error", "Credenciales incorrectas.")
            return

        self.callback(usuario_validado)
