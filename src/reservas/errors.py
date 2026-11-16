class ReglaError(Exception):
    def __init__(self, codigo: str, mensaje: str):
        self.codigo = codigo
        self.mensaje = mensaje
        super().__init__(mensaje)


class PermisoError(Exception):
    def __init__(self, mensaje: str = "No tiene permiso para esta acción"):
        self.mensaje = mensaje
        super().__init__(mensaje)
