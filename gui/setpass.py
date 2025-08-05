import customtkinter as ctk
from tkinter import messagebox, filedialog
from gui.colors import *
from db import db as db_manager
import os
from PIL import Image
from gui.route import *

class RecoveryPasswordFrame(ctk.CTkFrame):
    def __init__(self, master, volver_callback):
        super().__init__(master, fg_color=COLOR_FONDO())
        self.volver_callback = volver_callback
        
        # Contenedor central
        self.container = ctk.CTkFrame(self, fg_color="transparent", width=150, height=300)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Header
        header_frame = ctk.CTkFrame(self.container, fg_color=COLOR_FONDO(), width=150, height=300)
        header_frame.pack(fill="x", pady=(0, 15))

        left_img_path = resource_path("assets/LEFT_WHITE.png")
        if os.path.exists(left_img_path):
            self.img_left = ctk.CTkImage(Image.open(left_img_path), size=(30, 30))
        else:
            self.img_left = None

        btn_volver = ctk.CTkButton(
            header_frame,
            image=self.img_left,
            text="",
            width=40,
            height=40,
            fg_color="transparent",
            hover_color=COLOR_HOVER(),
            corner_radius=10,
            command=self.volver_callback,
        )
        btn_volver.pack(side="left")

        titulo = ctk.CTkLabel(
            header_frame,
            text="Recuperar contraseña",
            font=("Orbitron", 24, "bold"),
            text_color="white",
        )
        titulo.pack(side="left", expand=True)

        # Área principal con fondo secundario
        self.main_frame = ctk.CTkFrame(self.container, fg_color=COLOR_FONDO_SECUNDARIO(), width=150, height=300)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        # --- Campos iniciales ---
        self.usuario_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.usuario_frame.pack(fill="x", pady=6)

        ctk.CTkLabel(
            self.usuario_frame,
            text="Usuario:",
            font=("Orbitron", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.usuario_entry_var = ctk.StringVar()
        self.usuario_entry = ctk.CTkEntry(
            self.usuario_frame,
            textvariable=self.usuario_entry_var,
            font=("Orbitron", 14),
            width=250
        )
        self.usuario_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.usuario_frame.grid_columnconfigure(1, weight=1)

        self.archivo_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.archivo_frame.pack(fill="x", pady=6)

        ctk.CTkLabel(
            self.archivo_frame,
            text="Archivo de llave:",
            font=("Orbitron", 14, "bold"),
            text_color="white"
        ).grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.ruta_llave_var = ctk.StringVar()
        self.llave_entry = ctk.CTkEntry(
            self.archivo_frame,
            textvariable=self.ruta_llave_var,
            state="readonly",
            font=("Orbitron", 14),
            width=250
        )
        self.llave_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)

        # Botón debajo del entry
        self.btn_browse = ctk.CTkButton(
            self.archivo_frame,
            text="Seleccionar archivo",
            command=self.seleccionar_archivo,
            font=("Orbitron", 14, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            width=250,     # Igual que entry
            height=40      # Similar al de cambiar contraseña
        )
        self.btn_browse.grid(row=1, column=0, columnspan=2, pady=(10, 5))

        self.archivo_frame.grid_columnconfigure(1, weight=1)

        # --- Área de restablecer, oculta inicialmente ---
        self.result_frame = ctk.CTkFrame(self.main_frame, fg_color=COLOR_FONDO_SECUNDARIO())
        self.new_pw_var = ctk.StringVar()
        self.confirm_pw_var = ctk.StringVar()

        self.label_new = ctk.CTkLabel(
            self.result_frame,
            text="Nueva contraseña:",
            font=("Orbitron", 14),
            text_color="white",
            width=150
        )
        self.entry_new = ctk.CTkEntry(
            self.result_frame,
            textvariable=self.new_pw_var,
            show="*",
            font=("Orbitron", 14),
            width=250
        )
        self.label_confirm = ctk.CTkLabel(
            self.result_frame,
            text="Confirmar contraseña:",
            font=("Orbitron", 14),
            text_color="white",
            width=150
        )
        self.entry_confirm = ctk.CTkEntry(
            self.result_frame,
            textvariable=self.confirm_pw_var,
            show="*",
            font=("Orbitron", 14),
            width=250
        )

        # Botón restablecer, oculto hasta verificación
        self.btn_reset = ctk.CTkButton(
            self.main_frame,
            text="Restablecer contraseña",
            command=self.restablecer_contrasena,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            font=("Orbitron", 14, "bold")
            )
        self.btn_reset.configure(state="disabled")  # inicialmente desactivado

        # Variables internas
        self.usuario_validado = None
        self.recovery_key_id = None

    def seleccionar_archivo(self):
        ruta = filedialog.askopenfilename(filetypes=[("Texto", "*.txt"), ("Todos", "*.*")])
        if ruta:
            self.ruta_llave_var.set(ruta)
            self.verificar_llave()

    def verificar_llave(self):
        usuario = self.usuario_entry_var.get().strip()
        ruta = self.ruta_llave_var.get()

        if not usuario:
            messagebox.showerror("Error", "Debes ingresar el usuario.")
            return
        if not ruta or not os.path.exists(ruta):
            messagebox.showerror("Error", "Debes seleccionar un archivo válido.")
            return

        # Verificar usuario en DB
        with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT usuario FROM usuarios WHERE usuario = ?", (usuario,))
            row = cursor.fetchone()
            if not row:
                messagebox.showerror("Error", f"El usuario '{usuario}' no existe.")
                return

        # Leer archivo
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")
            return

        llaves = []
        if hasattr(db_manager, "obtener_llave_recuperacion"):
            llaves = db_manager.obtener_llave_recuperacion(usuario)

        match = None
        for item in llaves:
            if item["llave"] == contenido:
                match = item
                break

        if not match:
            messagebox.showerror("Error", "La llave de recuperación no coincide con el usuario.")
            return

        # Validado: ocultar campos iniciales y mostrar restablecer
        self.usuario_validado = usuario
        self.recovery_key_id = match["id"]

        # Ocultar entrada de usuario/archivo/verificar
        self.usuario_frame.pack_forget()
        self.archivo_frame.pack_forget()
       
        # Mostrar formulario de nueva contraseña
        self.result_frame.pack(fill="x", pady=10)
        # organizar campos dentro de result_frame
        self.label_new.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_new.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        self.label_confirm.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_confirm.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.result_frame.grid_columnconfigure(1, weight=1)

        # Mostrar y habilitar botón reset
        self.btn_reset.pack(pady=(10, 5), ipadx=20, ipady=8)
        self.btn_reset.configure(state="normal")

        messagebox.showinfo("Verificado", "Llave válida. Ingresa nueva contraseña.")

    def restablecer_contrasena(self):
        pw = self.new_pw_var.get()
        confirm = self.confirm_pw_var.get()
        if not pw or not confirm:
            messagebox.showerror("Error", "Ambos campos de contraseña son obligatorios.")
            return
        if pw != confirm:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        if len(pw) < 8:
            messagebox.showerror("Error", "La contraseña debe tener al menos 8 caracteres.")
            return
        try:
            db_manager.actualizar_contrasena_usuario(self.usuario_validado, pw)
            messagebox.showinfo("Éxito", "Contraseña restablecida correctamente.")
            self.volver_callback()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar la contraseña: {e}")
