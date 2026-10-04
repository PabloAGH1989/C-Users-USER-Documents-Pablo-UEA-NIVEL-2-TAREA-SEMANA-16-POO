class Usuario:
    def __init__(self, identificador: str, nombre: str, usuario: str, contraseña: str, rol: str = "Cliente"):
        self.identificador = identificador
        self.nombre = nombre
        self.usuario = usuario
        self.contraseña = contraseña
        self.rol = rol

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
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str):
        self._nombre = self.validar_texto(valor, "nombre")

    @property
    def usuario(self) -> str:
        return self._usuario

    @usuario.setter
    def usuario(self, valor: str):
        self._usuario = self.validar_texto(valor, "usuario")

    @property
    def contraseña(self) -> str:
        return self._contraseña

    @contraseña.setter
    def contraseña(self, valor: str):
        self._contraseña = self.validar_texto(valor, "contraseña")

    @property
    def rol(self) -> str:
        return self._rol

    @rol.setter
    def rol(self, valor: str):
        rol_normalizado = self.validar_texto(valor, "rol").title()
        roles_permitidos = {"Administrador", "Empleado", "Cliente"}
        if rol_normalizado not in roles_permitidos:
            raise ValueError("El rol debe ser Administrador, Empleado o Cliente.")
        self._rol = rol_normalizado