import os
import sys

def obtener_base_dir():
    if getattr(sys, 'frozen', False):  
        return sys._MEIPASS  # Carpeta temporal de PyInstaller
    return os.path.dirname(os.path.abspath(__file__))

def obtener_ruta_db():
    if sys.platform == "win32":
        carpeta_datos = os.path.join(os.getenv("LOCALAPPDATA"), "TuApp")
    else:
        carpeta_datos = os.path.join(os.path.expanduser("~"), ".local", "share", "TuApp")

    os.makedirs(carpeta_datos, exist_ok=True)  # Asegura que la carpeta exista
    return os.path.join(carpeta_datos, "database.sqlite")

BASE_DIR = obtener_base_dir()
DB_PATH = obtener_ruta_db()