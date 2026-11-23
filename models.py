# Código base: Software_FJ_UNAD de Evelyn Carolina Calvache Pabón.
# Aportes de Yeison: excepciones, validaciones y procesamiento de reservas.
# Aporte de César: propiedades name y base_cost, conservadas del ZIP.

# logging registra los eventos de las reservas.
import logging
# isfinite rechaza costos infinitos o indefinidos.
from math import isfinite
# ABC y abstractmethod permiten conservar las clases abstractas de Evelyn.
from abc import ABC, abstractmethod
# Se utilizan las tres excepciones que ya tenía el proyecto.
from exceptions import InvalidDataFJError, ServiceNotAvailableFJError, FailedReservationFJError


# Reutiliza una validación sencilla para números de costos y parámetros.
def validar_numero(valor, nombre, minimo=0):
    if type(valor) not in (int, float):  # Comprueba la condición antes de continuar.
        raise InvalidDataFJError(f"{nombre} must be a number.")  # Informa del dato o de la operación no permitida.
    try:  # Inicia la operación cuyo error se controlará.
        valido = isfinite(valor)  # Guarda el dato o el resultado para usarlo después.
    except OverflowError as error:  # Captura el error para tratarlo de forma controlada.
        raise InvalidDataFJError(f"{nombre} is too large.") from error  # Informa del dato o de la operación no permitida.
    if not valido or valor < minimo:  # Comprueba la condición antes de continuar.
        raise InvalidDataFJError(f"{nombre} must be finite and at least {minimo}.")  # Informa del dato o de la operación no permitida.


# Valida identificadores y nombres obligatorios sin aceptar solo espacios.
def validar_texto(valor, nombre):
    if not isinstance(valor, str) or valor.strip() == "":  # Comprueba la condición antes de continuar.
        raise InvalidDataFJError(f"{nombre} cannot be empty.")  # Informa del dato o de la operación no permitida.
    return valor.strip()  # Devuelve el resultado de la operación.


# Clase general para las entidades del sistema.
class AbstractEntityFJ(ABC):
    def __init__(self, entity_id):  # Define esta operación y los datos que recibe.
        # Guarda el identificador de la entidad.
        self.entity_id = validar_texto(entity_id, "Entity ID")

    @abstractmethod  # Indica una propiedad o un método abstracto.
    def get_details(self):  # Define esta operación y los datos que recibe.
        # Cada clase hija debe definir cómo muestra sus datos.
        pass


# Cliente conserva la herencia y la propiedad email del proyecto original.
class Client(AbstractEntityFJ):
    def __init__(self, entity_id, name, email):  # Define esta operación y los datos que recibe.
        # Inicializa el identificador heredado.
        super().__init__(entity_id)
        # La propiedad valida el nombre al crear o modificar el cliente.
        self.name = name
        # Esta asignación ejecuta la validación de la propiedad email.
        self.email = email

    # César: propiedad name del ZIP, para validar también cambios posteriores.
    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise InvalidDataFJError("El nombre del cliente no puede estar vacio.")
        self._name = value.strip()


    @property  # Indica una propiedad o un método abstracto.
    def email(self):  # Define esta operación y los datos que recibe.
        # Devuelve el correo almacenado.
        return self._email

    @email.setter  # Indica una propiedad o un método abstracto.
    def email(self, value):  # Define esta operación y los datos que recibe.
        # Validación básica del ejercicio; no intenta verificar la existencia del correo.
        correo = validar_texto(value, "Email")
        if correo.count("@") != 1 or any(letra.isspace() for letra in correo):  # Comprueba la condición antes de continuar.
            raise InvalidDataFJError("Invalid email format.")  # Informa del dato o de la operación no permitida.
        usuario, dominio = correo.split("@")  # Guarda el dato o el resultado para usarlo después.
        if not usuario or "." not in dominio or any(parte == "" for parte in dominio.split(".")):  # Comprueba la condición antes de continuar.
            raise InvalidDataFJError("Invalid email format.")  # Informa del dato o de la operación no permitida.
        self._email = correo  # Guarda el dato o el resultado para usarlo después.

    def get_details(self):  # Define esta operación y los datos que recibe.
        # Presenta los datos del cliente.
        return f"Client ID: {self.entity_id} | Name: {self.name} | Email: {self.email}"


# Clase abstracta común a los tres servicios.
class Service(ABC):
    def __init__(self, service_code, base_cost):  # Define esta operación y los datos que recibe.
        self.service_code = validar_texto(service_code, "Service code")  # Guarda el dato o el resultado para usarlo después.
        self.base_cost = base_cost  # Guarda el dato o el resultado para usarlo después.
        # Un servicio puede marcarse como no disponible sin eliminarlo de la lista.
        self.available = True

    # César: propiedad base_cost del ZIP; control de valores finitos ampliado por Yeison.
    @property
    def base_cost(self) -> float:
        return self._base_cost

    @base_cost.setter
    def base_cost(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise InvalidDataFJError("El costo base no puede ser negativo y debe ser numerico.")

        # Yeison: amplía el control de César para rechazar infinito y NaN.
        validar_numero(value, "Base cost")
        self._base_cost = float(value)


    # Sala y asesoría usan una tarifa por unidad de duración en este ejercicio.
    def calculate_reservation_cost(self, duration):
        return self.calculate_cost() * duration  # Devuelve el resultado de la operación.

    @abstractmethod  # Indica una propiedad o un método abstracto.
    def calculate_cost(self):  # Define esta operación y los datos que recibe.
        # Las clases hijas implementan sus propias fórmulas.
        pass

    @abstractmethod  # Indica una propiedad o un método abstracto.
    def describe_service(self):  # Define esta operación y los datos que recibe.
        # Las clases hijas describen su servicio.
        pass


# Servicio de reserva de salas.
class RoomReservationService(Service):
    def __init__(self, service_code, base_cost, room_capacity):  # Define esta operación y los datos que recibe.
        # Reutiliza el constructor de Service.
        super().__init__(service_code, base_cost)
        # Guarda la capacidad de la sala.
        if type(room_capacity) != int or room_capacity <= 0:
            raise InvalidDataFJError("Room capacity must be a positive integer.")  # Informa del dato o de la operación no permitida.
        self.room_capacity = room_capacity  # Guarda el dato o el resultado para usarlo después.

    def calculate_cost(self, discount=0.0, tax=0.19):  # Define esta operación y los datos que recibe.
        # Los parámetros opcionales conservan la sobrecarga simulada de Evelyn.
        validar_numero(discount, "Discount")
        validar_numero(tax, "Tax")  # Rechaza números inválidos antes de calcular.
        if discount > 1:  # Comprueba la condición antes de continuar.
            raise InvalidDataFJError("Use a discount from 0 to 1 and a non-negative tax.")  # Informa del dato o de la operación no permitida.
        # Aplica el descuento y después el impuesto de ejemplo del proyecto.
        subtotal = self.base_cost * (1 - discount)
        total = subtotal * (1 + tax)  # Guarda el dato o el resultado para usarlo después.
        # Devuelve el costo con dos decimales.
        validar_numero(total, "Total cost")
        return round(total, 2)  # Devuelve el resultado de la operación.

    def describe_service(self):  # Define esta operación y los datos que recibe.
        return f"[Room Service] Code: {self.service_code} | Capacity: {self.room_capacity} | Base cost: {self.base_cost}"  # Devuelve el resultado de la operación.


# Servicio de alquiler de equipos.
class EquipmentRentalService(Service):
    def __init__(self, service_code, base_cost, equipment_name):  # Define esta operación y los datos que recibe.
        # Inicializa los datos comunes del servicio.
        super().__init__(service_code, base_cost)
        # Guarda el nombre del equipo.
        self.equipment_name = validar_texto(equipment_name, "Equipment name")

    def calculate_cost(self, hours=1, insurance_fee=10.0):  # Define esta operación y los datos que recibe.
        # Rechaza una duración o un seguro inválidos.
        validar_numero(hours, "Rental hours")
        validar_numero(insurance_fee, "Insurance fee")  # Rechaza números inválidos antes de calcular.
        if hours <= 0:  # Comprueba la condición antes de continuar.
            raise InvalidDataFJError("Rental hours must be positive and insurance cannot be negative.")  # Informa del dato o de la operación no permitida.
        # Calcula el alquiler y agrega el seguro.
        total = self.base_cost * hours + insurance_fee
        validar_numero(total, "Total cost")  # Rechaza números inválidos antes de calcular.
        return round(total, 2)  # Devuelve el resultado de la operación.

    # Sobrescribe el cálculo por duración sin multiplicar varias veces el seguro.
    def calculate_reservation_cost(self, duration):
        return self.calculate_cost(hours=duration)  # Devuelve el resultado de la operación.

    def describe_service(self):  # Define esta operación y los datos que recibe.
        return f"[Equipment Rental] Code: {self.service_code} | Equipment: {self.equipment_name} | Hourly cost: {self.base_cost}"  # Devuelve el resultado de la operación.


# Servicio de asesoría especializada.
class SpecializedConsultingService(Service):
    def __init__(self, service_code, base_cost, specialty_area):  # Define esta operación y los datos que recibe.
        # Inicializa el servicio y guarda su especialidad.
        super().__init__(service_code, base_cost)
        self.specialty_area = validar_texto(specialty_area, "Specialty area")  # Guarda el dato o el resultado para usarlo después.

    def calculate_cost(self, complexity_factor=1.0):  # Define esta operación y los datos que recibe.
        # Conserva la regla de complejidad del proyecto original.
        validar_numero(complexity_factor, "Complexity factor", 1)
        # Un parámetro inválido genera un error en lugar de devolver otro costo.
        total = self.base_cost * complexity_factor
        validar_numero(total, "Total cost")  # Rechaza números inválidos antes de calcular.
        return round(total, 2)  # Devuelve el resultado de la operación.

    def describe_service(self):  # Define esta operación y los datos que recibe.
        return f"[Consulting Service] Code: {self.service_code} | Specialty: {self.specialty_area} | Base fee: {self.base_cost}"  # Devuelve el resultado de la operación.


# Relaciona un cliente, un servicio, una duración y un estado.
class Reservation:
    def __init__(self, reservation_id, client, service, duration):  # Define esta operación y los datos que recibe.
        # Guarda los datos necesarios para confirmar la reserva.
        self.reservation_id = validar_texto(reservation_id, "Reservation ID")
        self.client = client  # Guarda el dato o el resultado para usarlo después.
        self.service = service  # Guarda el dato o el resultado para usarlo después.
        self.duration = duration  # Guarda el dato o el resultado para usarlo después.
        # Toda reserva nueva empieza pendiente.
        self.status = "Pending"
        self.total_cost = None  # Guarda el costo calculado de la reserva.

    def confirm_reservation(self):  # Define esta operación y los datos que recibe.
        # Una reserva confirmada o cancelada no se confirma otra vez.
        if self.status != "Pending":
            raise FailedReservationFJError("Only pending reservations can be confirmed.")  # Informa del dato o de la operación no permitida.
        try:  # Inicia la operación cuyo error se controlará.
            # Comprueba que existan los objetos que necesita la reserva.
            if not isinstance(self.client, Client):
                raise InvalidDataFJError("A valid client is required.")  # Informa del dato o de la operación no permitida.
            if not isinstance(self.service, Service):  # Comprueba la condición antes de continuar.
                raise ServiceNotAvailableFJError("The requested service is not available.")  # Informa del dato o de la operación no permitida.
            if self.service.available is not True:  # Comprueba la condición antes de continuar.
                raise ServiceNotAvailableFJError("The requested service is not available.")  # Informa del dato o de la operación no permitida.
            # La duración debe ser un entero positivo, no un valor booleano.
            if type(self.duration) != int or self.duration <= 0:
                raise InvalidDataFJError("Reservation duration must be a positive integer.")  # Informa del dato o de la operación no permitida.
        except InvalidDataFJError as error:  # Captura el error para tratarlo de forma controlada.
            # Marca el fallo y conserva el error original mediante from.
            self.status = "Failed"
            raise FailedReservationFJError("Reservation could not be confirmed.") from error  # Informa del dato o de la operación no permitida.
        except ServiceNotAvailableFJError:  # Captura el error para tratarlo de forma controlada.
            # Propaga el error para que la simulación lo registre y continúe.
            self.status = "Failed"
            raise  # Propaga la excepción conservando su causa.
        else:  # Ejecuta este bloque cuando la operación anterior fue válida.
            # Este bloque sí se ejecuta porque el try ya no termina con return.
            self.status = "Confirmed"
            logging.info(f"Reserva {self.reservation_id}: confirmación completada en else.")  # Escribe el evento o el error en el registro.
            return f"Reservation {self.reservation_id} confirmed for {self.client.name}."  # Devuelve el resultado de la operación.
        finally:  # Ejecuta el registro final tanto en éxito como en fallo.
            # Se registra el estado tanto si hay error como si la reserva funciona.
            logging.info(f"Reserva {self.reservation_id}: estado final {self.status}.")

    def cancel_reservation(self):  # Define esta operación y los datos que recibe.
        # Solo permite cancelar una reserva pendiente o confirmada.
        if self.status not in ("Pending", "Confirmed"):
            raise FailedReservationFJError("This reservation cannot be cancelled.")  # Informa del dato o de la operación no permitida.
        # Cambia el estado y registra el evento.
        self.status = "Cancelled"
        logging.info(f"Reserva {self.reservation_id}: cancelada.")  # Escribe el evento o el error en el registro.
        return f"Reservation {self.reservation_id} cancelled."  # Devuelve el resultado de la operación.


    # Procesa únicamente una reserva confirmada y conserva el costo final.
    def process_reservation(self):
        if self.status != "Confirmed":  # Comprueba la condición antes de continuar.
            raise FailedReservationFJError("Only confirmed reservations can be processed.")  # Informa del dato o de la operación no permitida.
        try:  # Inicia la operación cuyo error se controlará.
            if self.service.available is not True:  # Comprueba la condición antes de continuar.
                raise ServiceNotAvailableFJError("The service is no longer available.")  # Informa del dato o de la operación no permitida.
            # Revisa de nuevo los datos si se modificaron después de confirmar.
            if type(self.duration) != int or self.duration <= 0:
                raise InvalidDataFJError("Reservation duration must be a positive integer.")  # Informa del dato o de la operación no permitida.
            total = self.service.calculate_reservation_cost(self.duration)  # Guarda el dato o el resultado para usarlo después.
            validar_numero(total, "Reservation total")  # Rechaza números inválidos antes de calcular.
        except Exception as error:  # Captura el error para tratarlo de forma controlada.
            self.status = "Failed"  # Actualiza el estado de la reserva.
            raise FailedReservationFJError("Reservation could not be processed.") from error  # Informa del dato o de la operación no permitida.
        else:  # Ejecuta este bloque cuando la operación anterior fue válida.
            self.total_cost = round(total, 2)  # Guarda el costo calculado de la reserva.
            self.status = "Processed"  # Actualiza el estado de la reserva.
            logging.info(f"Reserva {self.reservation_id}: procesada, costo {self.total_cost}.")  # Escribe el evento o el error en el registro.
            return self.total_cost  # Devuelve el resultado de la operación.
        finally:  # Ejecuta el registro final tanto en éxito como en fallo.
            logging.info(f"Reserva {self.reservation_id}: estado final {self.status}.")  # Escribe el evento o el error en el registro.
