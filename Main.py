# Proyecto base de Evelyn Carolina Calvache Pabón.
# Aporte local de Yeison Andrés Bran Henao: excepciones y simulaciones independientes.

# Importa el registro de eventos y el manejo de rutas de archivos.
import logging
import os  # Importa las herramientas usadas en este módulo.
# César: comprobación de referencias antes de usar un servicio.
from exceptions import ServiceNotAvailableFJError
# Importa las clases originales, con las correcciones del aporte.
from models import Client, RoomReservationService, EquipmentRentalService
from models import SpecializedConsultingService, Reservation  # Importa las herramientas usadas en este módulo.


# Muestra y registra las operaciones que terminaron correctamente.
def registrar_exito(numero, mensaje):
    print(f"[Simulacion {numero:02d}] OK: {mensaje}")  # Muestra el resultado en la consola.
    logging.info(f"Simulacion {numero:02d}: {mensaje}")  # Escribe el evento o el error en el registro.


# Registra el error y su causa sin detener las siguientes simulaciones.
def registrar_error(numero, error):
    print(f"[Simulacion {numero:02d}] ERROR CONTROLADO: {error}")  # Muestra el resultado en la consola.
    # exc_info conserva la información completa, incluido raise ... from ... .
    logging.error(f"Simulacion {numero:02d}: {error}", exc_info=True)


# Ejecuta el programa solamente cuando se abre este archivo directamente.
if __name__ == "__main__":
    # Ubica el log junto a los archivos del proyecto.
    carpeta = os.path.dirname(os.path.abspath(__file__))
    ruta_log = os.path.join(carpeta, "fj_software_exceptions.log")  # Guarda el dato o el resultado para usarlo después.
    # Conserva los eventos y errores de cada ejecución.
    logging.basicConfig(filename=ruta_log, level=logging.INFO, encoding="utf-8",
                        format="%(asctime)s - [%(levelname)s] - %(message)s")  # Guarda el dato o el resultado para usarlo después.
    # Anuncia el inicio de la ejecución.
    print("SOFTWARE FJ - 22 SIMULACIONES\n")
    logging.info("Inicio de las 22 simulaciones.")  # Escribe el evento o el error en el registro.
    # Las listas guardan solamente los objetos creados correctamente.
    clients_list = []
    services_list = []  # Guarda el dato o el resultado para usarlo después.
    reservations_list = []  # Guarda el dato o el resultado para usarlo después.
    # Inicializa las referencias utilizadas en operaciones posteriores.
    c1 = None
    s1 = None  # Guarda el dato o el resultado para usarlo después.
    s2 = None  # Guarda el dato o el resultado para usarlo después.
    s3 = None  # Guarda el dato o el resultado para usarlo después.
    r1 = None  # Guarda el dato o el resultado para usarlo después.

    # Simulación 1: registra un cliente con datos correctos.
    try:
        c1 = Client("C001", "Carlos Gomez", "carlos.gomez@softwarefj.com")  # Guarda el dato o el resultado para usarlo después.
        clients_list.append(c1)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(1, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(1, c1.get_details())  # Muestra y registra la operación válida.

    # Simulación 2: rechaza el correo inválido y continúa con la simulación 3.
    try:
        c2 = Client("C002", "Ana Perez", "correo_invalido")  # Guarda el dato o el resultado para usarlo después.
        clients_list.append(c2)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(2, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(2, c2.get_details())  # Muestra y registra la operación válida.

    # Simulación 3: rechaza un nombre vacío.
    try:
        c3 = Client("C003", "   ", "cliente@softwarefj.com")  # Guarda el dato o el resultado para usarlo después.
        clients_list.append(c3)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(3, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(3, c3.get_details())  # Muestra y registra la operación válida.

    # Simulación 4: crea correctamente un servicio de sala.
    try:
        s1 = RoomReservationService("SR01", 200.0, 15)  # Guarda el dato o el resultado para usarlo después.
        services_list.append(s1)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(4, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(4, s1.describe_service())  # Muestra y registra la operación válida.

    # Simulación 5: crea correctamente un servicio de equipos.
    try:
        s2 = EquipmentRentalService("SE01", 45.0, "Workstation PC")  # Guarda el dato o el resultado para usarlo después.
        services_list.append(s2)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(5, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(5, s2.describe_service())  # Muestra y registra la operación válida.

    # Simulación 6: crea correctamente un servicio de asesoría.
    try:
        s3 = SpecializedConsultingService("SC01", 350.0, "Cloud Migration")  # Guarda el dato o el resultado para usarlo después.
        services_list.append(s3)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(6, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(6, s3.describe_service())  # Muestra y registra la operación válida.

    # Simulación 7: rechaza un servicio con costo negativo.
    try:
        servicio_invalido = RoomReservationService("SR02", -200.0, 15)  # Guarda el dato o el resultado para usarlo después.
        services_list.append(servicio_invalido)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(7, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(7, servicio_invalido.describe_service())  # Muestra y registra la operación válida.

    # Simulación 8: confirma una reserva y ejecuta su bloque else.
    try:
        # César: comprueba las referencias antes de reservar.
        if c1 is None or s1 is None:
            raise ServiceNotAvailableFJError("Cliente o servicio de sala no disponible.")
        r1 = Reservation("R101", c1, s1, 3)  # Guarda el dato o el resultado para usarlo después.
        mensaje = r1.confirm_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r1)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(8, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(8, mensaje)  # Muestra y registra la operación válida.

    # Simulación 9: una duración cero produce una excepción encadenada.
    try:
        # César: comprueba que existan cliente y servicio de equipos.
        if c1 is None or s2 is None:
            raise ServiceNotAvailableFJError("Cliente o servicio de equipo no disponible.")
        r2 = Reservation("R102", c1, s2, 0)  # Guarda el dato o el resultado para usarlo después.
        mensaje = r2.confirm_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r2)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(9, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(9, mensaje)  # Muestra y registra la operación válida.

    # Simulación 10: controla la reserva de un servicio inexistente.
    try:
        r3 = Reservation("R103", c1, None, 2)  # Guarda el dato o el resultado para usarlo después.
        mensaje = r3.confirm_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r3)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(10, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(10, mensaje)  # Muestra y registra la operación válida.

    # Simulación 11: calcula el costo de sala con los parámetros opcionales.
    try:
        # César: evita utilizar un servicio que no pudo crearse.
        if s1 is None:
            raise ServiceNotAvailableFJError("Servicio de sala no disponible.")
        costo_sala = s1.calculate_cost(discount=0.15, tax=0.19)  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(11, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(11, f"Room cost with discount and tax: {costo_sala:.2f}")  # Muestra y registra la operación válida.

    # Simulación 12: rechaza horas negativas sin devolver un costo alternativo.
    try:
        costo_equipo = s2.calculate_cost(hours=-2)  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(12, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(12, f"Equipment cost: {costo_equipo:.2f}")  # Muestra y registra la operación válida.

    # Simulación 13: cancela la reserva confirmada en la simulación 8.
    try:
        mensaje = r1.cancel_reservation()  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(13, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(13, mensaje)  # Muestra y registra la operación válida.

    # Simulación 14: calcula el alquiler de equipos después de un error anterior.
    try:
        # César: comprueba que el servicio de equipos exista.
        if s2 is None:
            raise ServiceNotAvailableFJError("Servicio de equipos no disponible.")
        costo_equipo = s2.calculate_cost(hours=5, insurance_fee=15.0)  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(14, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(14, f"Equipment cost for 5 hours: {costo_equipo:.2f}")  # Muestra y registra la operación válida.

    # Simulación 15: demuestra que también se controla un TypeError de Python.
    try:
        # La ausencia de nombre y correo es intencional en este caso de prueba.
        cliente_incompleto = Client("C004")
        clients_list.append(cliente_incompleto)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(15, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(15, cliente_incompleto.get_details())  # Muestra y registra la operación válida.

    # Simulación 16: confirma que el programa continúa después del TypeError.
    try:
        costo_asesoria = s3.calculate_cost(complexity_factor=1.5)  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(16, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(16, f"Consulting cost: {costo_asesoria:.2f}")  # Muestra y registra la operación válida.

    # Simulación 17: confirma y procesa una sala por dos unidades de duración.
    try:
        r4 = Reservation("R104", c1, s1, 2)  # Guarda el dato o el resultado para usarlo después.
        r4.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        total = r4.process_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r4)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(17, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(17, f"Room reservation processed: {total:.2f}")  # Muestra y registra la operación válida.

    # Simulación 18: procesa equipos y cobra el seguro una sola vez.
    try:
        r5 = Reservation("R105", c1, s2, 3)  # Guarda el dato o el resultado para usarlo después.
        r5.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        total = r5.process_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r5)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(18, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(18, f"Equipment reservation processed: {total:.2f}")  # Muestra y registra la operación válida.

    # Simulación 19: procesa una asesoría confirmada.
    try:
        r6 = Reservation("R106", c1, s3, 2)  # Guarda el dato o el resultado para usarlo después.
        r6.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        total = r6.process_reservation()  # Guarda el dato o el resultado para usarlo después.
        reservations_list.append(r6)  # Guarda en la lista el objeto válido.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(19, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(19, f"Consulting reservation processed: {total:.2f}")  # Muestra y registra la operación válida.

    # Simulación 20: no permite procesar dos veces la misma reserva.
    try:
        r4.process_reservation()  # Calcula el costo y marca la reserva como procesada.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(20, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(20, "Reservation processed again.")  # Muestra y registra la operación válida.

    # Simulación 21: rechaza un servicio marcado como no disponible.
    try:
        servicio_ocupado = RoomReservationService("SR03", 100, 10)  # Guarda el dato o el resultado para usarlo después.
        servicio_ocupado.available = False  # Guarda el dato o el resultado para usarlo después.
        reserva_ocupada = Reservation("R107", c1, servicio_ocupado, 1)  # Guarda el dato o el resultado para usarlo después.
        reserva_ocupada.confirm_reservation()  # Confirma la reserva después de validar sus datos.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(21, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(21, "Unavailable service reserved.")  # Muestra y registra la operación válida.

    # Simulación 22: demuestra continuidad con un cálculo válido al final.
    try:
        total = s3.calculate_cost(complexity_factor=1.5)  # Guarda el dato o el resultado para usarlo después.
    except Exception as error:  # Captura el error para tratarlo de forma controlada.
        registrar_error(22, error)  # Registra el fallo y permite continuar con el siguiente caso.
    else:  # Ejecuta este bloque cuando la operación anterior fue válida.
        registrar_exito(22, f"Final consulting cost: {total:.2f}")  # Muestra y registra la operación válida.

    # El cierre indica operaciones procesadas, no que todos los datos eran válidos.
    print("\nFIN: se procesaron las 22 simulaciones, incluidos los errores de prueba.")
    print(f"Clientes válidos: {len(clients_list)}")  # Muestra el resultado en la consola.
    print(f"Servicios válidos: {len(services_list)}")  # Muestra el resultado en la consola.
    print(f"Reservas registradas (incluye canceladas y procesadas): {len(reservations_list)}")  # Muestra el resultado en la consola.
    print("Consulte fj_software_exceptions.log para revisar los detalles.")  # Muestra el resultado en la consola.
    logging.info("Fin de las 22 simulaciones.")  # Escribe el evento o el error en el registro.
