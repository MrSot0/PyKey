import customtkinter as ctk
from PIL import Image
from gui.colors import *
from tkinter import messagebox
import db.db as db_manager
from gui.route import *

class CambiarContrasenaFrame(ctk.CTkFrame):
    def __init__(self, master, volver_callback, usuario_activo):
        super().__init__(master, fg_color="gray10")
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.usuario_activo = usuario_activo
        self.volver_callback = volver_callback

        # Icono de volver
        self.icon_back = ctk.CTkImage(Image.open(resource_path("assets/LEFT_WHITE.png")), size=(48, 48))
        self.btn_volver = ctk.CTkButton(
            self,
            image=self.icon_back,
            text="",
            width=40,
            height=40,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.volver  # usa directamente el callback almacenado
        )
        self.btn_volver.pack(anchor="nw", pady=10, padx=10)

        ctk.CTkLabel(
            self, text="Cambiar Contraseña", font=("Orbitron", 20, "bold"), text_color="white"
        ).pack(pady=20)

        # Frame decorativo
        self.campos_frame = ctk.CTkFrame(self, fg_color=COLOR_FONDO(), corner_radius=10, width=420, height=255)
        self.campos_frame.pack(pady=10, padx=20)
        self.campos_frame.pack_propagate(False)

        entry_width = 350
        entry_height = 40
        font_entry = ("Orbitron", 16)

        # Contraseña actual
        self.actual_entry = ctk.CTkEntry(
            self.campos_frame,
            placeholder_text="Contraseña actual",
            show="*",
            width=entry_width,
            height=entry_height,
            font=font_entry
        )
        self.actual_entry.pack(pady=(20, 5), padx=20)

        # Nueva contraseña
        self.contra_entry = ctk.CTkEntry(
            self.campos_frame,
            placeholder_text="Nueva contraseña",
            show="*",
            width=entry_width,
            height=entry_height,
            font=font_entry
        )
        self.contra_entry.pack(pady=5, padx=20)

        # Confirmar
        self.confirmar_entry = ctk.CTkEntry(
            self.campos_frame,
            placeholder_text="Confirmar contraseña",
            show="*",
            width=entry_width,
            height=entry_height,
            font=font_entry
        )
        self.confirmar_entry.pack(pady=5, padx=20)

        # Botón guardar
        self.btn_guardar = ctk.CTkButton(
            self.campos_frame,
            text="Guardar",
            width=entry_width,
            height=45,
            font=("Orbitron", 18, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.guardar
        )
        self.btn_guardar.pack(pady=(20,10), padx=20)

    def volver(self):
        # llama al callback original para regresar
        if callable(self.volver_callback):
            self.volver_callback()

    def validar_password(self, password):
        if len(password) < 8:
            return False, "La contraseña debe tener al menos 8 caracteres"
        if not any(c.isupper() for c in password):
            return False, "Debe contener al menos una mayúscula"
        if not any(c.isdigit() for c in password):
            return False, "Debe contener al menos un número"
        return True, ""

    def guardar(self):
        actual = self.actual_entry.get().strip()
        nueva = self.contra_entry.get().strip()
        confirmar = self.confirmar_entry.get().strip()

        if not all([actual, nueva, confirmar]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Verificar contraseña actual en base de datos
        usuario_en_bd = db_manager.obtener_usuario(self.usuario_activo, actual)
        if not usuario_en_bd:
            messagebox.showerror("Error", "La contraseña actual es incorrecta")
            return

        if nueva != confirmar:
            messagebox.showerror("Error", "La nueva contraseña y su confirmación no coinciden")
            return

        es_valida, mensaje = self.validar_password(nueva)
        if not es_valida:
            messagebox.showerror("Error en contraseña", mensaje)
            return

        # Actualizar en la base de datos
        db_manager.actualizar_contrasena_usuario(self.usuario_activo, nueva)
        messagebox.showinfo("Éxito", "Contraseña actualizada correctamente")
        self.volver()
