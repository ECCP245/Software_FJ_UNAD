# Software FJ

Proyecto de Programación 213023, Fase 4, grupo 110, UNAD.
Gestiona clientes, servicios y reservas mediante objetos y listas en memoria.
Solo se escribe un archivo para registrar eventos y errores; no usa bases de datos.

## Ejecución

Requiere Python 3.9 o posterior y no necesita instalar paquetes adicionales.

```bash
python Main.py
```

Se procesan 22 simulaciones: 13 operaciones válidas y 9 errores intencionales controlados.
La última operación válida demuestra continuidad después de los errores.
El registro queda en `fj_software_exceptions.log`, junto al programa.

## Archivos

- `models.py`: entidades, cliente, servicios y reserva.
- `exceptions.py`: tres excepciones personalizadas.
- `Main.py`: registro de eventos y simulaciones independientes.
- `pruebas_unitarias.py`: siete pruebas originales de Jaminton con ajustes de compatibilidad.
- `pruebas_completacion.py`: comprobaciones de validación y procesamiento.

## Pruebas

```bash
python -m unittest -v pruebas_unitarias pruebas_completacion
```

## Diseño

`AbstractEntityFJ` y `Service` son clases abstractas. `Client` hereda de la entidad general;
los servicios de salas, equipos y asesorías heredan de `Service`.
Las propiedades `name`, `email` y `base_cost` validan las asignaciones.
Los métodos de costos y descripción se sobrescriben en los servicios.
Los parámetros opcionales de `calculate_cost` representan la sobrecarga simulada en Python;
no se definen varios métodos del mismo nombre con firmas diferentes.

Una reserva comienza en Pending, puede confirmarse como Confirmed, cancelarse como Cancelled
o procesarse como Processed. Un fallo de validación o procesamiento deja Failed.
Solo una reserva confirmada puede procesarse; una procesada no puede confirmarse,
procesarse ni cancelarse otra vez. El servicio puede marcarse como no disponible con `available`.
Las excepciones se propagan hasta cada simulación, donde se registran y se permite continuar.
`raise ... from ...` conserva la causa y `finally` registra el estado de los intentos validados.

## Criterio de costos

El anexo no establece tarifas ni unidades exactas. En este proyecto la duración es una cantidad
de unidades: sala y asesoría cobran su tarifa por unidad; equipos usa horas y un solo seguro.
Las llamadas anteriores a `calculate_cost` mantienen las fórmulas y valores ya utilizados.
El impuesto 0.19 es un parámetro de ejemplo de la base académica.
No se implementan fechas, cruces de horario, interfaz gráfica ni bases de datos.

## Participación

- Evelyn Carolina Calvache Pabón: arquitectura y código base.
- Yeison Andrés Bran Henao: excepciones y simulaciones del PR 1; cierre de validaciones,
  procesamiento, documentación y compatibilidad de pruebas en esta versión.
- Jaminton Trespalacios Castillo: suite de siete pruebas y documentación del PR 2.
- César Alejandro Calderón Albarrán: propiedades `name` y `base_cost` y comprobaciones
  previas de referencias, importadas de su ZIP por Yeison en un commit separado.

Se conservan los commits originales. La integración del ZIP de César y las correcciones
de funcionamiento son dos commits distintos creados por Yeison desde su propia rama.
El primero reconoce a César en el mensaje, los comentarios y este README; no se utiliza
su identidad como autor de Git ni se presenta como un commit publicado desde su cuenta.

## Alcance del aporte de César y ajustes de cierre

Fuente: `Software_FJ - Aportes César.zip`, publicado el 21 de noviembre de 2026:
https://campus141.unad.edu.co/ses114/mod/forum/discuss.php?d=20986#p290851

El primer commit incorpora sus propiedades y guardas sobre la versión actual. La
separación de simulaciones y la corrección del `else` que también propuso ya estaban
resueltas en el PR 1 y se conservan. El segundo commit amplía su propiedad de costo
para rechazar `NaN` e infinito, completa el procesamiento de reservas y ajusta las
pruebas incompatibles de Jaminton. Mantiene la propagación de correos y cálculos
inválidos; no recupera los valores de reemplazo que todavía aparecían en el ZIP.

El ZIP contiene únicamente `main.py` y `models.py`, sin conclusiones formales. El
informe final describe su contribución técnica sin atribuirle conclusiones nuevas.
