import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import string
import secrets
import datetime

from gui.colors import *
import db.db as db_manager 
from gui.route import *

class KP(ctk.CTkFrame):
    def __init__(self, master, usuario_activo, volver_callback=None):
        super().__init__(master, fg_color=COLOR_FONDO())
        self.usuario_activo = usuario_activo
        self.volver_callback = volver_callback

        try:
            db_manager.inicializar_db()
        except AttributeError:
            messagebox.showerror("Error", "Falta inicializar la base de datos correctamente.")
            return

        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Encabezado (Botón volver + título)
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))

        if self.volver_callback:
            self.icon_back = ctk.CTkImage(Image.open(resource_path("assets/LEFT_WHITE.png")), size=(48, 48))
            self.btn_volver = ctk.CTkButton(
                header_frame,
                image=self.icon_back,
                text="",
                width=40,
                height=40,
                fg_color=COLOR_PRINCIPAL(),
                hover_color=COLOR_HOVER(),
                command=self.volver_callback
            )
            self.btn_volver.pack(side="left", padx=(0, 10))

            ctk.CTkLabel(
                header_frame,
                text="Crear / Registrar Contraseña",
                font=("Orbitron", 24, "bold"),
                text_color="white",
                anchor="center"  # asegura que el texto se centre en el label
            ).pack(side="left", expand=True, fill="x")

        # Formulario
        form = ctk.CTkFrame(self, fg_color=COLOR_FONDO_SECUNDARIO(), corner_radius=10)
        form.pack(fill="x", padx=10, pady=10)

        # Plataforma
        ctk.CTkLabel(form, text="Plataforma", font=("Orbitron", 14), anchor="w").pack(fill="x", padx=15, pady=(10, 0))
        self.entry_plataforma = ctk.CTkEntry(form, placeholder_text="Ej: GitHub", font=("Orbitron", 14))
        self.entry_plataforma.pack(fill="x", padx=15, pady=10)

        # Usuario / Correo
        ctk.CTkLabel(form, text="Usuario / Correo", font=("Orbitron", 14), anchor="w").pack(fill="x", padx=15, pady=(10, 0))
        self.entry_login = ctk.CTkEntry(form, placeholder_text="ejemplo@correo.com", font=("Orbitron", 14))
        self.entry_login.pack(fill="x", padx=15, pady=10)

        # Longitud de contraseña
        ctk.CTkLabel(form, text="Longitud de contraseña (máx 64)", font=("Orbitron", 14), anchor="w").pack(fill="x", padx=15, pady=(10, 0))
        self.entry_length = ctk.CTkEntry(form, placeholder_text="32", font=("Orbitron", 14))
        self.entry_length.pack(fill="x", padx=15, pady=10)

        # Contraseña generada
        ctk.CTkLabel(form, text="Contraseña", font=("Orbitron", 14), anchor="w").pack(fill="x", padx=15, pady=(10, 0))
        gen_frame = ctk.CTkFrame(form, fg_color="transparent")
        gen_frame.pack(fill="x", padx=15, pady=10)

        self.generated_pw_var = ctk.StringVar()
        self.password_entry = ctk.CTkEntry(
            gen_frame,
            textvariable=self.generated_pw_var,
            placeholder_text="Contraseña generada",
            font=("Orbitron", 14),
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.btn_generar = ctk.CTkButton(
            gen_frame,
            text="Generar",
            font=("Orbitron", 14, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.generar_contrasena
        )
        self.btn_generar.pack(side="left", padx=5)

        # Mostrar/ocultar
        self.show_var = ctk.BooleanVar(value=False)
        self.chk_show = ctk.CTkCheckBox(form, text="Mostrar contraseña", variable=self.show_var, command=self._toggle_show)
        self.chk_show.pack(anchor="w", padx=15, pady=(5, 0))

        # Botón guardar (dentro de form)
        self.btn_guardar = ctk.CTkButton(
            form,
            text="Guardar contraseña",
            font=("Orbitron", 16, "bold"),
            width=300,
            height=50,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.guardar
        )
        self.btn_guardar.pack(fill="y", expand=True, pady=(0, 20))


    def _toggle_show(self):
        if self.show_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def generar_contrasena(self):
        length_str = self.entry_length.get().strip()
        if not length_str.isdigit():
            messagebox.showerror("Error", "La longitud debe ser un número válido")
            return
        length = int(length_str)
        if length <= 8 or length > 64:
            messagebox.showerror("Error", "La longitud debe estar entre 8 y 64")
            return

        alphabet = string.ascii_letters + string.digits + string.punctuation
        pw = "".join(secrets.choice(alphabet) for _ in range(length))
        self.generated_pw_var.set(pw)
        if not self.show_var.get():
            self.password_entry.configure(show="*")

    def guardar(self):
        plataforma = self.entry_plataforma.get().strip()
        login = self.entry_login.get().strip()
        password = self.generated_pw_var.get()

        if not plataforma or not login or not password:
            messagebox.showerror("Error", "Todos los campos son obligatorios y debe generarse una contraseña")
            return

        if len(password) > 64:
            messagebox.showerror("Error", "La contraseña no puede tener más de 64 caracteres")
            return

        # Validar que el login no se repita en esa plataforma para el usuario activo
        try:
            logins_existentes = db_manager.obtener_logins_por_plataforma(self.usuario_activo, plataforma)
        except AttributeError:
            messagebox.showerror("Error", "La función de consulta de logins por plataforma no está implementada.")
            return

        if login.lower() in (l.lower() for l in logins_existentes):
            messagebox.showerror("Error", f"El login '{login}' ya existe para la plataforma '{plataforma}'. Elige otro.")
            return

        # Guardar en DB
        try:
            ok = db_manager.guardar_contrasena_usuario(
                self.usuario_activo, plataforma, login, password
            )
            if not ok:
                messagebox.showerror("Error", "No se pudo guardar: ese login ya está registrado para esa plataforma.")
                return
        except AttributeError:
            messagebox.showerror("Error", "La función de guardado de contraseñas no está implementada.")
            return

        messagebox.showinfo("Éxito", f"Contraseña para '{plataforma}' con login '{login}' guardada.")
        self.entry_plataforma.delete(0, "end")
        self.entry_login.delete(0, "end")
        self.entry_length.delete(0, "end")
        self.generated_pw_var.set("")
        self.password_entry.configure(show="*")

