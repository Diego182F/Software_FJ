"""Punto de entrada: demostración secuencial de más de diez operaciones."""
import logging
from software_fj.registro import configurar_logger
from software_fj.gestor import GestorSoftwareFJ
from software_fj.cliente import Cliente
from software_fj.servicio import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from software_fj.reserva import Reserva
from software_fj.excepciones import SoftwareFJError

def ejecutar_operacion(nombre, funcion, logger):
    """Ejecuta una operación aislada para evitar que un error detenga el sistema."""
    print(f"\\n--- {nombre} ---")
    try:
        resultado = funcion()
    except SoftwareFJError as error:
        logger.exception("Error controlado en '%s': %s", nombre, error)
        print(f"[ERROR CONTROLADO] {error}")
    except (TypeError, ValueError) as error:
        logger.exception("Error de datos en '%s': %s", nombre, error)
        print(f"[ERROR DE DATOS] {error}")
    except Exception as error:
        logger.exception("Error inesperado en '%s': %s", nombre, error)
        print("[ERROR INESPERADO] La operación falló, pero el sistema continúa.")
    else:
        logger.info("Operación exitosa: %s", nombre)
        print(resultado if resultado is not None else "Operación realizada correctamente.")
    finally:
        print("[FIN] Operación finalizada.")

def main():
    logger = configurar_logger()
    gestor = GestorSoftwareFJ(logger)
    logger.info("Inicio de Software FJ.")

    # Operaciones 1 y 2: registro correcto e inválido de clientes.
    ejecutar_operacion("1. Registrar cliente válido", lambda: gestor.registrar_cliente(
        Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")), logger)

    ejecutar_operacion("2. Registrar cliente con correo inválido", lambda: Cliente(
        "C002", "Carlos Pérez", "correo_incorrecto", "3001234568"), logger)

    # Operación 3: detección de cliente duplicado.
    ejecutar_operacion("3. Intentar registrar cliente duplicado", lambda: gestor.registrar_cliente(
        Cliente("C001", "Laura Gómez", "laura@gmail.com", "3001234567")), logger)

    # Operaciones 4, 5 y 6: creación de servicios.
    sala = ReservaSala("S001", "Sala de juntas", 80000, 2, 12)
    equipo = AlquilerEquipo("E001", "Proyector HD", 50000, 5)
    asesoria = AsesoriaEspecializada("A001", "Consultoría Python", 100000, 3, "Desarrollo de software")

    ejecutar_operacion("4. Crear servicio de sala", lambda: gestor.agregar_servicio(sala), logger)
    ejecutar_operacion("5. Crear servicio de alquiler de equipos", lambda: gestor.agregar_servicio(equipo), logger)
    ejecutar_operacion("6. Crear servicio de asesoría", lambda: gestor.agregar_servicio(asesoria), logger)

    ejecutar_operacion("7. Intentar crear servicio con tarifa inválida", lambda: ReservaSala(
        "S002", "Sala inválida", -5000, 1, 10), logger)

    # Operaciones 8, 9 y 10: reservas correctas y cálculo polimórfico.
    cliente = gestor.buscar_cliente("C001")
    reserva_sala = Reserva("R001", cliente, sala, 3, impuesto=0.19, descuento=0.10)
    ejecutar_operacion("8. Crear reserva de sala", lambda: gestor.crear_reserva(reserva_sala), logger)
    ejecutar_operacion("9. Confirmar reserva", lambda: reserva_sala.confirmar(), logger)
    ejecutar_operacion("10. Procesar reserva y calcular costo", lambda: reserva_sala.procesar(), logger)

   
    # Operación 11: intentar confirmar una reserva sin disponibilidad.

    servicio_agotado = AlquilerEquipo(
        "E002",
        "Proyector de prueba",
        50000,
        0
    )

    reserva_fallida = Reserva(
        "R002",
        cliente,
        servicio_agotado,
        1
    )

    ejecutar_operacion(
        "11. Intentar confirmar reserva sin disponibilidad",
        lambda: reserva_fallida.confirmar(),
        logger
    )

    # Operación 12: intentar procesar una reserva pendiente.
    reserva_pendiente = Reserva("R003", cliente, equipo, 2)

    ejecutar_operacion(
        "12. Procesar reserva no confirmada",
        lambda: reserva_pendiente.procesar(),
        logger
    )

    # Operación 13: cancelar una reserva pendiente.
    ejecutar_operacion(
        "13. Cancelar reserva pendiente",
        lambda: reserva_pendiente.cancelar(),
        logger
    )

    # Operación 14: cálculo de asesoría con impuesto y descuento.
    ejecutar_operacion("14. Calcular asesoría con impuesto y descuento", lambda: asesoria.calcular_costo(
        2, impuesto=0.19, descuento=0.05), logger)

    # Operación 15: mostrar resumen.
    ejecutar_operacion("15. Consultar reservas", lambda: "\\n".join(gestor.listar_reservas()), logger)

    logger.info("Fin de demostración. Clientes=%d, servicios=%d, reservas=%d",
                len(gestor.clientes), len(gestor.servicios), len(gestor.reservas))
    print("\\nSistema Software FJ finalizado. Consulte logs/software_fj.log.")

if __name__ == "__main__":
    main()
