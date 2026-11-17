"""Capa de aplicación: administra las listas en memoria."""
from .excepciones import ClienteDuplicadoError, ValidacionError
from .cliente import Cliente
from .servicio import Servicio
from .reserva import Reserva

class GestorSoftwareFJ:
    """Centraliza clientes, servicios y reservas sin utilizar bases de datos."""

    def __init__(self, logger):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        self.logger = logger

    def registrar_cliente(self, cliente):
        if not isinstance(cliente, Cliente):
            raise ValidacionError("El objeto recibido no es un cliente.")
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteDuplicadoError(f"Ya existe el cliente {cliente.identificador}.")
        self.clientes.append(cliente)
        self.logger.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ValidacionError("El objeto recibido no es un servicio válido.")
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ValidacionError(f"Ya existe el servicio {servicio.identificador}.")
        self.servicios.append(servicio)
        self.logger.info("Servicio agregado: %s", servicio.identificador)
        return servicio

    def crear_reserva(self, reserva):
        if not isinstance(reserva, Reserva):
            raise ValidacionError("El objeto recibido no es una reserva.")
        if any(r.identificador == reserva.identificador for r in self.reservas):
            raise ValidacionError(f"Ya existe la reserva {reserva.identificador}.")
        self.reservas.append(reserva)
        self.logger.info("Reserva creada: %s", reserva.identificador)
        return reserva

    def buscar_cliente(self, identificador):
        return next((c for c in self.clientes if c.identificador == identificador), None)

    def buscar_servicio(self, identificador):
        return next((s for s in self.servicios if s.identificador == identificador), None)

    def listar_reservas(self):
        return [r.describir() for r in self.reservas]
