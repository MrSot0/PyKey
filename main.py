import os
import sys
import json
import customtkinter as ctk
from tkinter import messagebox

import db.db as db_manager
from gui.login import FrameLogin
from gui.register import FrameRegistro
from gui.principal import FramePrincipal  
from gui.colors import *  
from gui.config_manager import cargar_config, guardar_config  
from gui.route import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Inicializa la base de datos
        db_manager.inicializar_db()

        # Ventana
        self.geometry("650x650")
        self.state("zoomed")
        self.minsize(650, 650)
        self.title("PyKey Beta 1.0.0")

        self.iconbitmap(resource_path("assets/icono.ico"))

        # Carga config
        self.config_data = cargar_config()

        # Aplica tema desde config (antes de construir UI)
        set_theme(color_base=self.config_data.get("color_base"), modo=self.config_data.get("modo"))

        # Fondo inicial acorde al tema
        self.configure(fg_color=COLOR_FONDO())

        # Frame contenedor
        self.current_frame = None
        self.restart_frame()

        # Hook para guardar al cerrar
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Inicio en login
        self.cargar_modulo("login")

    def restart_frame(self):
        if hasattr(self, "main_frame"):
            try:
                self.main_frame.forget()
            except Exception:
                pass
        self.main_frame = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO())
        self.main_frame.pack(fill="both", expand=True, padx=8, pady=8)

    def cargar_modulo(self, nombre_modulo, **kwargs):
        if hasattr(self, "current_frame") and self.current_frame is not None:
            if hasattr(self.current_frame, "cerrar"):
                try:
                    self.current_frame.cerrar()
                except Exception:
                    pass
            try:
                self.current_frame.destroy()
            except Exception:
                pass
            self.current_frame = None

        self.restart_frame()

        if nombre_modulo == "login":
            frame = FrameLogin(
                self.main_frame,
                cambiar_frame=self.cambiar_frame
            )
            frame.place(relx=0.5, rely=0.5, anchor="center")

        elif nombre_modulo == "registro":
            frame = FrameRegistro(
                self.main_frame,
                cambiar_frame=self.cambiar_frame
            )
            frame.place(relx=0.5, rely=0.5, anchor="center")

        elif nombre_modulo == "principal":
            usuario_info = kwargs.get("usuario_info")
            if usuario_info is None:
                messagebox.showerror("Error", "No se proporcionó información de usuario.")
                return
            # Pasar config y callback para persistir cambios desde el SettingsFrame dentro
            frame = FramePrincipal(
                self.main_frame,
                cambiar_frame=self.cambiar_frame,
                usuario_info=usuario_info
            )
            frame.configuracion = self.config_data  
            original_actualizar = frame._actualizar_configuracion

            def wrapped_actualizar(nueva_config):
                original_actualizar(nueva_config)
                self.actualizar_config(nueva_config)

            frame._actualizar_configuracion = wrapped_actualizar

            frame.pack(fill="both", expand=True, padx=0, pady=0)
        else:
            frame = ctk.CTkLabel(
                self.main_frame,
                text=f"Módulo '{nombre_modulo}' no encontrado.",
                text_color=COLOR_TEXTO_CLARO()
            )
            frame.pack(padx=20, pady=20)

        self.current_frame = frame

    def cambiar_frame(self, nombre_modulo, **kwargs):
        self.cargar_modulo(nombre_modulo, **kwargs)

    def actualizar_config(self, nueva_config):
        # actualizar y persistir
        self.config_data.update(nueva_config)
        try:
            guardar_config(self.config_data)
        except Exception as e:
            print("Error guardando config:", e)

    def _on_close(self):
        # Asegura que la config actual se guarda antes de cerrar
        try:
            guardar_config(self.config_data)
        except Exception:
            pass
        self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()
