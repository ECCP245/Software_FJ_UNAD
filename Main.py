# Aqui estoy importando las librerias para los errores los registross, y llamando las clases de models y exceptions
# Preguntar si la libreria os es obligatoria o si con sys basta
import logging
import os
from exceptions import InvalidDataFJError, ServiceNotAvailableFJError, FailedReservationFJError
from models import (
    Client,
    RoomReservationService,
    EquipmentRentalService,
    SpecializedConsultingService,
    Reservation
)

# Configurando el archivo de registro en disco dentro de la carpeta del proyecto
current_dir = os.path.dirname(os.path.abspath(__file__))
log_file_path = os.path.join(current_dir, 'fj_software_exceptions.log')

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Bloque principal con las simulaciones
if __name__ == "__main__":
    print(">>> STARTING SOFTWARE FJ SYSTEM SIMULATIONS (10+ OPERATIONS) <<<\n")
    
    clients_list = []
    services_list = []
    reservations_list = []

    try:
        # Simulacion 1
        c1 = Client("C001", "Carlos Gomez", "carlos.gomez@softwarefj.com")
        clients_list.append(c1)
        print(f"[Simulacion 1] -> Client registered: {c1.name}")

        # Simulacion 2
        c2 = Client("C002", "Ana Perez", "correo_invalido_sin_caracteres")
        clients_list.append(c2)
        print(f"[Simulacion 2] -> Client with invalid email handled: {c2.email}")

        # Simulacion 3
        s1 = RoomReservationService("SR01", 200.0, 15)
        services_list.append(s1)
        print(f"[Simulacion 3] -> {s1.describe_service()}")

        # Simulacion 4
        s2 = EquipmentRentalService("SE01", 45.0, "Workstation PC")
        services_list.append(s2)
        print(f"[Simulacion 4] -> {s2.describe_service()}")

        # Simulacion 5
        s3 = SpecializedConsultingService("SC01", 350.0, "Cloud Migration")
        services_list.append(s3)
        print(f"[Simulacion 5] -> {s3.describe_service()}")

        # Simulacion 6
        r1 = Reservation("R101", c1, s1, duration=3)
        res_msg1 = r1.confirm_reservation()
        reservations_list.append(r1)
        print(f"[Simulacion 6] -> {res_msg1}")

        # Simulacion 7 
        r2 = Reservation("R102", c1, s2, duration=0)
        res_msg2 = r2.confirm_reservation()
        reservations_list.append(r2)
        print(f"[Simulacion 7] -> {res_msg2}")

        # Simulacion 8
        r3 = Reservation("R103", c1, s3, duration=2)
        res_msg3 = r3.confirm_reservation()
        reservations_list.append(r3)
        print(f"[Simulacion 8] -> {res_msg3}")

        # Simulacion 9
        cost_room = s1.calculate_store if hasattr(s1, 'calculate_store') else s1.calculate_cost(discount=0.15, tax=0.19)
        print(f"[Simulacion 9] -> Calculated Room Cost (with discount): ${cost_room}")

        # Simulacion 10
        cost_equip = s2.calculate_cost(hours=5, insurance_fee=15.0)
        print(f"[Simulacion 10] -> Calculated Equipment Cost (5 hours): ${cost_equip}")

        print("\n>>> ALL 10+ SIMULATIONS COMPLETED SUCCESSFULLY. CHECK 'fj_software_exceptions.log' <<<\n")

    except Exception as general_err:
        logging.critical(f"Error critico general: {general_err}")
        print(f"Critical System Error: {general_err}")
