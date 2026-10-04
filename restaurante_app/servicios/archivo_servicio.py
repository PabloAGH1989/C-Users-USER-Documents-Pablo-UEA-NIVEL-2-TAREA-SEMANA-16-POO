import json
from pathlib import Path
from typing import Any, cast

from modelos.producto import Producto


class ArchivoServicio:
    def __init__(self, carpeta_datos: str | Path):
        self.carpeta_datos = Path(carpeta_datos)
        self.carpeta_datos.mkdir(parents=True, exist_ok=True)

    def leer_json(self, nombre_archivo: str) -> list[dict[str, Any]]:
        ruta = self.carpeta_datos / nombre_archivo

        if not ruta.exists():
            return []

        with ruta.open("r", encoding="utf-8") as archivo:
            datos: Any = json.load(archivo)
            if isinstance(datos, list):
                return [
                    cast(dict[str, Any], dato)
                    for dato in cast(list[Any], datos)
                    if isinstance(dato, dict)
                ]
            return [datos] if isinstance(datos, dict) else []

    def escribir_json(self, nombre_archivo: str, datos: list[dict[str, Any]]) -> None:
        ruta = self.carpeta_datos / nombre_archivo
        ruta.parent.mkdir(parents=True, exist_ok=True)

        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump(datos, archivo, indent=4, ensure_ascii=False)

    def read_json(self, nombre_archivo: str) -> list[dict[str, Any]]:
        return self.leer_json(nombre_archivo)

    def guardar_producto(self, producto: Producto, nombre_archivo: str = "productos.json") -> None:
        productos = self.read_json(nombre_archivo)
        productos.append(
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
            }
        )
        self.escribir_json(nombre_archivo, productos)

    def guardar_productos(self, productos: list[Producto], nombre_archivo: str = "productos.json") -> None:
        registros: list[dict[str, Any]] = [
            {
                "codigo": producto.codigo,
                "nombre": producto.nombre,
                "precio": producto.precio,
            }
            for producto in productos
        ]
        self.escribir_json(nombre_archivo, registros)

    def guardar_usuarios(self, usuarios: list[dict[str, Any]], nombre_archivo: str = "usuarios.json") -> None:
        self.escribir_json(nombre_archivo, usuarios)

    def guardar_ventas(self, ventas: list[dict[str, Any]], nombre_archivo: str = "ventas.json") -> None:
        self.escribir_json(nombre_archivo, ventas)

    def obtener_productos(self, nombre_archivo: str = "productos.json") -> list[Producto]:
        productos_data = self.read_json(nombre_archivo)
        return [
            Producto(
                dato.get("codigo", dato.get("id", "")),
                dato.get("nombre", ""),
                dato.get("precio", 0),
            )
            for dato in productos_data
        ]

    def read_json_usuarios(self) -> list[dict[str, Any]]:
        return self.leer_json("usuarios.json")