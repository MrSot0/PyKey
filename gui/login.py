import customtkinter as ctk
from tkinter import messagebox
import db.db as db_manager
from gui.colors import *
from gui.setpass import RecoveryPasswordFrame

class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame):
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
        self.crear_formulario()
        link = ctk.CTkButton(self, text="¿Olvidaste tu contraseña?", fg_color="transparent", text_color=COLOR_PRINCIPAL(), hover_color="gray20", cursor="hand2", font=("Orbitron", 12, "underline"))
        link.pack(pady=(0,20))
        link.bind("<Button-1>", lambda e: self.abrir_recuperacion())

    def abrir_recuperacion(self):
        for widget in self.master.winfo_children():
            widget.forget()
        RecoveryPasswordFrame(
            self.master,
            volver_callback=lambda: self.cambiar_frame("login") 
        ).pack(fill="both", expand=True)

    def crear_formulario(self):
        """Función para crear la interfaz del formulario"""
        # Título
        titulo = ctk.CTkLabel(
            self,
            text="Iniciar Sesión",
            font=("Orbitron", 32, "bold"),
            text_color=COLOR_PRINCIPAL()
        )
        titulo.pack(pady=20)

        # Campos
        self.entry_usuario = self.crear_campo("Usuario", "Ingrese su usuario")
        self.entry_password = self.crear_campo("Contraseña", "Ingrese su contraseña", es_password=True)

        # Botón de Iniciar sesión
        ctk.CTkButton(
            self,
            text="Iniciar Sesión",
            command=self.login,
            width=300,
            height=40,
            corner_radius=10,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            font=("Orbitron", 14, "bold")
        ).pack(pady=20)

        # Enlace a registro
        frame_enlace = ctk.CTkFrame(self, fg_color="transparent")
        frame_enlace.pack(pady=(0, 20))
        
        ctk.CTkLabel(
            frame_enlace,
            text="¿Aún no te registras?",
            font=("Orbitron", 14, "bold"),
            text_color=COLOR_TEXTO_SECUNDARIO()
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            frame_enlace,
            text="Regístrate",
            font=("Orbitron", 14, "underline"),
            fg_color="transparent",
            hover_color="gray20",
            text_color=COLOR_PRINCIPAL(),
            width=0,
            height=0,
            command=lambda: self.cambiar_frame("registro")  # Cambia a registro
        ).pack(side="left")

    def crear_campo(self, texto_label, placeholder, es_password=False):
        frame_campo = ctk.CTkFrame(self, fg_color="transparent")
        frame_campo.pack(fill="x", padx=60, pady=10)
        
        ctk.CTkLabel(
            frame_campo,
            text=f"{texto_label}",
            font=("Orbitron", 14, "bold"),
            anchor="w",
            text_color=COLOR_TEXTO_CLARO()
        ).pack(fill="x")
        
        entry = ctk.CTkEntry(
            frame_campo,
            placeholder_text=placeholder,
            width=300,
            show="*" if es_password else None,
            font=("Orbitron", 12),
            fg_color=COLOR_GRIS_OSCURO(),
            border_color=COLOR_BORDE_SUAVE(),
            text_color=COLOR_TEXTO_CLARO()
        )
        entry.pack(fill="x")
        
        return entry


    def login(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if not all([usuario, password]):
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        usuario_db = db_manager.obtener_usuario(usuario, password)
        if usuario_db:
            self.cambiar_frame("principal", usuario_info=usuario_db)
            print(f"Login exitoso para {usuario}")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    