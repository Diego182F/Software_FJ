"""Modelo de cliente con encapsulación y validaciones."""
import re
from .entidades import Entidad
from .excepciones import ValidacionError

class Cliente(Entidad):
    """Representa a una persona que contrata servicios."""

    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValidacionError("El nombre debe tener al menos tres caracteres.")
        self.__nombre = valor.strip().title()

    @property
    def correo(self):
        return self.__correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", valor.strip()
        ):
            raise ValidacionError("El correo electrónico no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono

    @telefono.setter
    def telefono(self, valor):
        digitos = re.sub(r"\D", "", str(valor))
        if len(digitos) < 7 or len(digitos) > 15:
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos.")
        self.__telefono = digitos

    def describir(self):
        return f"Cliente {self.identificador}: {self.nombre} | {self.correo} | {self.telefono}"

    def __str__(self):
        return self.describir()
