class Producto:
    def __init__(self, codigo: str, nombre: str, precio: float | str):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio

    @staticmethod
    def validar_texto(valor: str, campo: str) -> str:
        if not valor or not valor.strip():
            raise ValueError(f"El campo {campo} no puede estar vacio.")

        return valor.strip()

    @property
    def codigo(self) -> str:
        return self._codigo

    @codigo.setter
    def codigo(self, valor: str):
        self._codigo = self.validar_texto(valor, "codigo")

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def precio(self) -> float:
        return self._precio

    @precio.setter
    def precio(self, valor: float | str):
        if valor == "":
            raise ValueError("El campo precio no puede estar vacio.")

        try:
            self._precio = float(valor)
        except (TypeError, ValueError):
            raise ValueError("El campo precio debe ser un numero valido.")

