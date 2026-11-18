# Aqui estoy importando las librerias para logs, clases abstractas y llaamndo las excepciones personalizadas de exceptions
import logging
from abc import ABC, abstractmethod
from exceptions import InvalidDataFJError, ServiceNotAvailableFJError, FailedReservationFJError

# clase abstracta 
class AbstractEntityFJ(ABC):
    def __init__(self, entity_id: str):
        self.entity_id = entity_id

    @abstractmethod
    def get_details(self) -> str:
        pass

# clase Cliente 
class Client(AbstractEntityFJ):
    def __init__(self, entity_id: str, name: str, email: str):
        super().__init__(entity_id)
        self.name = name
        self.email = email

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str):
        try:
            if "@" not in value or "." not in value:
                raise InvalidDataFJError(f"Invalid email format: {value}")
            self._email = value
        except InvalidDataFJError as e:
            logging.warning(f"Error al asignar email a cliente {self.entity_id}: {e}")
            self._email = "invalid_email@softwarefj.com"

    def get_details(self) -> str:
        return f"Client ID: {self.entity_id} | Name: {self.name} | Email: {self.email}"

# clase abstracta Servicio
class Service(ABC):
    def __init__(self, service_code: str, base_cost: float):
        self.service_code = service_code
        self.base_cost = base_cost

    @abstractmethod
    def calculate_cost(self, *args, **kwargs) -> float:
        pass

    @abstractmethod
    def describe_service(self) -> str:
        pass

# Servicio 1
class RoomReservationService(Service):
    def __init__(self, service_code: str, base_cost: float, room_capacity: int):
        super().__init__(service_code, base_cost)
        self.room_capacity = room_capacity

    def calculate_cost(self, discount: float = 0.0, tax: float = 0.19) -> float:
        try:
            if discount < 0 or tax < 0:
                raise InvalidDataFJError("Discount or tax cannot be negative.")
            subtotal = self.base_cost * (1 - discount)
            total = subtotal * (1 + tax)
            return round(total, 2)
        except InvalidDataFJError as e:
            logging.error(f"Error en calculo de costos de sala: {e}")
            return self.base_cost

    def describe_service(self) -> str:
        return f"[Room Service] Code: {self.service_code} | Capacity: {self.room_capacity} people | Base Cost: ${self.base_cost}"

# Servicio 2
class EquipmentRentalService(Service):
    def __init__(self, service_code: str, base_cost: float, equipment_name: str):
        super().__init__(service_code, base_cost)
        self.equipment_name = equipment_name

    def calculate_cost(self, hours: int = 1, insurance_fee: float = 10.0) -> float:
        # TODO: Borrar este prin
        print(f"DEBUG_CALC: Calculando equipos para {hours} horas...")
        try:
            if hours <= 0:
                raise InvalidDataFJError("Rental hours must be greater than zero.")
            total = (self.base_cost * hours) + insurance_fee
            return round(total, 2)
        except InvalidDataFJError as e:
            logging.error(f"Error en calculo de alquiler de equipo: {e}")
            return self.base_cost

    def describe_service(self) -> str:
        return f"[Equipment Rental] Code: {self.service_code} | Equipment: {self.equipment_name} | Hourly Cost: ${self.base_cost}"

# Servicio 3: Asesorias
class SpecializedConsultingService(Service):
    def __init__(self, service_code: str, base_cost: float, specialty_area: str):
        super().__init__(service_code, base_cost)
        self.specialty_area = specialty_area

    def calculate_cost(self, complexity_factor: float = 1.0) -> float:
        try:
            if complexity_factor < 1.0:
                raise InvalidDataFJError("Complexity factor cannot be less than 1.0.")
            total = self.base_cost * complexity_factor
            return round(total, 2)
        except InvalidDataFJError as e:
            logging.error(f"Error en calculo de asesoria: {e}")
            return self.base_cost

    def describe_service(self) -> str:
        return f"[Consulting Service] Code: {self.service_code} | Specialty: {self.specialty_area} | Base Fee: ${self.base_cost}"

# clase Reserva 
class Reservation:
    def __init__(self, reservation_id: str, client: Client, service: Service, duration: int):
        self.reservation_id = reservation_id
        self.client = client
        self.service = service
        self.duration = duration
        self.status = "Pending"
        self.debug_attempts_counter = 0  

    def confirm_reservation(self) -> str:
        try:
            self.debug_attempts_counter += 1 # incrementa el contador muerto
            if self.duration <= 0:
                raise FailedReservationFJError("Reservation duration must be a positive integer.")
            self.status = "Confirmed"
            logging.info(f"Reserva {self.reservation_id} confirmada exitosamente.")
            return f"Reservation {self.reservation_id} successfully CONFIRMED for client {self.client.name}."
        except FailedReservationFJError as e:
            self.status = "Failed"
            logging.error(f"Fallo al confirmar reserva {self.reservation_id}: {e}")
            return f"❌ [Reservation Exception] {e}"
        else:
            logging.info(f"Bloque else ejecutado limpiamente para la reserva {self.reservation_id}")
        finally:
            print(f"[Log interno] Estado actual de la reserva {self.reservation_id}: {self.status}")

    def cancel_reservation(self) -> str:
        self.status = "Cancelled"
        logging.info(f"Reserva {self.reservation_id} cancelada por el usuario.")
        return f"Reservation {self.reservation_id} has been CANCELLED."
