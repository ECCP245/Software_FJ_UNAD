# Código base: Software_FJ_UNAD de Evelyn Carolina Calvache Pabón.
# Aporte de Yeison: excepciones y estados.
# Integración del ZIP de César: propiedades name y base_cost.

# logging registra los eventos de las reservas.
import logging
# ABC y abstractmethod permiten conservar las clases abstractas de Evelyn.
from abc import ABC, abstractmethod
# Se utilizan las tres excepciones que ya tenía el proyecto.
from exceptions import InvalidDataFJError, ServiceNotAvailableFJError, FailedReservationFJError


# Clase general para las entidades del sistema.
class AbstractEntityFJ(ABC):
    def __init__(self, entity_id):
        # Guarda el identificador de la entidad.
        self.entity_id = entity_id

    @abstractmethod
    def get_details(self):
        # Cada clase hija debe definir cómo muestra sus datos.
        pass


# Cliente conserva la herencia y la propiedad email del proyecto original.
class Client(AbstractEntityFJ):
    def __init__(self, entity_id, name, email):
        # Inicializa el identificador heredado.
        super().__init__(entity_id)
        # César: name valida el nombre al crear y modificar el cliente.
        self.name = name
        # Esta asignación ejecuta la validación de la propiedad email.
        self.email = email

    # Aporte original de César: encapsulación y validación de name.
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataFJError("El nombre del cliente no puede estar vacio.")
        self._name = value.strip()


    @property
    def email(self):
        # Devuelve el correo almacenado.
        return self._email

    @email.setter
    def email(self, value):
        # Validación básica del correo para las simulaciones del ejercicio.
        if not isinstance(value, str) or "@" not in value or "." not in value:
            raise InvalidDataFJError("Invalid email format.")
        # Solo guarda el correo si pasa la validación; no inventa un reemplazo.
        self._email = value

    def get_details(self):
        # Presenta los datos del cliente.
        return f"Client ID: {self.entity_id} | Name: {self.name} | Email: {self.email}"


# Clase abstracta común a los tres servicios.
class Service(ABC):
    def __init__(self, service_code, base_cost):
        # Guarda los datos comunes de los servicios.
        self.service_code = service_code
        self.base_cost = base_cost

    # Aporte original de César: validación del costo también al modificarlo.
    @property
    def base_cost(self) -> float:
        return self._base_cost

    @base_cost.setter
    def base_cost(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise InvalidDataFJError("El costo base no puede ser negativo y debe ser numerico.")

        self._base_cost = float(value)


    @abstractmethod
    def calculate_cost(self):
        # Las clases hijas implementan sus propias fórmulas.
        pass

    @abstractmethod
    def describe_service(self):
        # Las clases hijas describen su servicio.
        pass


# Servicio de reserva de salas.
class RoomReservationService(Service):
    def __init__(self, service_code, base_cost, room_capacity):
        # Reutiliza el constructor de Service.
        super().__init__(service_code, base_cost)
        # Guarda la capacidad de la sala.
        self.room_capacity = room_capacity

    def calculate_cost(self, discount=0.0, tax=0.19):
        # Los parámetros opcionales conservan la sobrecarga simulada de Evelyn.
        if discount < 0 or discount > 1 or tax < 0:
            raise InvalidDataFJError("Use a discount from 0 to 1 and a non-negative tax.")
        # Aplica el descuento y después el impuesto de ejemplo del proyecto.
        subtotal = self.base_cost * (1 - discount)
        total = subtotal * (1 + tax)
        # Devuelve el costo con dos decimales.
        return round(total, 2)

    def describe_service(self):
        return f"[Room Service] Code: {self.service_code} | Capacity: {self.room_capacity} | Base cost: {self.base_cost}"


# Servicio de alquiler de equipos.
class EquipmentRentalService(Service):
    def __init__(self, service_code, base_cost, equipment_name):
        # Inicializa los datos comunes del servicio.
        super().__init__(service_code, base_cost)
        # Guarda el nombre del equipo.
        self.equipment_name = equipment_name

    def calculate_cost(self, hours=1, insurance_fee=10.0):
        # Rechaza una duración o un seguro inválidos.
        if hours <= 0 or insurance_fee < 0:
            raise InvalidDataFJError("Rental hours must be positive and insurance cannot be negative.")
        # Calcula el alquiler y agrega el seguro.
        total = self.base_cost * hours + insurance_fee
        return round(total, 2)

    def describe_service(self):
        return f"[Equipment Rental] Code: {self.service_code} | Equipment: {self.equipment_name} | Hourly cost: {self.base_cost}"


# Servicio de asesoría especializada.
class SpecializedConsultingService(Service):
    def __init__(self, service_code, base_cost, specialty_area):
        # Inicializa el servicio y guarda su especialidad.
        super().__init__(service_code, base_cost)
        self.specialty_area = specialty_area

    def calculate_cost(self, complexity_factor=1.0):
        # Conserva la regla de complejidad del proyecto original.
        if complexity_factor < 1:
            raise InvalidDataFJError("Complexity factor cannot be less than 1.")
        # Un parámetro inválido genera un error en lugar de devolver otro costo.
        total = self.base_cost * complexity_factor
        return round(total, 2)

    def describe_service(self):
        return f"[Consulting Service] Code: {self.service_code} | Specialty: {self.specialty_area} | Base fee: {self.base_cost}"


# Relaciona un cliente, un servicio, una duración y un estado.
class Reservation:
    def __init__(self, reservation_id, client, service, duration):
        # Guarda los datos necesarios para confirmar la reserva.
        self.reservation_id = reservation_id
        self.client = client
        self.service = service
        self.duration = duration
        # Toda reserva nueva empieza pendiente.
        self.status = "Pending"

    def confirm_reservation(self):
        # Una reserva confirmada o cancelada no se confirma otra vez.
        if self.status != "Pending":
            raise FailedReservationFJError("Only pending reservations can be confirmed.")
        try:
            # Comprueba que existan los objetos que necesita la reserva.
            if not isinstance(self.client, Client):
                raise InvalidDataFJError("A valid client is required.")
            if not isinstance(self.service, Service):
                raise ServiceNotAvailableFJError("The requested service is not available.")
            # La duración debe ser un entero positivo, no un valor booleano.
            if type(self.duration) != int or self.duration <= 0:
                raise InvalidDataFJError("Reservation duration must be a positive integer.")
        except InvalidDataFJError as error:
            # Marca el fallo y conserva el error original mediante from.
            self.status = "Failed"
            raise FailedReservationFJError("Reservation could not be confirmed.") from error
        except ServiceNotAvailableFJError:
            # Propaga el error para que la simulación lo registre y continúe.
            self.status = "Failed"
            raise
        else:
            # Este bloque sí se ejecuta porque el try ya no termina con return.
            self.status = "Confirmed"
            logging.info(f"Reserva {self.reservation_id}: confirmación completada en else.")
            return f"Reservation {self.reservation_id} confirmed for {self.client.name}."
        finally:
            # Se registra el estado tanto si hay error como si la reserva funciona.
            logging.info(f"Reserva {self.reservation_id}: estado final {self.status}.")

    def cancel_reservation(self):
        # Solo permite cancelar una reserva pendiente o confirmada.
        if self.status not in ("Pending", "Confirmed"):
            raise FailedReservationFJError("This reservation cannot be cancelled.")
        # Cambia el estado y registra el evento.
        self.status = "Cancelled"
        logging.info(f"Reserva {self.reservation_id}: cancelada.")
        return f"Reservation {self.reservation_id} cancelled."
