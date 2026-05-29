# Pipeline de Datos – Limpieza, Transformación y Validación del Dataset

**Asignatura:** GESTIÓN DE DATOS PARA IA (ITY1101)  
**Resultado de Aprendizaje:** RA2  
**Indicadores de Logro:** IL 2.2 – IL 2.5  

Este proyecto implementa un pipeline de datos automatizado, reproducible y trazable para un conjunto de datos clínico veterinario (`mascotas.csv`). El flujo está diseñado en dos fases críticas: la limpieza de anomalías de formato y la posterior validación estructural y semántica de los datos bajo reglas de negocio.

---

## Fase de Validación de Calidad de Datos

Se implementó un segundo componente en el pipeline orientado al aseguramiento y control de calidad (QA de Datos). Las reglas aplicadas se dividen en dos categorías estratégicas:

### 1. Validaciones Estructurales
* **ID Mascota**: Debe ser estrictamente un valor numérico entero y no nulo para garantizar la integridad referencial del paciente.
* **Especie**: Restringido al catálogo oficial de la clínica `['perro', 'gato', 'conejo', 'pez', 'loro']`. Evita el ingreso de animales no soportados por el centro médico.
* **Rango de Peso**: Limitado entre `0.05 kg` y `120.0 kg` para detectar fallas extremas de entrada de datos (outliers biológicamente imposibles).
* **Fecha de Consulta**: Debe corresponder a una estructura cronológica coherente y almacenable en formato datetime.

### 2. Validaciones Semánticas (Lógica de Negocio)
* **Consistencia de Peso por Estado (Obeso)**: Si la etiqueta clínica asignada es 'obeso', el peso del paciente debe superar obligatoriamente los `30 kg` en caninos o los `6 kg` en felinos.
* **Consistencia de Datos de Contacto**: Si un mismo cliente posee múltiples registros de consultas, el correo electrónico asociado debe ser idéntico en todos ellos para evitar duplicidad de perfiles o pérdida de trazabilidad.
* **Regla de Negocio Propia (Justificación)**: El campo `costo_consulta` debe ser estrictamente mayor que cero (`> 0`). *Justificación:* Toda consulta registrada en el sistema de gestión debe representar un cobro transaccionado o un ítem base tasado; un valor igual a cero o negativo delata un error de omisión en caja o un bug en el procesamiento del precio.

## 📁 Estructura del Proyecto

De acuerdo con las buenas prácticas de modularidad, documentación y trazabilidad, el repositorio se organiza de la siguiente manera[cite: 12, 20]:

```text
mi_proyecto_pipeline/
├── data/
│   ├── raw/          # Contiene el dataset original/crudo (Inmutable)
│   └── processed/    # Contiene los datasets limpios y validados resultantes
├── src/
│   ├── limpiar_datos.py    # Script de la Fase 1: Limpieza y transformación
│   └── validar_datos.py    # Script de la Fase 2: Control de calidad (QA) y Logs
└── README.md         # Documentación técnica del proceso
