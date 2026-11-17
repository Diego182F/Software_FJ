
"""Gestión del ciclo de vida de una reserva."""

from enum import Enum
from .entidades import Entidad
from .excepciones import EstadoReservaError, ReservaError


class EstadoReserva(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADA = "Confirmada"
    CANCELADA = "Cancelada"
    PROCESADA = "Procesada"


class Reserva(Entidad):
    """Relaciona un cliente con un servicio y controla su estado."""

    def __init__(
        self,
        identificador,
        cliente,
        servicio,
        cantidad,
        impuesto=0.19,
        descuento=0.0
    ):
        super().__init__(identificador)

        from .cliente import Cliente
        from .servicio import Servicio

        if not isinstance(cliente, Cliente):
            raise ReservaError(
                "La reserva requiere un objeto Cliente válido."
            )

        if not isinstance(servicio, Servicio):
            raise ReservaError(
                "La reserva requiere un objeto Servicio válido."
            )

        servicio.validar_parametros(cantidad)

        self.cliente = cliente
        self.servicio = servicio
        self.cantidad = cantidad
        self.impuesto = impuesto
        self.descuento = descuento

        self.estado = EstadoReserva.PENDIENTE
        self.costo = None
        self._recurso_separado = False

    def confirmar(self):
        """Confirma la reserva si existe disponibilidad."""

        if self.estado is not EstadoReserva.PENDIENTE:
            raise EstadoReservaError(
                "Solo se pueden confirmar reservas pendientes."
            )

        # La cantidad de recursos depende del tipo de servicio.
        cantidad_recursos = (
            self.cantidad
            if self.servicio.__class__.__name__ == "AlquilerEquipo"
            else 1
        )

        # Si no hay disponibilidad, se genera ServicioNoDisponibleError.
        # El estado permanece pendiente si ocurre la excepción.
        self.servicio.reservar_recurso(cantidad_recursos)

        self._recurso_separado = True
        self.estado = EstadoReserva.CONFIRMADA

        return self

    def cancelar(self):
        """Cancela la reserva y libera los recursos separados."""

        if self.estado not in (
            EstadoReserva.PENDIENTE,
            EstadoReserva.CONFIRMADA
        ):
            raise EstadoReservaError(
                "La reserva no se puede cancelar en su estado actual."
            )

        if self._recurso_separado:
            cantidad_recursos = (
                self.cantidad
                if self.servicio.__class__.__name__ == "AlquilerEquipo"
                else 1
            )

            self.servicio.liberar_recurso(cantidad_recursos)
            self._recurso_separado = False

        self.estado = EstadoReserva.CANCELADA

        return self

    def procesar(self):
        """Calcula el costo y cambia el estado a procesada."""

        if self.estado is not EstadoReserva.CONFIRMADA:
            raise EstadoReservaError(
                "Solo se pueden procesar reservas confirmadas."
            )

        try:
            self.costo = self.servicio.calcular_costo(
                self.cantidad,
                self.impuesto,
                self.descuento
            )

        except Exception as error:
            raise ReservaError(
                "No fue posible calcular el costo de la reserva."
            ) from error

        self.estado = EstadoReserva.PROCESADA

        return self.costo

    def describir(self):
        """Devuelve la información completa de la reserva."""

        costo = (
            f"${self.costo:.2f}"
            if self.costo is not None
            else "Pendiente de cálculo"
        )

        return (
            f"Reserva {self.identificador} | "
            f"Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | "
            f"Cantidad: {self.cantidad} | "
            f"Estado: {self.estado.value} | "
            f"Costo: {costo}"
        )
