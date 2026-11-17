"""Define la abstracción común de las entidades del sistema."""
from abc import ABC, abstractmethod
from datetime import datetime

class Entidad(ABC):
    """Clase abstracta base para las entidades identificables."""

    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador es obligatorio.")
        self._identificador = identificador.strip()
        self._fecha_creacion = datetime.now()

    @property
    def identificador(self):
        """Devuelve el identificador sin permitir su modificación directa."""
        return self._identificador

    @property
    def fecha_creacion(self):
        """Devuelve la fecha de creación."""
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Obliga a las clases concretas a describir la entidad."""
        raise NotImplementedError
