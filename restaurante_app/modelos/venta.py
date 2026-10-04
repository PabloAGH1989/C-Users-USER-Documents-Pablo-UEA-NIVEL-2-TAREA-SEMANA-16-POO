from datetime import date


class Venta:
    def __init__(self, identificador: str, usuario_id: str, producto_codigo: str, fecha: str | None = None):
        self.identificador = identificador
        self.usuario_id = usuario_id
        self.producto_codigo = producto_codigo
        self.fecha = fecha or date.today().isoformat()

    @staticmethod
    def validar_texto(valor: str, campo: str) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return valor.strip()

    @property
    def identificador(self) -> str:
        return self._identificador

    @identificador.setter
    def identificador(self, valor: str):
        self._identificador = self.validar_texto(valor, "identificador")

    @property
    def usuario_id(self) -> str:
        return self._usuario_id

    @usuario_id.setter
    def usuario_id(self, valor: str):
        self._usuario_id = self.validar_texto(valor, "usuario")

    @property
    def producto_codigo(self) -> str:
        return self._producto_codigo

    @producto_codigo.setter
    def producto_codigo(self, valor: str):
        self._producto_codigo = self.validar_texto(valor, "producto")

    @property
    def fecha(self) -> str:
        return self._fecha

    @fecha.setter
    def fecha(self, valor: str):
        self._fecha = self.validar_texto(valor, "fecha")
