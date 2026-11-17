"""Pruebas unitarias básicas del sistema Software FJ."""
import unittest
import logging
from software_fj.cliente import Cliente
from software_fj.servicio import ReservaSala, AlquilerEquipo
from software_fj.reserva import Reserva, EstadoReserva
from software_fj.gestor import GestorSoftwareFJ
from software_fj.excepciones import ValidacionError, EstadoReservaError

class SistemaFJTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("test_software_fj")
        self.gestor = GestorSoftwareFJ(self.logger)
        self.cliente = Cliente("C100", "Ana Torres", "ana@example.com", "3105551234")
        self.sala = ReservaSala("S100", "Sala principal", 60000, 2, 10)

    def test_cliente_valido(self):
        self.assertEqual(self.cliente.correo, "ana@example.com")

    def test_correo_invalido(self):
        with self.assertRaises(ValidacionError):
            Cliente("C101", "Ana Torres", "correo", "3105551234")

    def test_costo_con_impuesto_descuento(self):
        self.assertEqual(self.sala.calcular_costo(2, 0.19, 0.10), 128520.0)

    def test_confirmar_y_procesar_reserva(self):
        reserva = Reserva("R100", self.cliente, self.sala, 2)
        reserva.confirmar()
        costo = reserva.procesar()
        self.assertEqual(reserva.estado, EstadoReserva.PROCESADA)
        self.assertEqual(costo, 142800.0)

    def test_no_procesar_pendiente(self):
        reserva = Reserva("R101", self.cliente, self.sala, 1)
        with self.assertRaises(EstadoReservaError):
            reserva.procesar()

    def test_disponibilidad(self):
        equipo = AlquilerEquipo("E100", "Portátil", 40000, 1)
        equipo.reservar_recurso()
        with self.assertRaises(Exception):
            equipo.reservar_recurso()

if __name__ == "__main__":
    unittest.main()
