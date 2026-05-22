import os
import pandas as pd
import numpy as np

def pipeline_limpieza():
    # 1. Definir rutas de archivos
    ruta_origen = os.path.join("data", "raw", "mascotas.csv")
    ruta_destino = os.path.join("data", "processed", "mascotas_limpias.csv")
    
    print("Iniciando Pipeline de Limpieza...")
    
    # Cargar el dataset
    if not os.path.exists(ruta_origen):
        print(f"Error: No se encontró el archivo en {ruta_origen}")
        return
        
    df = pd.read_csv(ruta_origen)
    
    # 2. Eliminación de registros completamente vacíos o irrelevantes
    # Elimina filas donde todos los elementos sean nulos (como la fila 6)
    df.dropna(how='all', inplace=True)
    
    # Eliminar registros sin datos clave obligatorios (ej. sin nombre ni dueño)
    df.dropna(subset=['nombre', 'dueño_nombre'], how='all', inplace=True)
    
    # 3. Tratamiento de Duplicados
    # Normalizamos temporalmente para detectar el duplicado Firulais (ID 1 y 2)
    df['nombre_temp'] = df['nombre'].astype(str).str.upper()
    df['fecha_temp'] = df['fecha_consulta'].astype(str)
    
    # Eliminamos duplicados basados en nombre de mascota, dueño y fecha, dejando el primero
    df.drop_duplicates(subset=['nombre_temp', 'dueño_nombre', 'fecha_temp'], keep='first', inplace=True)
    df.drop(columns=['nombre_temp', 'fecha_temp'], inplace=True)
    
    # 4. Estandarización de Textos (Especie y Género integrado)
    df['especie'] = df['especie'].astype(str).str.lower().str.strip()
    
    # Homologar sinónimos y variaciones de género
    reemplazos_especie = {
        'perra': 'perro',
        'gata': 'gato',
        'cat': 'gato'
    }
    df['especie'] = df['especie'].replace(reemplazos_especie)
    
    # Capitalizar nombres propios para mantener consistencia visual
    df['nombre'] = df['nombre'].astype(str).str.capitalize()
    df['dueño_nombre'] = df['dueño_nombre'].astype(str).str.title()
    
    # 5. Estandarización de Fechas
    # Convertimos los distintos formatos detectados a un estándar YYYY-MM-DD
    df['fecha_consulta'] = pd.to_datetime(df['fecha_consulta'], format='mixed').dt.strftime('%Y-%m-%d')
    
    # 6. Corrección de Outliers (Valores fuera de rango)
    # Edades negativas (Fido) pasan a NaN o se corrigen a un valor coherente (usaremos NaN)
    df.loc[df['edad_años'] < 0, 'edad_años'] = np.nan
    
    # Pesos extremos (Errores de tipeo de Rex y Garfield)
    # Si es perro y pesa 350kg, probablemente eran 35.0kg. Si el gato pesa 9999kg, lo seteamos como nulo o mediana.
    df.loc[(df['especie'] == 'perro') & (df['peso_kg'] == 350.0), 'peso_kg'] = 35.0
    df.loc[(df['especie'] == 'gato') & (df['peso_kg'] > 100), 'peso_kg'] = np.nan
    
    # 7. Imputación de Valores Faltantes (Opcional/Criterio Técnico)
    # Para las edades vacías, calculamos la mediana según la especie
    df['edad_años'] = df.groupby('especie')['edad_años'].transform(lambda x: x.fillna(round(x.median(), 1)))
    # Si quedan elementos sin especie asignada que no permitan calcular mediana, rellenar con la general
    df['edad_años'] = df['edad_años'].fillna(round(df['edad_años'].median(), 1))
    
    # 8. Creación de Columnas Derivadas (Transformación avanzada)
    # Por ejemplo, clasificar la tarifa de consulta
    def clasificar_costo(costo):
        if costo < 20000: return 'Económica'
        elif costo <= 40000: return 'Estándar'
        else: return 'Premium'
        
    df['categoria_costo'] = df['costo_consulta'].apply(clasificar_costo)
    
    # 9. Guardar Dataset Procesado
    os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
    df.to_csv(ruta_destino, index=False)
    print(f"¡Proceso completado con éxito! Archivo guardado en: {ruta_destino}")

if __name__ == "__main__":
    pipeline_limpieza()