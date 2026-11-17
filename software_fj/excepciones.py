"""Excepciones personalizadas del sistema Software FJ."""

class SoftwareFJError(Exception):
    """Excepción base para los errores controlados de la aplicación."""

class ValidacionError(SoftwareFJError):
    """Se genera cuando un dato no cumple las reglas de validación."""

class ClienteDuplicadoError(SoftwareFJError):
    """Se genera cuando se intenta registrar un cliente ya existente."""

class ServicioNoDisponibleError(SoftwareFJError):
    """Se genera cuando un servicio no tiene disponibilidad suficiente."""

class ReservaError(SoftwareFJError):
    """Se genera cuando una operación de reserva no está permitida."""

class EstadoReservaError(ReservaError):
    """Se genera cuando se intenta operar sobre un estado no permitido."""
