"""Clase abstracta y servicios especializados."""
from abc import abstractmethod
from .entidades import Entidad
from .excepciones import ValidacionError, ServicioNoDisponibleError

class Servicio(Entidad):
    """Contrato común de todos los servicios ofrecidos por Software FJ."""

    def __init__(self, identificador, nombre, tarifa, disponibles):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa, bool) or not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise ValidacionError("La tarifa debe ser un número positivo.")
        if isinstance(disponibles, bool) or not isinstance(disponibles, int) or disponibles < 0:
            raise ValidacionError("La disponibilidad debe ser un entero no negativo.")
        self.nombre = nombre.strip()
        self.tarifa = float(tarifa)
        self._disponibles = disponibles

    @property
    def disponibles(self):
        return self._disponibles

    def reservar_recurso(self, cantidad=1):
        self.validar_parametros(cantidad)
        if cantidad > self._disponibles:
            raise ServicioNoDisponibleError(
                f"{self.nombre}: disponibles {self._disponibles}, solicitados {cantidad}."
            )
        self._disponibles -= cantidad

    def liberar_recurso(self, cantidad=1):
        if not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidacionError("La cantidad a liberar debe ser un entero positivo.")
        self._disponibles += cantidad

    @abstractmethod
    def validar_parametros(self, cantidad):
        """Valida el parámetro específico de cada servicio."""

    @abstractmethod
    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0):
        """Calcula el costo; los argumentos opcionales simulan sobrecarga."""

    @abstractmethod
    def describir(self):
        """Devuelve la descripción particular del servicio."""

class ReservaSala(Servicio):
    """Servicio de alquiler de salas por hora."""

    def __init__(self, identificador, nombre, tarifa_hora, salas_disponibles, capacidad):
        super().__init__(identificador, nombre, tarifa_hora, salas_disponibles)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionError("La capacidad de la sala debe ser positiva.")
        self.capacidad = capacidad

    def validar_parametros(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValidacionError("Las horas reservadas deben ser mayores que cero.")

    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0):
        self.validar_parametros(cantidad)
        _validar_ajustes(impuesto, descuento)
        subtotal = self.tarifa * cantidad
        return round(subtotal * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Sala '{self.nombre}': ${self.tarifa:.2f}/hora, capacidad {self.capacidad}, salas disponibles {self.disponibles}."

class AlquilerEquipo(Servicio):
    """Servicio de alquiler de equipos por día y unidades."""

    def validar_parametros(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise ValidacionError("La cantidad de equipos debe ser un entero positivo.")

    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0):
        self.validar_parametros(cantidad)
        _validar_ajustes(impuesto, descuento)
        return round(self.tarifa * cantidad * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Equipo '{self.nombre}': ${self.tarifa:.2f}/día por unidad, unidades disponibles {self.disponibles}."

class AsesoriaEspecializada(Servicio):
    """Servicio de asesoría profesional cobrado por hora."""

    def __init__(self, identificador, nombre, tarifa_hora, asesores_disponibles, especialidad):
        super().__init__(identificador, nombre, tarifa_hora, asesores_disponibles)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError("La especialidad es obligatoria.")
        self.especialidad = especialidad.strip()

    def validar_parametros(self, cantidad):
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValidacionError("Las horas de asesoría deben ser mayores que cero.")

    def calcular_costo(self, cantidad, impuesto=0.0, descuento=0.0):
        self.validar_parametros(cantidad)
        _validar_ajustes(impuesto, descuento)
        return round(self.tarifa * cantidad * (1 + impuesto) * (1 - descuento), 2)

    def describir(self):
        return f"Asesoría '{self.nombre}' ({self.especialidad}): ${self.tarifa:.2f}/hora, asesores disponibles {self.disponibles}."

def _validar_ajustes(impuesto, descuento):
    """Valida tasas expresadas como proporciones: 0.19 equivale al 19 %."""
    for nombre, valor in (("impuesto", impuesto), ("descuento", descuento)):
        if isinstance(valor, bool) or not isinstance(valor, (int, float)) or not 0 <= valor <= 1:
            raise ValidacionError(f"El {nombre} debe estar entre 0 y 1.")
