import customtkinter as ctk
from PIL import Image
from tkinter import filedialog
import os

from gui.colors import *
from gui.name import CambiarNombreFrame
from gui.password import CambiarContrasenaFrame
from gui.recovery import RecoveryKeyPopup
from gui.route import *

class UsuarioContentFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        usuario_info,
        actualizar_imagen_callback,
        cambiar_nombre_callback,
        cambiar_contrasena_callback,
    ):
        super().__init__(master, fg_color=COLOR_FONDO_SECUNDARIO())

        self.usuario_info = usuario_info
        self.actualizar_imagen_callback = actualizar_imagen_callback
        self.cambiar_nombre_callback = cambiar_nombre_callback
        self.cambiar_contrasena_callback = cambiar_contrasena_callback

        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Extraer campos con seguridad, soportando tupla/lista o dict
        if isinstance(self.usuario_info, (list, tuple)):
            usuario_id = self.usuario_info[0] if len(self.usuario_info) > 0 else ""
            nombre = self.usuario_info[1] if len(self.usuario_info) > 1 else ""
            usuario = self.usuario_info[3] if len(self.usuario_info) > 3 else ""
            imagen_ruta = self.usuario_info[5] if len(self.usuario_info) > 5 and self.usuario_info[5] else None
        elif isinstance(self.usuario_info, dict):
            usuario_id = self.usuario_info.get("id", "")
            nombre = self.usuario_info.get("nombre", "")
            usuario = self.usuario_info.get("usuario", "")
            imagen_ruta = self.usuario_info.get("imagen", None)
        else:
            usuario_id = ""
            nombre = ""
            usuario = ""
            imagen_ruta = None

        if not imagen_ruta:
            imagen_ruta = resource_path("assets/user.png")
        if not os.path.exists(imagen_ruta):
            imagen_ruta = resource_path("assets/user.png")

        self.imagen_usuario = ctk.CTkImage(Image.open(imagen_ruta), size=(120, 120))
        self.imagen_label = ctk.CTkButton(
            self,
            image=self.imagen_usuario,
            text="",
            width=130,
            height=130,
            corner_radius=65,
            fg_color="transparent",
            hover_color="gray20",
            command=self.cambiar_imagen,
        )
        self.imagen_label.pack(pady=15)

        # --- DATOS ---
        self.label_id = ctk.CTkLabel(
            self, text=f"ID: {usuario_id}", text_color="white", font=("Orbitron", 16)
        )
        self.label_id.pack(pady=5)

        self.label_nombre = ctk.CTkLabel(
            self, text=f"Nombre: {nombre}", text_color="white", font=("Orbitron", 16)
        )
        self.label_nombre.pack(pady=5)

        self.label_usuario = ctk.CTkLabel(
            self, text=f"Usuario: {usuario}", text_color="white", font=("Orbitron", 16)
        )
        self.label_usuario.pack(pady=5)

        # Íconos
        self.icon_edit = ctk.CTkImage(Image.open(resource_path("assets/EDIT_WHITE.png")), size=(50, 50))
        self.icon_lock = ctk.CTkImage(Image.open(resource_path("assets/LOCK_WHITE.png")), size=(50, 50))
        self.icon_recuperacion = ctk.CTkImage(Image.open(resource_path("assets/KEY.png")), size=(50, 50))

        # --- BOTONES apilados verticalmente y centrados ---
        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.pack(pady=10)

        # Cambiar Nombre
        self.btn_cambiar_nombre = ctk.CTkButton(
            botones_frame,
            text="Cambiar Nombre",
            image=self.icon_edit,
            compound="left",
            width=300,
            height=30,
            font=("Orbitron", 16, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.abrir_cambiar_nombre,
        )
        self.btn_cambiar_nombre.pack(pady=8, padx=10, fill="x")

        # Cambiar Contraseña
        self.btn_cambiar_contra = ctk.CTkButton(
            botones_frame,
            text="Cambiar Contraseña",
            image=self.icon_lock,
            compound="left",
            width=300,
            height=30,
            font=("Orbitron", 16, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.abrir_cambiar_contrasena,
        )
        self.btn_cambiar_contra.pack(pady=8, padx=10, fill="x")

        # Pase de Recuperación
        self.btn_pase_recuperacion = ctk.CTkButton(
            botones_frame,
            text="Special Key",
            image=self.icon_recuperacion,
            compound="left",
            width=300,
            height=30,
            font=("Orbitron", 16, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.abrir_pase_recuperacion,  # placeholder: define este método
        )
        self.btn_pase_recuperacion.pack(pady=8, padx=10, fill="x")

    def cambiar_imagen(self):
        nueva_ruta = filedialog.askopenfilename(
            filetypes=[("Imagen", "*.png;*.jpg;*.jpeg")]
        )
        if not nueva_ruta:
            return

        # 1. Callback externo (actualiza DB y/o sidebar)
        if callable(self.actualizar_imagen_callback):
            self.actualizar_imagen_callback(nueva_ruta)

        # 2. Actualiza la copia local de usuario_info (manteniendo tupla o dict)
        if isinstance(self.usuario_info, (list, tuple)):
            info_lista = list(self.usuario_info)
            while len(info_lista) <= 5:
                info_lista.append(None)
            info_lista[5] = nueva_ruta
            self.usuario_info = tuple(info_lista)
        elif isinstance(self.usuario_info, dict):
            self.usuario_info["imagen"] = nueva_ruta

        # 3. Refresca la imagen en UI
        self.imagen_usuario = ctk.CTkImage(Image.open(nueva_ruta), size=(120, 120))
        self.imagen_label.configure(image=self.imagen_usuario)

    def abrir_cambiar_nombre(self):
        for widget in self.master.winfo_children():
            widget.forget()
        CambiarNombreFrame(
            self.master,
            volver_callback=self.volver_a_usuario,
            usuario_activo=self._get_usuario_activo(),
            cambiar_nombre_callback=self.actualizar_nombre_usuario,
        ).pack(fill="both", expand=True)

    def abrir_cambiar_contrasena(self):
        for widget in self.master.winfo_children():
            widget.forget()
        CambiarContrasenaFrame(
            self.master,
            volver_callback=self.volver_a_usuario,
            usuario_activo=self._get_usuario_activo(),
        ).pack(fill="both", expand=True)

    def abrir_pase_recuperacion(self):
        usuario_activo = self._get_usuario_activo()
        popup = RecoveryKeyPopup(self, usuario=usuario_activo)
        popup.grab_set()  # modal

    def volver_a_usuario(self):
        for widget in self.master.winfo_children():
            widget.forget()
        UsuarioContentFrame(
            self.master,
            self.usuario_info,
            self.actualizar_imagen_callback,
            self.cambiar_nombre_callback,
            self.cambiar_contrasena_callback,
        ).pack(fill="both", expand=True)

    def actualizar_nombre_usuario(self, nuevo_nombre):
        if isinstance(self.usuario_info, (list, tuple)):
            info = list(self.usuario_info)
            if len(info) > 1:
                info[1] = nuevo_nombre
            else:
                while len(info) <= 1:
                    info.append("")
                info[1] = nuevo_nombre
            self.usuario_info = tuple(info)
        elif isinstance(self.usuario_info, dict):
            self.usuario_info["nombre"] = nuevo_nombre

        try:
            self.label_nombre.configure(text=f"Nombre: {nuevo_nombre}")
        except Exception:
            pass

    def _get_usuario_activo(self):
        if isinstance(self.usuario_info, (list, tuple)):
            return self.usuario_info[3] if len(self.usuario_info) > 3 else ""
        elif isinstance(self.usuario_info, dict):
            return self.usuario_info.get("usuario", "")
        return ""


# P?)ink-=}Ge@78\T{#eL$*>QB;64SY9&