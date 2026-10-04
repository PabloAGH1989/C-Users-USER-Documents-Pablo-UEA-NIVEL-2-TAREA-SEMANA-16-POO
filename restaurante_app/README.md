# Restaurante App - Semana 16

Aplicación modular desarrollada con Python y Tkinter para gestionar usuarios, productos y ventas de un restaurante. Esta versión conserva la arquitectura del proyecto anterior y evoluciona la sección de usuarios para aplicar manejo de eventos, validaciones y persistencia desde un servicio centralizado.

## Objetivo de la semana

La Semana 16 se enfoca en la gestión de usuarios desde una interfaz visual con eventos de Tkinter. Se mantiene el inicio de sesión, la navegación por secciones y la gestión previa de productos y ventas, pero se incorpora la administración de usuarios con `Treeview`, `Combobox`, `bind()` y callbacks para registrar, consultar, actualizar y eliminar registros.

## Estructura del proyecto

restaurante_app/
├── datos/
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/
│   ├── __init__.py
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/
│   ├── __init__.py
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/
│   ├── __init__.py
│   ├── login_view.py
│   └── main_view.py
├── assets/
│   ├── login.png
│   ├── products.png
│   ├── users.png
│   ├── save.png
│   └── delete.png
├── main.py
├── README.md

## Funcionalidades implementadas

- Inicio de sesión con validación de credenciales.
- Navegación por secciones de Productos, Ventas y Usuarios.
- Gestión de usuarios con formulario y tabla `Treeview`.
- Atributo `rol` en el modelo `Usuario` con valores `Administrador`, `Empleado` y `Cliente`.
- Control de acceso: solo el administrador puede gestionar usuarios.
- Registro, actualización y eliminación de usuarios desde la interfaz.
- Selección de usuario desde la tabla usando `<<TreeviewSelect>>` y `bind()`.
- Uso de `Combobox` para cambiar el rol con `<<ComboboxSelected>>`.
- Acceso rápido con `Enter` para registrar usando `<Return>`.
- Limpieza del formulario con `Escape` para devolver el estado inicial.
- Persistencia de usuarios en `datos/usuarios.json`.
- Validaciones y reglas de negocio centralizadas en `RestauranteServicio`.

## Eventos y callbacks

La interacción con la interfaz se organiza siguiendo el flujo:

1. El usuario interactúa con la vista.
2. Un evento `bind()` o `command=` dispara el callback correspondiente.
3. La vista coordina la operación.
4. `RestauranteServicio` valida y persiste la información.
5. La interfaz actualiza la tabla y muestra la respuesta visual.

Ejemplos implementados:

- `<<TreeviewSelect>>` para cargar un usuario desde la tabla al formulario.
- `<Return>` para registrar usuario con el mismo método reutilizado.
- `<Escape>` para limpiar formulario y selección.
- `<<ComboboxSelected>>` para responder al cambio de rol.
- `command=` en los botones de Registrar, Actualizar, Eliminar y Limpiar.

## Persistencia

Los datos se conservan en archivos JSON. La capa de interfaz no escribe directamente en disco; todas las operaciones de negocio y almacenamiento se delegan a `ArchivoServicio` y `RestauranteServicio`.

## Ejecución

Desde la carpeta del proyecto ejecuta:

```bash
python main.py
```

## Credenciales de prueba

- Usuario: admin
- Contraseña: 1234

## Observación

La aplicación mantiene la modularidad y continuidad del proyecto anterior, ampliando la gestión de usuarios con una solución basada en eventos, roles y persistencia para la Semana 16.
