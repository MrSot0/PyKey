import customtkinter as ctk
from gui.colors import *
from gui.config_manager import *
from gui.route import *

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master, settings=None, on_save_callback=None):
        super().__init__(master, fg_color=COLOR_FONDO_SECUNDARIO())
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.settings = settings or {
            "idioma": "Español",
            "modo": "oscuro",
            "color_base": "azul",
            "atajos": True
        }
        self.on_save_callback = on_save_callback

        ctk.CTkLabel(self, text="Configuración", font=("Orbitron", 28, "bold"), text_color="white").pack(pady=20)

        form = ctk.CTkFrame(self, fg_color="transparent")
        form.pack(fill="x")

        # Idioma
        ctk.CTkLabel(form, text="Idioma:", font=("Orbitron", 16, "bold"), text_color="white").grid(row=0, column=0, sticky="w", pady=10, padx=10)
        self.idioma_var = ctk.StringVar(value=self.settings.get("idioma", "Español"))
        self.idioma_menu = ctk.CTkOptionMenu(
            form, 
            values=["Español"], 
            variable=self.idioma_var, 
            fg_color="gray20", 
            font=("Orbitron", 14, "bold"),
            button_color=COLOR_PRINCIPAL(),
            button_hover_color=COLOR_HOVER()
            )
        self.idioma_menu.grid(row=0, column=1, sticky="ew", padx=10)

        # Tema
        ctk.CTkLabel(form, text="Tema:", font=("Orbitron", 16, "bold"), text_color="white").grid(row=1, column=0, sticky="w", pady=10, padx=10)
        self.tema_var = ctk.StringVar(value=self.settings.get("modo", "oscuro"))
        self.tema_menu = ctk.CTkOptionMenu(
            form,
            values=["oscuro"], 
            variable=self.tema_var, 
            fg_color="gray20", 
            font=("Orbitron", 14, "bold"),
            button_color=COLOR_PRINCIPAL(),
            button_hover_color=COLOR_HOVER()
            )
        self.tema_menu.grid(row=1, column=1, sticky="ew", padx=10)

        # Color base
        ctk.CTkLabel(form, text="Color base:", font=("Orbitron", 16, "bold"), text_color="white").grid(row=2, column=0, sticky="w", pady=10, padx=10)
        self.color_var = ctk.StringVar(value=self.settings.get("color_base", "azul"))
        self.color_menu = ctk.CTkOptionMenu(
            form, 
            values=["verde", "azul", "rojo", "naranja"], 
            font=("Orbitron", 14, "bold"), 
            variable=self.color_var, 
            fg_color="gray20",
            button_color=COLOR_PRINCIPAL(),
            button_hover_color=COLOR_HOVER()
        )
        self.color_menu.grid(row=2, column=1, sticky="ew", padx=10)


        # Botón guardar
        btn_guardar = ctk.CTkButton(self, text="Guardar configuración", font=("Orbitron", 16, "bold"), command=self._guardar, fg_color=COLOR_PRINCIPAL(), hover_color=COLOR_HOVER())
        btn_guardar.pack(pady=30, ipadx=10, ipady=10)
        form.grid_columnconfigure(1, weight=1)

    def _guardar(self):
        # Leer valores actuales del formulario
        nueva_config = {
            "idioma": self.idioma_var.get(),
            "modo": self.tema_var.get(),
            "color_base": self.color_var.get(),
            #"atajos": self.atajos_var.get()
        }
        # Guardar en archivo JSON
        guardar_config(nueva_config)

        # Llamar callback para que lo reciba el frame principal y aplique cambios si quiere
        if callable(self.on_save_callback):
            self.on_save_callback(nueva_config)