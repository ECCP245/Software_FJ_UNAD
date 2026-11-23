# Proyecto base de Evelyn Carolina Calvache Pabón.
# Aporte local de Yeison Andrés Bran Henao: excepciones y simulaciones independientes.

# Importa el registro de eventos y el manejo de rutas de archivos.
import logging
import os
# César: excepción para comprobar referencias necesarias antes de utilizarlas.
from exceptions import ServiceNotAvailableFJError
# Importa las clases originales, con las correcciones del aporte.
from models import Client, RoomReservationService, EquipmentRentalService
from models import SpecializedConsultingService, Reservation


# Muestra y registra las operaciones que terminaron correctamente.
def registrar_exito(numero, mensaje):
    print(f"[Simulacion {numero:02d}] OK: {mensaje}")
    logging.info(f"Simulacion {numero:02d}: {mensaje}")


# Registra el error y su causa sin detener las siguientes simulaciones.
def registrar_error(numero, error):
    print(f"[Simulacion {numero:02d}] ERROR CONTROLADO: {error}")
    # exc_info conserva la información completa, incluido raise ... from ... .
    logging.error(f"Simulacion {numero:02d}: {error}", exc_info=True)


# Ejecuta el programa solamente cuando se abre este archivo directamente.
if __name__ == "__main__":
    # Ubica el log junto a los archivos del proyecto.
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_log = os.path.join(carpeta, "fj_software_exceptions.log")
    # Conserva los eventos y errores de cada ejecución.
    logging.basicConfig(filename=ruta_log, level=logging.INFO, encoding="utf-8",
                        format="%(asctime)s - [%(levelname)s] - %(message)s")
    # Anuncia el inicio de la ejecución.
    print("SOFTWARE FJ - 16 SIMULACIONES\n")
    logging.info("Inicio de las 16 simulaciones.")
    # Las listas guardan solamente los objetos creados correctamente.
    clients_list = []
    services_list = []
    reservations_list = []
    # Inicializa las referencias utilizadas en operaciones posteriores.
    c1 = None
    s1 = None
    s2 = None
    s3 = None
    r1 = None

    # Simulación 1: registra un cliente con datos correctos.
    try:
        c1 = Client("C001", "Carlos Gomez", "carlos.gomez@softwarefj.com")
        clients_list.append(c1)
    except Exception as error:
        registrar_error(1, error)
    else:
        registrar_exito(1, c1.get_details())

    # Simulación 2: rechaza el correo inválido y continúa con la simulación 3.
    try:
        c2 = Client("C002", "Ana Perez", "correo_invalido")
        clients_list.append(c2)
    except Exception as error:
        registrar_error(2, error)
    else:
        registrar_exito(2, c2.get_details())

    # Simulación 3: rechaza un nombre vacío.
    try:
        c3 = Client("C003", "   ", "cliente@softwarefj.com")
        clients_list.append(c3)
    except Exception as error:
        registrar_error(3, error)
    else:
        registrar_exito(3, c3.get_details())

    # Simulación 4: crea correctamente un servicio de sala.
    try:
        s1 = RoomReservationService("SR01", 200.0, 15)
        services_list.append(s1)
    except Exception as error:
        registrar_error(4, error)
    else:
        registrar_exito(4, s1.describe_service())

    # Simulación 5: crea correctamente un servicio de equipos.
    try:
        s2 = EquipmentRentalService("SE01", 45.0, "Workstation PC")
        services_list.append(s2)
    except Exception as error:
        registrar_error(5, error)
    else:
        registrar_exito(5, s2.describe_service())

    # Simulación 6: crea correctamente un servicio de asesoría.
    try:
        s3 = SpecializedConsultingService("SC01", 350.0, "Cloud Migration")
        services_list.append(s3)
    except Exception as error:
        registrar_error(6, error)
    else:
        registrar_exito(6, s3.describe_service())

    # Simulación 7: rechaza un servicio con costo negativo.
    try:
        servicio_invalido = RoomReservationService("SR02", -200.0, 15)
        services_list.append(servicio_invalido)
    except Exception as error:
        registrar_error(7, error)
    else:
        registrar_exito(7, servicio_invalido.describe_service())

    # Simulación 8: confirma una reserva y ejecuta su bloque else.
    try:
        # César: comprueba las referencias antes de reservar.
        if c1 is None or s1 is None:
            raise ServiceNotAvailableFJError("Cliente o servicio de sala no disponible.")
        r1 = Reservation("R101", c1, s1, 3)
        mensaje = r1.confirm_reservation()
        reservations_list.append(r1)
    except Exception as error:
        registrar_error(8, error)
    else:
        registrar_exito(8, mensaje)

    # Simulación 9: una duración cero produce una excepción encadenada.
    try:
        # César: comprueba que existan cliente y servicio de equipos.
        if c1 is None or s2 is None:
            raise ServiceNotAvailableFJError("Cliente o servicio de equipo no disponible.")
        r2 = Reservation("R102", c1, s2, 0)
        mensaje = r2.confirm_reservation()
        reservations_list.append(r2)
    except Exception as error:
        registrar_error(9, error)
    else:
        registrar_exito(9, mensaje)

    # Simulación 10: controla la reserva de un servicio inexistente.
    try:
        r3 = Reservation("R103", c1, None, 2)
        mensaje = r3.confirm_reservation()
        reservations_list.append(r3)
    except Exception as error:
        registrar_error(10, error)
    else:
        registrar_exito(10, mensaje)

    # Simulación 11: calcula el costo de sala con los parámetros opcionales.
    try:
        # César: evita utilizar un servicio que no pudo crearse.
        if s1 is None:
            raise ServiceNotAvailableFJError("Servicio de sala no disponible.")
        costo_sala = s1.calculate_cost(discount=0.15, tax=0.19)
    except Exception as error:
        registrar_error(11, error)
    else:
        registrar_exito(11, f"Room cost with discount and tax: {costo_sala:.2f}")

    # Simulación 12: rechaza horas negativas sin devolver un costo alternativo.
    try:
        costo_equipo = s2.calculate_cost(hours=-2)
    except Exception as error:
        registrar_error(12, error)
    else:
        registrar_exito(12, f"Equipment cost: {costo_equipo:.2f}")

    # Simulación 13: cancela la reserva confirmada en la simulación 8.
    try:
        mensaje = r1.cancel_reservation()
    except Exception as error:
        registrar_error(13, error)
    else:
        registrar_exito(13, mensaje)

    # Simulación 14: calcula el alquiler de equipos después de un error anterior.
    try:
        # César: comprueba que el servicio de equipos exista.
        if s2 is None:
            raise ServiceNotAvailableFJError("Servicio de equipos no disponible.")
        costo_equipo = s2.calculate_cost(hours=5, insurance_fee=15.0)
    except Exception as error:
        registrar_error(14, error)
    else:
        registrar_exito(14, f"Equipment cost for 5 hours: {costo_equipo:.2f}")

    # Simulación 15: demuestra que también se controla un TypeError de Python.
    try:
        # La ausencia de nombre y correo es intencional en este caso de prueba.
        cliente_incompleto = Client("C004")
        clients_list.append(cliente_incompleto)
    except Exception as error:
        registrar_error(15, error)
    else:
        registrar_exito(15, cliente_incompleto.get_details())

    # Simulación 16: confirma que el programa continúa después del TypeError.
    try:
        costo_asesoria = s3.calculate_cost(complexity_factor=1.5)
    except Exception as error:
        registrar_error(16, error)
    else:
        registrar_exito(16, f"Consulting cost: {costo_asesoria:.2f}")

    # El cierre indica operaciones procesadas, no que todos los datos eran válidos.
    print("\nFIN: se procesaron las 16 simulaciones, incluidos los errores de prueba.")
    print(f"Clientes válidos: {len(clients_list)}")
    print(f"Servicios válidos: {len(services_list)}")
    print(f"Reservas confirmadas registradas (incluye canceladas después): {len(reservations_list)}")
    print("Consulte fj_software_exceptions.log para revisar los detalles.")
    logging.info("Fin de las 16 simulaciones.")
