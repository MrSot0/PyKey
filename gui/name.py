import customtkinter as ctk
from PIL import Image
from gui.colors import *
from tkinter import messagebox
import db.db as db_manager


class CambiarNombreFrame(ctk.CTkFrame):
    def __init__(self, master, volver_callback, usuario_activo, cambiar_nombre_callback):
        super().__init__(master, fg_color="gray10")
        self.pack(fill="both", expand=True, padx=20, pady=20)

        self.volver_callback = volver_callback
        self.usuario_activo = usuario_activo
        self.cambiar_nombre_callback = cambiar_nombre_callback

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
            command=self.volver
        )
        self.btn_volver.pack(anchor="nw", pady=10, padx=10)

        ctk.CTkLabel(
            self, text="Cambiar Nombre", font=("Orbitron", 20, "bold"), text_color="white"
        ).pack(pady=20)

        # Frame decorativo para el contenido
        self.campos_frame = ctk.CTkFrame(
            self, fg_color=COLOR_FONDO(), corner_radius=10, width=420, height=152
        )
        self.campos_frame.pack(pady=10, padx=20)
        self.campos_frame.pack_propagate(False)

        entry_width = 350
        entry_height = 40
        font_entry = ("Orbitron", 16)

        self.nombre_entry = ctk.CTkEntry(
            self.campos_frame,
            placeholder_text="Nuevo nombre",
            width=entry_width,
            height=entry_height,
            font=font_entry
        )
        self.nombre_entry.pack(pady=(20, 5), padx=20)

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
        self.btn_guardar.pack(pady=20, padx=20)

    def volver(self):
        if callable(self.volver_callback):
            self.volver_callback()

    def guardar(self):
        nuevo_nombre = self.nombre_entry.get().strip()
        if not nuevo_nombre:
            messagebox.showerror("Error", "El nombre no puede estar vacío")
            return

        # Actualiza en la BD
        try:
            db_manager.actualizar_nombre_usuario(self.usuario_activo, nuevo_nombre)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar el nombre: {str(e)}")
            return

        messagebox.showinfo("Éxito", f"Nombre actualizado a: {nuevo_nombre}")
        # Llama callback con el nuevo nombre
        if callable(self.cambiar_nombre_callback):
            self.cambiar_nombre_callback(nuevo_nombre)
        self.volver()
