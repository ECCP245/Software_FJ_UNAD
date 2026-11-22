# Sistema de Gestión de Clientes Servicios y Reservas  Software FJ

Proyecto desarrollado para el curso Programación, Código: 213023 de la Universidad Nacional Abierta y a Distancia (UNAD) — Fase 4: Componente Práctico Prácticas Simuladas

## Descripción del Proyecto
Sistema de gestion en Python orientado a objetos que administra los clientes, reservas, servicios de Software FJ, funciona en memoria usando objetos y listas sin bases de datos y manejo de excepciones y regristro de errores. 

## Estructura del Repositorio
* `exceptions.py`: Define las excepciones personalizadas del sistema (`InvalidDataFJError`, `ServiceNotAvailableFJError`, `FailedReservationFJError`).
* `models.py`: Contiene la arquitectura orientada a objetos (`AbstractEntityFJ`, `Client`, `Service`, `RoomReservationService`, `EquipmentRentalService`, `SpecializedConsultingService`, `Reservation`) aplicando abstracción, herencia, encapsulación, polimorfismo y sobrecarga de métodos.
* `Main.py`: Script principal que configura el sistema de logs y ejecuta 16 simulaciones independientes: 9 operaciones válidas y 7 errores intencionales controlados.
* `fj_software_exceptions.log`: Archivo generado automáticamente al ejecutar el programa donde se registran los errores y eventos relevantes.

## Requisitos y Ejecución
1. Asegúrese de tener **Python 3.9 o posterior** instalado (No requiere librerias externas)
2. Clone el repositorio o descargue los archivos en una misma carpeta.
3. Ejecute el archivo principal desde la terminal:
   ```bash
   python Main.py
   ```

## Aporte de Yeison Andrés Bran Henao

Se corrige la propagación de errores y se conserva la causa del fallo de una reserva con `raise ... from ...`. El bloque `else` confirma únicamente las reservas válidas y `finally` registra su estado. Cada simulación controla su error para permitir que continúen las siguientes. Se conservan las clases y las fórmulas de costos del proyecto base de Evelyn, con comentarios `#`.

Los casos inválidos son intencionales; ver mensajes ERROR CONTROLADO es parte del resultado esperado. El detalle queda en `fj_software_exceptions.log`. Este aporte se prepara sobre el commit `965dfecfb8ee6319ef23aa19545f9d358627d463` y no incorpora el ZIP de César.
