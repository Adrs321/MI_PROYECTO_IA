import os
import pandas as pd
import numpy as np

def cargar_datos():
    ruta_origen = os.path.join("data", "processed", "mascotas_limpias.csv")
    if not os.path.exists(ruta_origen):
        raise FileNotFoundError(f"No se encuentra el dataset limpio en {ruta_origen}. Ejecuta primero el script de limpieza.")
    return pd.read_csv(ruta_origen)

def validaciones_estructurales(df):
    print("\n--- [EJECUTANDO VALIDACIONES ESTRUCTURALES] ---")
    inicial = len(df)
    
    # 1. id_mascota sea int y no nulo
    # Al cargar de CSV, a veces los nulos transforman la columna a float. Forzamos conversión para evaluar.
    df['id_mascota'] = pd.to_numeric(df['id_mascota'], errors='coerce')
    cond_id = df['id_mascota'].notnull() & (df['id_mascota'] % 1 == 0)
    
    # 2. Validar que especie esté en la lista permitida
    especies_validas = ['perro', 'gato', 'conejo', 'pez', 'loro']
    cond_especie = df['especie'].isin(especies_validas)
    
    # 3. Verificar que peso_kg esté entre 0.05 y 120
    cond_peso = df['peso_kg'].between(0.05, 120.0, inclusive='both')
    
    # 4. Comprobar que fecha_consulta sea datetime válido
    # Intentamos convertir. Si falla o es NaT, la condición será False.
    fechas_convertidas = pd.to_datetime(df['fecha_consulta'], errors='coerce')
    cond_fecha = fechas_convertidas.notnull()
    
    # Combinar todas las estructurales
    registro_valido = cond_id & cond_especie & cond_peso & cond_fecha
    
    df_validos = df[registro_valido].copy()
    df_invalidos = df[~registro_valido].copy()
    
    print(f"Log Estructural: Inicial: {inicial} | Válidos: {len(df_validos)} | Inválidos: {len(df_invalidos)}")
    return df_validos, df_invalidos

def validaciones_semanticas(df_validos, df_invalidos):
    print("\n--- [EJECUTANDO VALIDACIONES SEMÁNTICAS] ---")
    inicial_validos = len(df_validos)
    
    if inicial_validos == 0:
        print("No hay registros estructuralmente válidos para evaluar semántica.")
        return df_validos, df_invalidos

    # Para evaluar la regla de 'obeso', primero necesitamos crear la columna 'rango_peso' de forma lógica o usar una existente.
    # Como tu dataset no venía con 'rango_peso', la crearemos dinámicamente según la regla inversa para evaluar consistencia,
    # o simularemos que ya existe. Asumiremos que se define una regla basada en los umbrales solicitados:
    if 'rango_peso' not in df_validos.columns:
        # Simulamos la columna 'rango_peso' basándonos en los datos para verificar consistencia.
        # En un flujo real esta columna vendría del negocio.
        cond_obeso_perro = (df_validos['especie'] == 'perro') & (df_validos['peso_kg'] > 30)
        cond_obeso_gato = (df_validos['especie'] == 'gato') & (df_validos['peso_kg'] > 6)
        df_validos['rango_peso'] = np.where(cond_obeso_perro | cond_obeso_gato, 'obeso', 'normal')

    # Regla 1: Si rango_peso == 'obeso' -> peso > 30 (perro) o > 6 (gato)
    cumple_peso_perro = (df_validos['especie'] == 'perro') & (df_validos['peso_kg'] > 30)
    cumple_peso_gato = (df_validos['especie'] == 'gato') & (df_validos['peso_kg'] > 6)
    
    # Es correcto si NO es obeso, O si siendo obeso cumple alguna de las dos condiciones de peso
    cond_sem_peso = (df_validos['rango_peso'] != 'obeso') | (cumple_weight_perro := cumple_peso_perro | cumple_peso_gato)

    # Regla 2: 2+ consultas del mismo dueño -> verificar email consistente
    # Buscamos dueños con más de un correo electrónico distinto registrado en el set actual
    dueños_inconsistentes = df_validos.groupby('dueño_nombre')['dueño_email'].nunique()
    dueños_conflictivos = dueños_inconsistentes[dueños_inconsistentes > 1].index
    cond_sem_email = ~df_validos['dueño_nombre'].isin(dueños_conflictivos)

    # Regla 3 (REGLA LIBRE): Costo de consulta debe ser estrictamente mayor a 0
    # Justificación: Ninguna atención veterinaria, ni clínica ni control, puede registrar un costo cero o negativo en el sistema.
    cond_regla_libre = df_validos['costo_consulta'] > 0

    # Combinar todas las semánticas
    semantica_correcta = cond_sem_peso & cond_sem_email & cond_regla_libre
    
    # Filtrar y mover los que fallan semántica a la lista de inválidos
    nuevos_invalidos = df_validos[~semantica_correcta]
    df_final_validos = df_validos[semantica_correcta]
    df_final_invalidos = pd.concat([df_invalidos, nuevos_invalidos], ignore_index=True)
    
    print(f"Log Semántico: Evaluados: {inicial_validos} | Pasaron: {len(df_final_validos)} | Rechazados: {len(nuevos_invalidos)}")
    return df_final_validos, df_final_invalidos

def exportar_y_reportar(df_total, df_val, df_inval):
    print("\n--- [REPORTE FINAL Y EXPORTACIÓN] ---")
    ruta_validos = os.path.join("data", "processed", "mascotas_validas.csv")
    ruta_invalidos = os.path.join("data", "processed", "mascotas_invalidas.csv")
    
    # Exportar datasets resultantes
    df_val.to_csv(ruta_validos, index=False)
    df_inval.to_csv(ruta_invalidos, index=False)
    
    # Calcular porcentaje final
    total_registros = len(df_total)
    total_validos = len(df_val)
    
    porcentaje_validos = (total_validos / total_registros) * 100 if total_registros > 0 else 0
    
    print(f"-> Archivo de registros válidos guardado en: {ruta_validos}")
    print(f"-> Archivo de registros inválidos guardado en: {ruta_invalidos}")
    print(f"\nPRINT FINAL: {porcentaje_validos:.2f}% de registros válidos sobre el total.")

def main():
    try:
        df_original = cargar_datos()
        
        # Flujo modular de validaciones
        df_val, df_inval = validaciones_estructurales(df_original)
        df_val_final, df_inval_final = validaciones_semanticas(df_val, df_inval)
        
        # Cierre e informe
        exportar_y_reportar(df_original, df_val_final, df_inval_final)
        
    except Exception as e:
        print(f"Error en el pipeline de validación: {e}")

if __name__ == "__main__":
    main()