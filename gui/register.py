import customtkinter as ctk
from tkinter import messagebox
import db.db as db_manager
from gui.colors import *

class FrameRegistro(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame, theme=None):
        super().__init__(
            master,
            width=700,
            height=650,
            fg_color=COLOR_FONDO(),
            border_width=3,
            border_color=COLOR_BORDE(),
            corner_radius=15
        )

        self.marco_decorativo = ctk.CTkFrame(
            self,
            width=400,
            height=600,
            fg_color=COLOR_FONDO_SECUNDARIO(),
            border_width=2,
            border_color=COLOR_BORDE(),
            corner_radius=15
        )


        self.cambiar_frame = cambiar_frame

        # Variables para los campos
        self.entry_nombre = None
        self.entry_email = None
        self.entry_usuario = None
        self.entry_password = None

        self.crear_formulario()

    def validar_password(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not any(c.isupper() for c in password):
            return False, "Debe contener al menos una mayúscula"
        if not any(c.isdigit() for c in password):
            return False, "Debe contener al menos un número"
        return True, ""

    def crear_campo(self, marco, texto_label, placeholder, es_password=False, ancho=300):
        PAD_X = 50    # margen lateral
        PAD_Y = 15     # espacio vertical entre campos

        frame_campo = ctk.CTkFrame(marco, fg_color="transparent")
        frame_campo.pack(fill="x", padx=PAD_X, pady=(PAD_Y, 0))

        # Label encima del campo de entrada
        label = ctk.CTkLabel(
            frame_campo,
            text=texto_label,
            font=("Orbitron", 14, "bold"),
            anchor="w",           # alineado a la izquierda
            text_color=COLOR_TEXTO_CLARO()
        )
        label.pack(anchor="w", pady=(0, 4))  # ligero espacio debajo del label

        entry = ctk.CTkEntry(
            frame_campo,
            placeholder_text=placeholder,
            width=ancho,
            show="*" if es_password else None,
            font=("Orbitron", 12),
            fg_color=COLOR_GRIS_OSCURO(),
            border_color=COLOR_BORDE_SUAVE(),
            text_color=COLOR_TEXTO_CLARO()
        )
        entry.pack(fill="x")

        return entry



    def registrar_usuario(self):
        nombre = self.entry_nombre.get().strip()
        usuario = self.entry_usuario.get().strip()
        password = self.entry_password.get().strip()

        if not all([nombre, usuario, password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        es_valida, mensaje = self.validar_password(password)
        if not es_valida:
            messagebox.showerror("Error en contraseña", mensaje)
            return

        try:
            print(f"[DEBUG] Insertando: {nombre}, {usuario}, {password}")
            db_manager.insertar_usuario(nombre, usuario, password)
            messagebox.showinfo("Éxito", "¡Usuario registrado correctamente!")
            self.limpiar_campos()
            self.cambiar_frame("login")
        except Exception as e:
            messagebox.showerror("Error en registro", str(e))

    def limpiar_campos(self):
        for entry in [self.entry_nombre, self.entry_usuario, self.entry_password]:
            if entry:
                entry.delete(0, "end")

    def crear_formulario(self):
        titulo = ctk.CTkLabel(
            self,
            text="Registro",
            font=("Orbitron", 32, "bold"),
            text_color=COLOR_PRINCIPAL()
        )
        titulo.pack(pady=20)

        # Entradas
        self.entry_nombre = self.crear_campo(self, "Nombre completo", "Ej: PyKey")
        self.entry_usuario = self.crear_campo(self, "Nombre de usuario", "Ej: MrSot0")
        self.entry_password = self.crear_campo(self, "Contraseña", "Mínimo 8 caracteres", es_password=True)

        ctk.CTkButton(
            self,
            text="Registrarse",
            command=self.registrar_usuario,
            width=300,
            height=40,
            corner_radius=10,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            font=("Orbitron", 14, "bold")
        ).pack(pady=20)


        frame_enlace = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        frame_enlace.pack(pady=(0, 20), padx=40)

        ctk.CTkLabel(
            frame_enlace,
            text="¿Ya estás registrado?",
            font=("Orbitron", 14, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO()
        ).pack(side="left", padx=(0, 5))

        ctk.CTkButton(
            frame_enlace,
            text="Iniciar sesión",
            font=("Orbitron", 14, "underline"),
            fg_color="transparent",
            hover_color="gray20",
            text_color=COLOR_PRINCIPAL(),
            width=0,
            height=0,
            command=self.iniciar_sesion
        ).pack(side="left")

    def iniciar_sesion(self):
        self.cambiar_frame("login")
