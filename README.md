# Pipeline de Datos – Limpieza, Transformación y Validación del Dataset

**Asignatura:** GESTIÓN DE DATOS PARA IA (ITY1101)  
**Resultado de Aprendizaje:** RA2  
**Indicadores de Logro:** IL 2.2 – IL 2.5  

Este proyecto implementa un pipeline de datos automatizado, reproducible y trazable para un conjunto de datos clínico veterinario (`mascotas.csv`). El flujo está diseñado en dos fases críticas: la limpieza de anomalías de formato y la posterior validación estructural y semántica de los datos bajo reglas de negocio.

---

## 📁 Estructura del Proyecto

[cite_start]De acuerdo con las buenas prácticas de modularidad, documentación y trazabilidad, el repositorio se organiza de la siguiente manera[cite: 12, 20]:

```text
mi_proyecto_pipeline/
├── data/
│   ├── raw/          # Contiene el dataset original/crudo (Inmutable)
│   └── processed/    # Contiene los datasets limpios y validados resultantes
├── src/
│   ├── limpiar_datos.py    # Script de la Fase 1: Limpieza y transformación
│   └── validar_datos.py    # Script de la Fase 2: Control de calidad (QA) y Logs
└── README.md         # Documentación técnica del proceso
