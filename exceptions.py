# Código base: proyecto Software_FJ_UNAD de Evelyn Carolina Calvache Pabón.
# Aporte local de Yeison Andrés Bran Henao: manejo sencillo de excepciones.
# El error se registra cuando se captura, para no repetirlo en el log.


# Identifica errores en los datos de entrada.
class InvalidDataFJError(Exception):
    pass  # Deja la implementación a la clase hija o a Exception.


# Identifica un servicio que no se puede utilizar.
class ServiceNotAvailableFJError(Exception):
    pass  # Deja la implementación a la clase hija o a Exception.


# Identifica un fallo al confirmar o cancelar una reserva.
class FailedReservationFJError(Exception):
    pass  # Deja la implementación a la clase hija o a Exception.
