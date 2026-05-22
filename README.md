# Pipeline de Datos - Limpieza y Transformación (Dataset Mascotas)

Este proyecto automatiza la ingesta, limpieza y transformación de un conjunto de datos clínico veterinario utilizando Python y Pandas.

## Transformaciones Aplicadas

1. **Remoción de Registros Inválidos**: Se eliminaron filas completamente vacías y registros huérfanos sin identificación.
2. **Control de Duplicados**: Se unificaron registros repetidos (mismo paciente, dueño y fecha de consulta).
3. **Estandarización de Variables Categóricas**:
   * Se normalizó la columna `especie` a minúsculas, unificando géneros (`perra` -> `perro`, `gata` -> `gato`) e idiomas (`cat` -> `gato`).
   * Se aplicó formato capitalizado a nombres de mascotas y dueños.
4. **Formato de Fechas**: Se parsearon múltiples estructuras (`mixed formats`) unificando todo al formato estándar `YYYY-MM-DD`.
5. **Tratamiento de Outliers**:
   * Se corrigieron errores de digitación en peso (ej. 350 kg corregido a 35.0 kg basado en raza/especie).
   * Valores absurdos o negativos se marcaron como nulos.
6. **Imputación de Nulos**: Las edades faltantes fueron completadas usando la mediana de edad correspondiente a cada especie.
7. **Ingeniería de Características**: Se añadió la columna `categoria_costo` para segmentar el valor de la consulta.

## Estructura de Salida
El dataset resultante se almacena de forma automatizada en `data/processed/mascotas_limpias.csv`.