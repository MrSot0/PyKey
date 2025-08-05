import os
import sqlite3
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet
import sys
from gui.route import resource_path

DB_PATH = resource_path("users.db")
KEY_PATH = resource_path("fernet.key")


# --- Conexión ---
def get_connection():
    return sqlite3.connect(DB_PATH)


# --- Gestión de clave de cifrado ---
def generar_o_cargar_clave():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, "rb") as f:
            key = f.read()
    else:
        key = Fernet.generate_key()
        with open(KEY_PATH, "wb") as f:
            f.write(key)
    return key

FERNET = Fernet(generar_o_cargar_clave())

# --- Inicialización y migraciones ---
def inicializar_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        # tabla de usuarios
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                usuario TEXT NOT NULL UNIQUE,
                contraseña_hash BLOB NOT NULL,
                imagen TEXT,
                creado_en TEXT NOT NULL
            )
        """)
        # vault propio de contraseñas (tus credenciales personales) sin 'notas'
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT,
                nombre_de_usuario TEXT,
                contraseña_encriptada BLOB NOT NULL,
                creado_en TEXT NOT NULL,
                actualizado_en TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
            )
        """)
        # tabla de contraseñas por plataforma con la nueva restricción única
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS contrasenas_platform (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL,
                plataforma TEXT COLLATE NOCASE NOT NULL,
                login TEXT NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT NOT NULL,
                UNIQUE(usuario, plataforma, login)
            )
        """)
        # llaves de recuperación y logs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recovery_keys (
			    id INTEGER PRIMARY KEY AUTOINCREMENT,
			    usuario TEXT NOT NULL UNIQUE,
			    llave_encriptada BLOB NOT NULL,
			    creado_en TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS recovery_key_reads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recovery_key_id INTEGER NOT NULL,
                leido_en TEXT NOT NULL,
                FOREIGN KEY(recovery_key_id) REFERENCES recovery_keys(id) ON DELETE CASCADE
            )
        """)
        conn.commit()

# --- Hashing de contraseñas de login ---
def hash_contrasena(password: str) -> bytes:
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return salt + dk  # guardamos salt + derived key

def verificar_contrasena(password: str, stored: bytes) -> bool:
    salt = stored[:16]
    dk = stored[16:]
    nuevo_dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return nuevo_dk == dk

# --- Cifrado para vault interno ---
def cifrar(texto: str) -> bytes:
    return FERNET.encrypt(texto.encode("utf-8"))

def descifrar(token: bytes) -> str:
    try:
        return FERNET.decrypt(token).decode("utf-8")
    except Exception:
        return "<error al descifrar>"

# --- Operaciones de usuario ---
def insertar_usuario(nombre, usuario, contraseña):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            contraseña_hash = hash_contrasena(contraseña.strip())
            cursor.execute("""
                INSERT INTO usuarios (nombre, usuario, contraseña_hash, creado_en)
                VALUES (?, ?, ?, ?)
            """, (nombre.strip(), usuario.strip(), contraseña_hash, datetime.utcnow().isoformat()))
            conn.commit()
    except sqlite3.IntegrityError:
        raise Exception(f"El usuario '{usuario}' ya existe.")

def obtener_usuario(usuario, contraseña):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, usuario, contraseña_hash, imagen FROM usuarios
            WHERE usuario = ?
        """, (usuario.strip(),))
        row = cursor.fetchone()
        if not row:
            return None
        stored_hash = row[3]
        if verificar_contrasena(contraseña, stored_hash):
            return {
                "id": row[0],
                "nombre": row[1],
                "usuario": row[2],
                "imagen": row[4],
            }
        return None

def actualizar_nombre_usuario(usuario, nuevo_nombre):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios SET nombre = ?
            WHERE usuario = ?
        """, (nuevo_nombre.strip(), usuario.strip()))
        conn.commit()

def actualizar_contrasena_usuario(usuario, nueva_contrasena):
    with get_connection() as conn:
        cursor = conn.cursor()
        nueva_hash = hash_contrasena(nueva_contrasena.strip())
        cursor.execute("""
            UPDATE usuarios SET contraseña_hash = ?
            WHERE usuario = ?
        """, (nueva_hash, usuario.strip()))
        conn.commit()

def actualizar_imagen_usuario(usuario, ruta_imagen):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE usuarios SET imagen = ?
            WHERE usuario = ?
        """, (ruta_imagen, usuario.strip()))
        conn.commit()

# --- Vault interno de passwords ---
def agregar_password(usuario_id, titulo, nombre_de_usuario, contraseña_plain):
    with get_connection() as conn:
        cursor = conn.cursor()
        contraseña_encriptada = cifrar(contraseña_plain)
        ahora = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO passwords 
                (usuario_id, titulo, nombre_de_usuario, contraseña_encriptada, creado_en)
            VALUES (?, ?, ?, ?, ?)
        """, (usuario_id, titulo, nombre_de_usuario, contraseña_encriptada, ahora))
        conn.commit()

def listar_passwords(usuario_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titulo, nombre_de_usuario, contraseña_encriptada, creado_en, actualizado_en
            FROM passwords
            WHERE usuario_id = ?
            ORDER BY creado_en DESC
        """, (usuario_id,))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "titulo": row[1],
                "nombre_de_usuario": row[2],
                "contraseña": descifrar(row[3]),
                "creado_en": row[4],
                "actualizado_en": row[5],
            })
        return result

def obtener_password(usuario_id, password_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titulo, nombre_de_usuario, contraseña_encriptada, creado_en, actualizado_en
            FROM passwords
            WHERE usuario_id = ? AND id = ?
        """, (usuario_id, password_id))
        row = cursor.fetchone()
        if not row:
            return None
        return {
            "id": row[0],
            "titulo": row[1],
            "nombre_de_usuario": row[2],
            "contraseña": descifrar(row[3]),
            "creado_en": row[4],
            "actualizado_en": row[5],
        }

def actualizar_password(usuario_id, password_id, nuevo_titulo=None, nuevo_nombre_usuario=None, nueva_contrasena=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        partes = []
        valores = []
        if nuevo_titulo is not None:
            partes.append("titulo = ?")
            valores.append(nuevo_titulo)
        if nuevo_nombre_usuario is not None:
            partes.append("nombre_de_usuario = ?")
            valores.append(nuevo_nombre_usuario)
        if nueva_contrasena is not None:
            partes.append("contraseña_encriptada = ?")
            valores.append(cifrar(nueva_contrasena))
        if not partes:
            return
        partes.append("actualizado_en = ?")
        valores.append(datetime.utcnow().isoformat())

        valores.extend([usuario_id, password_id])
        sql = f"""
            UPDATE passwords SET {', '.join(partes)}
            WHERE usuario_id = ? AND id = ?
        """
        cursor.execute(sql, tuple(valores))
        conn.commit()

def eliminar_password(usuario_id, password_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM passwords WHERE usuario_id = ? AND id = ?
        """, (usuario_id, password_id))
        conn.commit()

# --- Contraseñas por plataforma (PasswordManagerFrame) ---
def obtener_plataformas_usuario(usuario):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT plataforma FROM contrasenas_platform WHERE usuario = ?", (usuario,))
        rows = [r[0] for r in cursor.fetchall()]
        return rows

def obtener_logins_por_plataforma(usuario, plataforma):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT login FROM contrasenas_platform
            WHERE usuario = ? AND plataforma = ?
        """, (usuario, plataforma))
        return [r[0] for r in cursor.fetchall()]

def guardar_contrasena_usuario(usuario, plataforma, login, password):
    with get_connection() as conn:
        cursor = conn.cursor()
        now = datetime.utcnow().isoformat()
        try:
            cursor.execute("""
                INSERT INTO contrasenas_platform (usuario, plataforma, login, password, created_at)
                VALUES (?, ?, ?, ?, ?)
            """, (usuario, plataforma, login, password, now))
            conn.commit()
            return True
        except sqlite3.IntegrityError as e:
            # si choca por UNIQUE(usuario, plataforma, login)
            if "UNIQUE" in str(e):
                return False
            raise

def obtener_contrasenas_de_usuario(usuario):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT plataforma, login, password, created_at 
            FROM contrasenas_platform 
            WHERE usuario = ?
        """, (usuario,))
        rows = cursor.fetchall()
        return rows

def eliminar_contrasena_platform(usuario, plataforma, login):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM contrasenas_platform
            WHERE usuario = ? AND plataforma = ? AND login = ?
        """, (usuario, plataforma, login))
        conn.commit()
        return cursor.rowcount

# --- Llaves de recuperación ---
def crear_llave_recuperacion(usuario: str, longitud: int = 50_000) -> tuple[int, str]:
    import string, secrets
    alphabet = string.ascii_letters + string.digits + string.punctuation
    llave = ''.join(secrets.choice(alphabet) for _ in range(longitud))
    llave_encriptada = cifrar(llave)
    ahora = datetime.utcnow().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        # Intentar actualizar primero
        cursor.execute("""
            UPDATE recovery_keys 
            SET llave_encriptada = ?, creado_en = ?
            WHERE usuario = ?
        """, (llave_encriptada, ahora, usuario))
        if cursor.rowcount == 0:
            # No existía, insertar nuevo registro
            cursor.execute("""
                INSERT INTO recovery_keys (usuario, llave_encriptada, creado_en)
                VALUES (?, ?, ?)
            """, (usuario, llave_encriptada, ahora))
            key_id = cursor.lastrowid
        else:
            # Obtener id del registro actualizado
            cursor.execute("SELECT id FROM recovery_keys WHERE usuario = ?", (usuario,))
            key_id = cursor.fetchone()[0]
        conn.commit()
    return key_id, llave


def registrar_lectura_llave(recovery_key_id: int):
    with get_connection() as conn:
        cursor = conn.cursor()
        ahora = datetime.utcnow().isoformat()
        cursor.execute("""
            INSERT INTO recovery_key_reads (recovery_key_id, leido_en)
            VALUES (?, ?)
        """, (recovery_key_id, ahora))
        conn.commit()

def obtener_llave_recuperacion(usuario: str) -> list[dict]:
    """Devuelve todas las llaves generadas para un usuario (descifradas)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, llave_encriptada, creado_en FROM recovery_keys
            WHERE usuario = ?
            ORDER BY creado_en DESC
        """, (usuario,))
        rows = cursor.fetchall()
        result = []
        for row in rows:
            descifrada = descifrar(row[1])
            result.append({
                "id": row[0],
                "llave": descifrada,
                "creado_en": row[2]
            })
        return result
