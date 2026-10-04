import tkinter as tk
from pathlib import Path

from servicios.archivo_servicio import ArchivoServicio
from servicios.restaurante_servicio import RestauranteServicio
from modelos.usuario import Usuario
from ui.login_view import LoginView
from ui.main_view import MainView


class AplicacionRestaurante:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Restaurante App - Semana 15")
        self.root.geometry("1100x650")
        self.root.minsize(850, 550)

        ruta_base = Path(__file__).resolve().parent
        archivo_servicio = ArchivoServicio(str(ruta_base / "datos"))
        self.restaurante_servicio = RestauranteServicio(archivo_servicio)

        self.vista_actual: tk.Frame | None = None
        self.mostrar_login()

    def cambiar_vista(self, nueva_vista: tk.Frame):
        if self.vista_actual is not None:
            self.vista_actual.destroy()

        self.vista_actual = nueva_vista
        self.vista_actual.pack(fill="both", expand=True)

    def mostrar_login(self):
        vista = LoginView(
            self.root,
            self.restaurante_servicio,
            self.mostrar_interfaz_principal,
        )
        self.cambiar_vista(vista)

    def mostrar_interfaz_principal(self, usuario_actual: Usuario):
        vista = MainView(
            self.root,
            self.restaurante_servicio,
            usuario_actual,
            self.mostrar_login,
        )
        self.cambiar_vista(vista)

    def ejecutar(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = AplicacionRestaurante()
    app.ejecutar()
