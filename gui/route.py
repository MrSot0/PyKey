import os
import sys

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        # Aquí tomamos la raíz del proyecto, no la carpeta del archivo actual
        # Cambia esta ruta si tu estructura es diferente
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    return os.path.join(base_path, relative_path)

DB_PATH = resource_path("users.db")
KEY_PATH = resource_path("fernet.key")
