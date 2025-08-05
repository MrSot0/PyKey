import customtkinter as ctk
from customtkinter import CTkImage
from gui.colors import *
from gui.user import UsuarioContentFrame
from gui.version import Version
from PIL import Image
import db.db as db_manager
from gui.kp import KP
from gui.key import PasswordsListFrame
from gui.developer import DeveloperFrame
from gui.support import SupportFrame
from gui.config import SettingsFrame
import os
from gui.config_manager import *
from gui.route import *


class FramePrincipal(ctk.CTkFrame):
    def __init__(self, master, cambiar_frame, usuario_info=None, **kwargs):
        super().__init__(master, **kwargs)

        self.configuracion = cargar_config()

        self.sidebar_visible = True
        self.cambiar_frame = cambiar_frame
        self.usuario_info = usuario_info or {}
        
        self.bar_menu_icon = CTkImage(Image.open(resource_path("assets/BAR_MENU_WHITE.png")), size=(24, 24))
        self.local_icon = CTkImage(Image.open(resource_path("assets/FIND_WHITE.png")), size=(24, 24))

        nombre = self.usuario_info.get("nombre", "Usuario")
        usuario = self.usuario_info.get("usuario", "")

        master.pack_configure(fill="both", expand=True, padx=0, pady=0)

         # Sidebar y usuario
        self.sidebar_container = ctk.CTkFrame(self, fg_color=COLOR_PRINCIPAL(), corner_radius=0)
        self.sidebar_container.pack(side="left", fill="both", padx=0, pady=0)
        self.user_container = ctk.CTkFrame(self.sidebar_container, fg_color=COLOR_FONDO_SECUNDARIO(), corner_radius=0, width=250, height=200)
        self.user_container.pack(side="top", pady=0)
        self.user_container.pack_propagate(False)

        default_image = resource_path("assets/user.png")
        imagen_guardada = self.usuario_info[5] if self.usuario_info and len(self.usuario_info) > 5 else None
        self.user_icon_path = self._extraer_ruta_imagen()
        self.user_icon = CTkImage(Image.open(self.user_icon_path), size=(80, 80))

        self.user_content_inner = ctk.CTkFrame(self.user_container, fg_color="transparent")
        self.user_content_inner.pack(fill="both", expand=True)
        self.user_content_inner.grid_rowconfigure(0, weight=1)
        self.user_content_inner.grid_columnconfigure(0, weight=1)

        self.boton_user = ctk.CTkButton(
            self.user_content_inner,
            image=self.user_icon,
            text="",
            fg_color=COLOR_HOVER(),
            hover_color=COLOR_HOVER(),
            corner_radius=100,
            width=50,
            height=50,
            border_width=0
        )
        self.boton_user.grid(row=0, column=0)

        self.user_label = ctk.CTkLabel(
            self.user_container,
            text=f"{usuario}",
            font=("Orbitron", 21, "bold"),
            text_color="white",
            fg_color=COLOR_HOVER(),
            height=50,
            width=250
        )
        self.user_label.pack(side="bottom", padx=0, pady=0)
        self.user_label.pack_propagate(False)

        # Sidebar de navegación
        self.sidebar = ctk.CTkFrame(self.sidebar_container, width=250, fg_color=COLOR_FONDO_SECUNDARIO(), corner_radius=0)
        self.sidebar.pack(side="top", fill="both", expand=True, padx=1, pady=1)
        self.sidebar.pack_propagate(False)

         # Contenido principal
        self.content_container = ctk.CTkFrame(self, fg_color=COLOR_PRINCIPAL(), corner_radius=0)
        self.content_container.pack(side="right", fill="both", expand=True, padx=0, pady=0)

        self.top_bar = ctk.CTkFrame(self.content_container, fg_color=COLOR_PRINCIPAL(), corner_radius=0)
        self.top_bar.pack(side="top", fill="x", padx=10, pady=10)

        self.toggle_button = ctk.CTkButton(
            self.top_bar,
            image=self.bar_menu_icon,
            text="",
            command=self.toggle_sidebar,
            width=40,
            height=40,
            corner_radius=5,
            fg_color=COLOR_FONDO_SECUNDARIO(),
            text_color="black",
            hover_color="gray20"
        )
        self.toggle_button.grid(row=0, column=0, padx=(0, 20), pady=5, sticky="w")

        self.entry_busqueda = ctk.CTkEntry(
            self.top_bar,
            placeholder_text="Buscar contraseña...",
            width=200,
            height=40,
            fg_color=COLOR_FONDO_SECUNDARIO(),
            font=("Orbitron", 14),
            text_color="white",
            corner_radius=5,
        )
        self.entry_busqueda.grid(row=0, column=1, pady=5, sticky="ew")

        self.botones_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.botones_frame.grid(row=0, column=2, padx=5, pady=5)

        self.boton_buscar_local = ctk.CTkButton(
            self.botones_frame,
            image=self.local_icon,
            text="",
            width=40,
            height=40,
            fg_color=COLOR_FONDO_SECUNDARIO(),
            corner_radius=5,
            command=self._on_buscar_click,
            hover_color="gray20"
        )
        self.boton_buscar_local.pack(side="left", padx=5)

        self.top_bar.grid_columnconfigure(1, weight=1)

        self.content = ctk.CTkFrame(self.content_container, fg_color=COLOR_FONDO(), corner_radius=0)
        self.content.pack(side="top", fill="both", expand=True, padx=1, pady=1)

        # Botones de sección
        self.opciones_sidebar = ["Mis Claves", "Crear", "Usuario", "Configuracion", "Desarrollador", "Apoyar / Donar", "VERSION", "Salir"]
        self.botones_sidebar = {}
        color_normal = COLOR_FONDO()
        fuente_normal = ("Orbitron", 20)

        for opcion in self.opciones_sidebar:
            boton = ctk.CTkButton(
                self.sidebar,
                width=100,
                height=57,
                text=opcion,
                command=lambda op=opcion: self.seleccionar_boton(op, usuario),
                fg_color=color_normal,
                font=fuente_normal,
                corner_radius=0,
                hover_color=COLOR_GRIS_OSCURO()
            )
            boton.pack(pady=0, fill="x")
            self.botones_sidebar[opcion] = boton


    def on_logout(self):
        self.cambiar_frame("login")

    def cerrar(self):
        pass

    def toggle_sidebar(self):
        if self.sidebar_visible:
            self.sidebar_container.pack_forget()
            self.sidebar_visible = False
        else:
            self.sidebar_container.pack(side="left", fill="both")
            self.sidebar_visible = True

    def seleccionar_boton(self, nombre, usuario):
        # Colores y fuentes
        color_normal = COLOR_FONDO()
        color_activo = COLOR_HOVER()
        fuente_normal = ("Orbitron", 20)
        fuente_activo = ("Orbitron", 20, "bold")

        # Si es "Salir", corta aquí
        if nombre == "Salir":
            self.on_logout()
            # actualizar UI de botones igual para mostrar el activo
            for opcion, boton in self.botones_sidebar.items():
                if opcion == nombre:
                    boton.configure(fg_color=color_activo, font=fuente_activo, hover_color=color_activo)
                else:
                    boton.configure(fg_color=color_normal, font=fuente_normal, hover_color=COLOR_GRIS_OSCURO())
            self.boton_activo = nombre
            return

        # Limpiar área de contenido
        for widget in self.content.winfo_children():
            widget.forget()

        # Dependiendo de la sección, mostrar algo
        if nombre == "Configuracion":
            frame = SettingsFrame(
                self.content,
                settings=self.configuracion,
                on_save_callback=self._actualizar_configuracion
            )
            frame.pack(fill="both", expand=True, padx=20, pady=20)

        elif nombre == "Usuario":
            usuario_frame = UsuarioContentFrame(
                self.content,
                usuario_info=self.usuario_info,
                actualizar_imagen_callback=self.actualizar_imagen_sidebar,
                cambiar_nombre_callback=getattr(self, "abrir_cambiar_nombre", None),
                cambiar_contrasena_callback=getattr(self, "abrir_cambiar_contrasena", None)
            )
            usuario_frame.pack(fill="both", expand=True)

        elif nombre == "Mis Claves":
            frame = PasswordsListFrame(
                self.content,
                usuario_activo=usuario,
                )
            frame.pack(fill="both", expand=True, padx=20, pady=20)
            self.passwords_frame = frame 

            self.entry_busqueda.bind(
                "<KeyRelease>",
                lambda e: getattr(self, "passwords_frame", None) and self.passwords_frame.aplicar_filtro(self.entry_busqueda.get())
            )

        elif nombre == "Desarrollador":
            frame = DeveloperFrame(self.content)
            frame.pack(fill="both", expand=True, padx=20, pady=20)
        elif nombre == "Crear":
            frame = KP(
                self.content,
                usuario_activo=usuario,
                volver_callback=lambda: self.seleccionar_boton("Mis Claves", usuario)
                )
            frame.pack(fill="both", expand=True, padx=20, pady=20)

        elif nombre == "Apoyar / Donar":
            frame = SupportFrame(self.content)
            frame.pack(fill="both", expand=True, padx=20, pady=20)

        elif nombre == "VERSION":
            version_frame = Version(
                self.content,
                usuario_activo=usuario
                )
            version_frame.pack(fill="both", expand=True, padx=20, pady=20)
        else:
            frame = ctk.CTkLabel(
                self.content,
                text=f"Sección: {nombre}",
                text_color="white",
                font=("Orbitron", 18)
            )
            frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Resalta el botón activo y restaura los demás
        for opcion, boton in self.botones_sidebar.items():
            if opcion == nombre:
                boton.configure(fg_color=color_activo, font=fuente_activo, hover_color=color_activo)
            else:
                boton.configure(fg_color=color_normal, font=fuente_normal, hover_color=COLOR_GRIS_OSCURO())

        self.boton_activo = nombre

    def actualizar_imagen_sidebar(self, nueva_ruta):
        # 1. Persistir en la base de datos
        usuario = self.usuario_info.get("usuario") if isinstance(self.usuario_info, dict) else self.usuario_info[3]
        db_manager.actualizar_imagen_usuario(usuario, nueva_ruta)

        # 2. Actualizar la copia local
        if isinstance(self.usuario_info, dict):
            self.usuario_info["imagen"] = nueva_ruta
        else:
            info = list(self.usuario_info)
            while len(info) <= 5:
                info.append(None)
            info[5] = nueva_ruta
            self.usuario_info = tuple(info)

        # 3. Refrescar sidebar
        default_image = resource_path("assets/user.png")
        ruta = nueva_ruta if nueva_ruta and os.path.exists(nueva_ruta) else default_image
        self.user_icon = CTkImage(Image.open(resource_path(ruta)), size=(80, 80))
        self.boton_user.configure(image=self.user_icon)

    def _extraer_ruta_imagen(self):
        default_image = "assets/user.png"
        if isinstance(self.usuario_info, dict):
            imagen = self.usuario_info.get("imagen") or default_image
        elif isinstance(self.usuario_info, (list, tuple)):
            imagen = self.usuario_info[5] if len(self.usuario_info) > 5 and self.usuario_info[5] else default_image
        else:
            imagen = default_image

        return resource_path(imagen if os.path.exists(imagen) else default_image)


    def _on_buscar_click(self):
        query = self.entry_busqueda.get().strip()
        if hasattr(self, "passwords_frame"):
            self.passwords_frame.aplicar_filtro(query)
        else:
            self.seleccionar_boton("Mis Claves", self.usuario_info.get("usuario", ""))
            if hasattr(self, "passwords_frame"):
                self.passwords_frame.aplicar_filtro(query)

    def _actualizar_configuracion(self, nueva_config):
        self.configuracion = nueva_config
        # Aplicar tema y color base
        set_theme(color_base=nueva_config.get("color_base"), modo=nueva_config.get("modo"))

        # Actualizar colores
        self.configure(fg_color=COLOR_PRINCIPAL())
        self.content_container.configure(fg_color=COLOR_PRINCIPAL())
        self.sidebar_container.configure(fg_color=COLOR_PRINCIPAL())
        self.sidebar.configure(fg_color=COLOR_FONDO_SECUNDARIO())
        self.boton_user.configure(fg_color=COLOR_HOVER(), hover_color=COLOR_HOVER())
        self.top_bar.configure(fg_color=COLOR_PRINCIPAL())
        self.user_label.configure(fg_color=COLOR_HOVER())
        self.master.configure(fg_color=COLOR_PRINCIPAL())
        self.configure(fg_color=COLOR_PRINCIPAL())


        if hasattr(self, "boton_activo") and self.boton_activo:
            usuario = self.usuario_info.get("usuario") if isinstance(self.usuario_info, dict) else None
            self.seleccionar_boton(self.boton_activo, usuario)
