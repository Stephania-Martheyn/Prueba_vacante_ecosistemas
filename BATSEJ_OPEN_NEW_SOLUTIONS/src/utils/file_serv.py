import os
import pandas as pd

def guardar_copia_seguridad(tabla, fecha_inicio, fecha_fin):
    """
    Guarda una copia de seguridad de la tabla en formato Excel en la carpeta 'resultado/'.

    Parámetros:
    - tabla: lista de listas con los datos a almacenar en el Excel.
    - fecha_inicio: fecha inicial del período en formato 'YYYY-MM'.
    - fecha_fin: fecha final del período en formato 'YYYY-MM'.

    Retorna:
    - str: ruta completa del archivo generado.
    """

    carpeta_resultado = "resultado"
    if not os.path.exists(carpeta_resultado):
        os.makedirs(carpeta_resultado)

    # Formatear las fechas eliminando el guion
    periodo_inicio = fecha_inicio.replace("-", "")  
    periodo_fin = fecha_fin.replace("-", "")  

    # Construir el nombre del archivo
    nombre_archivo = f"{periodo_inicio}_{periodo_fin}_backup_facturas.xlsx"
    ruta_archivo = os.path.join(carpeta_resultado, nombre_archivo)

    # Definir los encabezados de la tabla
    encabezados = ["Fecha", "Nombre", "NIT", "Comisión", "IVA", "Total", "Correo"]

    # Convertir los datos en un DataFrame de Pandas
    df = pd.DataFrame(tabla, columns=encabezados)

    # Guardar en formato XLSX sin índice
    df.to_excel(ruta_archivo, index=False)

    print(f"✅ Copia de seguridad guardada en: {ruta_archivo}")
    
    return ruta_archivo  
