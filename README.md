# Sistema de Gestión de Clientes Servicios y Reservas  Software FJ

Proyecto desarrollado para el curso Programación, Código: 213023 de la Universidad Nacional Abierta y a Distancia (UNAD) — Fase 4: Componente Práctico Prácticas Simuladas

## Descripción del Proyecto
Sistema de gestion en Python orientado a objetos que administra los clientes, reservas, servicios de Software FJ, funciona en memoria usando objetos y listas sin bases de datos y manejo de excepciones y regristro de errores. 

## Estructura del Repositorio
* `exceptions.py`: Define las excepciones personalizadas del sistema (`InvalidDataFJError`, `ServiceNotAvailableFJError`, `FailedReservationFJError`).
* `models.py`: Contiene la arquitectura orientada a objetos (`AbstractEntityFJ`, `Client`, `Service`, `RoomReservationService`, `EquipmentRentalService`, `SpecializedConsultingService`, `Reservation`) aplicando abstracción, herencia, encapsulación, polimorfismo y sobrecarga de métodos.
* `main.py`: Script principal que configura el sistema de logs y ejecuta las 10 simulaciones completas  sin interrumpir la ejecución.
* `fj_software_exceptions.log`: Archivo generado automáticamente al ejecutar el programa donde se registran los errores y eventos relevantes.

## Requisitos y Ejecución
1. Asegúrese de tener **Python 3.x** instalado (No requiere librerias externas)
2. Clone el repositorio o descargue los archivos en una misma carpeta.
3. Ejecute el archivo principal desde la terminal:
   ```bash
   python main.py
## Aporte de Jaminton Trespalacios Castillo (JamintonTC)

Se integra la suite de pruebas unitarias automatizadas en el archivo `pruebas_unitarias.py` utilizando la librería estándar `unittest` de Python, completamente documentada línea por línea con comentarios `#`.

Las pruebas validan de forma automatizada:
- Registro correcto de clientes y lanzamiento de `InvalidDataFJError` ante nombres vacíos.
- Rechazo de servicios con costos base negativos.
- Cálculos polimórficos de tarifas para alquiler de equipos y asesorías especializadas.
- Confirmación exitosa de reservas y manejo controlado de reservas con duración inválida mediante `FailedReservationFJError`.

Para ejecutar las pruebas unitarias desde la terminal:
```bash
python -m unittest pruebas_unitarias.py
```
