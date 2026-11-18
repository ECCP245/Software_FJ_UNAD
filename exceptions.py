# Aqui estoy importando la libreria de python para guardar en el log cada vez que salte una excepcion
import logging

# Excepciones 
class InvalidDataFJError(Exception):
    """Raised when data fields do not meet Software FJ standards."""
    def __init__(self, message="The provided data is invalid."):
        super().__init__(message)
        logging.error(f"Custom Exception Triggered: {message}")

class ServiceNotAvailableFJError(Exception):
    """Raised when a specific Software FJ service is inactive or not found."""
    def __init__(self, message="The requested service is not available."):
        super().__init__(message)
        logging.error(f"Custom Exception Triggered: {message}")

class FailedReservationFJError(Exception):
    """Raised when a reservation process fails due to business rule conflicts."""
    def __init__(self, message="Reservation processing failed."):
        super().__init__(message)
        logging.error(f"Custom Exception Triggered: {message}")
