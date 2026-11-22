# Importamos el módulo unittest estándar de Python para crear y ejecutar pruebas automatizadas
import unittest
# Importamos las excepciones personalizadas definidas en el módulo exceptions.py
from exceptions import InvalidDataFJError, ServiceNotAvailableFJError, FailedReservationFJError
# Importamos las clases principales del dominio desde el módulo models.py
from models import Client, RoomReservationService, EquipmentRentalService, SpecializedConsultingService, Reservation


# Definimos la clase de pruebas unitarias heredando de unittest.TestCase
class TestSoftwareFJ(unittest.TestCase):

    # Prueba 1: Verificar que un cliente con datos válidos se registre correctamente
    def test_registro_cliente_valido(self):
        # Instanciamos un objeto Client con ID, nombre y correo electrónico válidos
        cliente = Client("C10", "Laura Martinez", "laura@softwarefj.com")
        # Comprobamos que el atributo name coincida exactamente con el valor ingresado
        self.assertEqual(cliente.name, "Laura Martinez")

    # Prueba 2: Verificar que se lance excepción si el nombre del cliente queda vacío
    def test_cliente_nombre_vacio(self):
        # Validamos que al pasar un nombre vacío o con espacios se dispare InvalidDataFJError
        with self.assertRaises(InvalidDataFJError):
            Client("C11", "   ", "correo@softwarefj.com")

    # Prueba 3: Verificar que no se acepten servicios con costo base negativo
    def test_servicio_costo_negativo(self):
        # Validamos que intentar crear una sala con costo negativo (-50.0) lance InvalidDataFJError
        with self.assertRaises(InvalidDataFJError):
            RoomReservationService("S10", -50.0, 10)

    # Prueba 4: Verificar el cálculo polimórfico de costo en alquiler de equipos
    def test_calculo_costo_equipo(self):
        # Creamos un servicio de alquiler de equipo con tarifa base de 40.0 por hora
        equipo = EquipmentRentalService("E10", 40.0, "Workstation Pro")
        # Calculamos el costo total por 3 horas más un seguro fijo de 10.0 (40 * 3 + 10 = 130.0)
        total = equipo.calculate_cost(hours=3, insurance_fee=10.0)
        # Verificamos que el valor calculado sea exactamente 130.0
        self.assertEqual(total, 130.0)

    # Prueba 5: Verificar el cálculo polimórfico de costo en asesoría especializada
    def test_calculo_costo_asesoria(self):
        # Creamos un servicio de asesoría especializada con tarifa base de 100.0
        asesoria = SpecializedConsultingService("A10", 100.0, "Ciberseguridad")
        # Calculamos el costo para 2 sesiones aplicando el 19% de IVA (200 * 1.19 = 238.0)
        total = asesoria.calculate_cost(sessions=2, tax=0.19)
        # Verificamos que el resultado con impuestos coincida con 238.0
        self.assertAlmostEqual(total, 238.0)

    # Prueba 6: Verificar que una reserva válida se confirme y cambie su estado
    def test_confirmacion_reserva_valida(self):
        # Creamos un cliente y un servicio de sala válidos para la reserva
        cliente = Client("C12", "Pedro Ruiz", "pedro@softwarefj.com")
        sala = RoomReservationService("S12", 150.0, 20)
        # Instanciamos una reserva válida con duración de 2 horas
        reserva = Reservation("R100", cliente, sala, duration=2)
        # Ejecutamos el método de confirmación de la reserva
        resultado = reserva.confirm_reservation()
        # Comprobamos que el mensaje retornado contenga la palabra CONFIRMED
        self.assertIn("CONFIRMED", resultado)

    # Prueba 7: Verificar que una reserva con duración cero falle de forma controlada
    def test_reserva_duracion_invalida(self):
        # Creamos un cliente y un servicio válidos para la prueba de error
        cliente = Client("C13", "Sofia Gomez", "sofia@softwarefj.com")
        sala = RoomReservationService("S13", 100.0, 15)
        # Instanciamos una reserva inválida con duración igual a 0
        reserva = Reservation("R101", cliente, sala, duration=0)
        # Verificamos que al intentar confirmarla se lance la excepción FailedReservationFJError
        with self.assertRaises(FailedReservationFJError):
            reserva.confirm_reservation()


# Punto de entrada principal para ejecutar la suite de pruebas directamente
if __name__ == "__main__":
    # Iniciamos el ejecutor de pruebas unitarias de Python
    unittest.main()

