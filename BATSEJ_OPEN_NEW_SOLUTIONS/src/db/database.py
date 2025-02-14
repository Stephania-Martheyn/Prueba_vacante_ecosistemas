import os
import shutil
import sqlite3
from src.config import DB_PATH, BASE_DIR

# Ruta donde PyInstaller guarda los archivos al ejecutar el binario
RUTA_ORIGEN_DB = os.path.join(BASE_DIR, "data", "database.sqlite")

# Asegurar que la base de datos existe en el destino
if not os.path.exists(DB_PATH):
    if os.path.exists(RUTA_ORIGEN_DB):
        shutil.copy(RUTA_ORIGEN_DB, DB_PATH)
    else:
        print(f"Error: No se encontró la base de datos en {RUTA_ORIGEN_DB}")
        raise FileNotFoundError(f"No se encontró la base de datos en {RUTA_ORIGEN_DB}")

def conectar_db():
    """Crea y devuelve una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row 
    return conn
