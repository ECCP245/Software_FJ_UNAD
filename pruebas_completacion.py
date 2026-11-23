# Comprobaciones de cierre de Yeison Andrés Bran Henao.
# Comprueba los requisitos añadidos en la preparación local.
import unittest
from models import Client, RoomReservationService, EquipmentRentalService  # Importa las herramientas usadas en este módulo.
from models import SpecializedConsultingService, Reservation  # Importa las herramientas usadas en este módulo.
from exceptions import InvalidDataFJError, FailedReservationFJError, ServiceNotAvailableFJError  # Importa las herramientas usadas en este módulo.


class TestCompletacion(unittest.TestCase):  # Define la clase y su herencia.
    # Prepara objetos nuevos para que las pruebas sean independientes.
    def setUp(self):
        self.cliente = Client("C1", "Cliente", "cliente@ejemplo.com")  # Guarda el dato o el resultado para usarlo después.
        self.sala = RoomReservationService("S1", 100, 10)  # Guarda el dato o el resultado para usarlo después.

    def test_correo_invalido(self):  # Define esta operación y los datos que recibe.
        for correo in ["@ejemplo.com", "a@@b.com", "a@.com", "a@b.", "a b@c.com", None]:  # Recorre los casos que se deben comprobar.
            with self.subTest(correo=correo):  # Identifica el dato de este caso de prueba.
                with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
                    self.cliente.email = correo  # Guarda el dato o el resultado para usarlo después.
                self.assertEqual(self.cliente.email, "cliente@ejemplo.com")  # Comprueba el resultado esperado de la prueba.

    def test_cambio_nombre(self):  # Define esta operación y los datos que recibe.
        with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
            self.cliente.name = " "  # Guarda el dato o el resultado para usarlo después.
        self.assertEqual(self.cliente.name, "Cliente")  # Comprueba el resultado esperado de la prueba.

    def test_costos_invalidos(self):  # Define esta operación y los datos que recibe.
        for valor in [-1, True, "100", float("nan"), float("inf")]:  # Recorre los casos que se deben comprobar.
            with self.subTest(valor=valor):  # Identifica el dato de este caso de prueba.
                with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
                    self.sala.base_cost = valor  # Guarda el dato o el resultado para usarlo después.
                self.assertEqual(self.sala.base_cost, 100)  # Comprueba el resultado esperado de la prueba.

    def test_capacidad_invalida(self):  # Define esta operación y los datos que recibe.
        for capacidad in [0, -1, True, 1.5, "10"]:  # Recorre los casos que se deben comprobar.
            with self.subTest(capacidad=capacidad):  # Identifica el dato de este caso de prueba.
                with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
                    RoomReservationService("S", 100, capacidad)

    def test_parametros_calculo(self):  # Define esta operación y los datos que recibe.
        equipo = EquipmentRentalService("E", 40, "PC")  # Guarda el dato o el resultado para usarlo después.
        asesoria = SpecializedConsultingService("A", 100, "Software")  # Guarda el dato o el resultado para usarlo después.
        operaciones = [lambda: self.sala.calculate_cost(discount=1.1),  # Guarda el dato o el resultado para usarlo después.
                       lambda: self.sala.calculate_cost(tax=float("inf")),  # Guarda el dato o el resultado para usarlo después.
                       lambda: equipo.calculate_cost(hours=True),  # Guarda el dato o el resultado para usarlo después.
                       lambda: equipo.calculate_cost(insurance_fee=-1),  # Guarda el dato o el resultado para usarlo después.
                       lambda: asesoria.calculate_cost(complexity_factor="2")]  # Guarda el dato o el resultado para usarlo después.
        for operacion in operaciones:  # Recorre los casos que se deben comprobar.
            with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
                operacion()

    def test_procesamiento_polimorfico(self):  # Define esta operación y los datos que recibe.
        # Sala y asesoría cobran por unidad; el equipo suma un solo seguro.
        servicios = [self.sala, EquipmentRentalService("E", 40, "PC"),
                     SpecializedConsultingService("A", 100, "Software")]
        for servicio, esperado in zip(servicios, [238, 90, 200]):  # Recorre los casos que se deben comprobar.
            with self.subTest(servicio=servicio.service_code):  # Identifica el dato de este caso de prueba.
                reserva = Reservation("R", self.cliente, servicio, 2)  # Guarda el dato o el resultado para usarlo después.
                reserva.confirm_reservation()  # Confirma la reserva después de validar sus datos.
                self.assertEqual(reserva.process_reservation(), esperado)  # Comprueba el resultado esperado de la prueba.
                self.assertEqual(reserva.status, "Processed")  # Comprueba el resultado esperado de la prueba.
                self.assertEqual(reserva.total_cost, esperado)  # Comprueba el resultado esperado de la prueba.

    def test_procesamiento_sin_confirmar(self):  # Define esta operación y los datos que recibe.
        reserva = Reservation("R", self.cliente, self.sala, 1)  # Guarda el dato o el resultado para usarlo después.
        with self.assertRaises(FailedReservationFJError):  # Comprueba que la operación rechaza este caso inválido.
            reserva.process_reservation()  # Calcula el costo y marca la reserva como procesada.
        self.assertEqual(reserva.status, "Pending")  # Comprueba el resultado esperado de la prueba.

    def test_servicio_no_disponible(self):  # Define esta operación y los datos que recibe.
        self.sala.available = False  # Guarda el dato o el resultado para usarlo después.
        reserva = Reservation("R", self.cliente, self.sala, 1)  # Guarda el dato o el resultado para usarlo después.
        with self.assertRaises(ServiceNotAvailableFJError):  # Comprueba que la operación rechaza este caso inválido.
            reserva.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        self.assertEqual(reserva.status, "Failed")  # Comprueba el resultado esperado de la prueba.

    def test_fallo_durante_procesamiento(self):  # Define esta operación y los datos que recibe.
        reserva = Reservation("R", self.cliente, self.sala, 1)  # Guarda el dato o el resultado para usarlo después.
        reserva.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        self.sala.available = False  # Guarda el dato o el resultado para usarlo después.
        with self.assertRaises(FailedReservationFJError) as fallo:  # Comprueba que la operación rechaza este caso inválido.
            reserva.process_reservation()  # Calcula el costo y marca la reserva como procesada.
        self.assertIsInstance(fallo.exception.__cause__, ServiceNotAvailableFJError)  # Comprueba el resultado esperado de la prueba.
        self.assertEqual(reserva.status, "Failed")  # Comprueba el resultado esperado de la prueba.
        self.assertIsNone(reserva.total_cost)  # Comprueba el resultado esperado de la prueba.

    def test_estados_despues_procesamiento(self):  # Define esta operación y los datos que recibe.
        reserva = Reservation("R", self.cliente, self.sala, 1)  # Guarda el dato o el resultado para usarlo después.
        reserva.confirm_reservation()  # Confirma la reserva después de validar sus datos.
        reserva.process_reservation()  # Calcula el costo y marca la reserva como procesada.
        for operacion in [reserva.confirm_reservation, reserva.process_reservation, reserva.cancel_reservation]:  # Recorre los casos que se deben comprobar.
            with self.assertRaises(FailedReservationFJError):  # Comprueba que la operación rechaza este caso inválido.
                operacion()
            self.assertEqual(reserva.status, "Processed")  # Comprueba el resultado esperado de la prueba.

    def test_encadenamiento_duracion(self):  # Define esta operación y los datos que recibe.
        for duracion in [0, -1, 1.5, True, "2"]:  # Recorre los casos que se deben comprobar.
            reserva = Reservation("R", self.cliente, self.sala, duracion)  # Guarda el dato o el resultado para usarlo después.
            with self.assertRaises(FailedReservationFJError) as fallo:  # Comprueba que la operación rechaza este caso inválido.
                reserva.confirm_reservation()  # Confirma la reserva después de validar sus datos.
            self.assertIsInstance(fallo.exception.__cause__, InvalidDataFJError)  # Comprueba el resultado esperado de la prueba.

    def test_identificadores_vacios(self):  # Define esta operación y los datos que recibe.
        for operacion in [lambda: Client("", "Cliente", "c@ejemplo.com"),  # Recorre los casos que se deben comprobar.
                          lambda: RoomReservationService("", 100, 10),
                          lambda: Reservation("", self.cliente, self.sala, 1)]:
            with self.assertRaises(InvalidDataFJError):  # Comprueba que la operación rechaza este caso inválido.
                operacion()

    # Comprueba que las clases abstractas no se puedan crear directamente.
    def test_clases_abstractas(self):
        from models import AbstractEntityFJ, Service
        with self.assertRaises(TypeError):
            AbstractEntityFJ("A")
        with self.assertRaises(TypeError):
            Service("S", 100)

    # Un fallo inesperado conserva la causa y no deja la reserva como procesada.
    def test_error_inesperado_procesamiento(self):
        reserva = Reservation("R", self.cliente, self.sala, 1)
        reserva.confirm_reservation()
        def provocar_error(duration):
            raise RuntimeError("Fallo intencional de comprobación")
        self.sala.calculate_reservation_cost = provocar_error
        with self.assertRaises(FailedReservationFJError) as fallo:
            reserva.process_reservation()
        self.assertIsInstance(fallo.exception.__cause__, RuntimeError)
        self.assertEqual(reserva.status, "Failed")
        self.assertIsNone(reserva.total_cost)

    # Las variantes opcionales conservan los resultados usados por el grupo.
    def test_variantes_costos(self):
        sala = RoomReservationService("S2", 200, 10)
        equipo = EquipmentRentalService("E", 45, "PC")
        asesoria = SpecializedConsultingService("A", 350, "Software")
        self.assertEqual(sala.calculate_cost(), 238)
        self.assertEqual(sala.calculate_cost(discount=0.15, tax=0.19), 202.3)
        self.assertEqual(equipo.calculate_cost(), 55)
        self.assertEqual(equipo.calculate_cost(hours=5, insurance_fee=15), 240)
        self.assertEqual(asesoria.calculate_cost(), 350)
        self.assertEqual(asesoria.calculate_cost(complexity_factor=1.5), 525)


if __name__ == "__main__":  # Ejecuta este bloque solo al abrir el archivo directamente.
    unittest.main()  # Ejecuta las pruebas de este archivo.
