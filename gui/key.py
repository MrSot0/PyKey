import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import pyperclip  # pip install pyperclip
from datetime import datetime

from gui.colors import *
import db.db as db_manager
from gui.route import *

class PasswordsListFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        usuario_activo,  
        on_refresh_callback=None
    ):
        super().__init__(master, fg_color=COLOR_FONDO())
        self.usuario_activo = usuario_activo
        self.on_refresh_callback = on_refresh_callback

        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Scroll principal
        self.scrollable_frame = ctk.CTkScrollableFrame(self, fg_color="gray10", corner_radius=0)
        self.scrollable_frame.pack(fill="both", expand=True)

        self.reload()

    def clear_cards(self):
        for child in self.scrollable_frame.winfo_children():
            child.destroy()

    def reload(self):
        """Recarga desde la base de datos y reconstruye las cards."""
        self.clear_cards()
        try:
            filas = db_manager.obtener_contrasenas_de_usuario(self.usuario_activo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las contraseñas: {e}")
            return

        if not filas:
            empty = ctk.CTkLabel(self.scrollable_frame, text="No hay contraseñas guardadas.", font=("Orbitron", 16), text_color="white")
            empty.pack(pady=20)
            return

        for plataforma, login, password, created_at in filas:
            datos = {
                "plataforma": plataforma,
                "login": login,
                "password": password,
                "created_at": created_at
            }
            self.add_password_card(datos)

        if callable(self.on_refresh_callback):
            self.on_refresh_callback()

    def add_password_card(self, datos: dict):
        card = ctk.CTkFrame(self.scrollable_frame, fg_color="gray7", corner_radius=10)
        card.pack(fill="x", pady=10, padx=10)

        # Info textual
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Plataforma
        plat_lbl = ctk.CTkLabel(
            info_frame,
            text=datos.get("plataforma", ""),
            font=("Orbitron", 16, "bold"),
            text_color="white"
        )
        plat_lbl.pack(anchor="w")

        # Login
        login_lbl = ctk.CTkLabel(
            info_frame,
            text=f"Usuario: {datos.get('login','')}",
            font=("Orbitron", 14),
            text_color="gray80"
        )
        login_lbl.pack(anchor="w", pady=(2, 0))

        # Fecha
        created = datos.get("created_at", "")
        try:
            dt = datetime.fromisoformat(created)
            created_str = dt.strftime("%Y-%m-%d %H:%M")
        except Exception:
            created_str = created
        created_lbl = ctk.CTkLabel(
            info_frame,
            text=f"Creado: {created_str}",
            font=("Orbitron", 12),
            text_color="gray60"
        )
        created_lbl.pack(anchor="w", pady=(2, 0))

        # Contraseña oculta / mostrada
        pw_frame = ctk.CTkFrame(card, fg_color="transparent")
        pw_frame.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        pw_var = ctk.StringVar(value="*" * max(1, len(datos.get("password", ""))))
        showing = {"on": False}

        pw_entry = ctk.CTkEntry(
            pw_frame,
            textvariable=pw_var,
            font=("Orbitron", 14),
            state="readonly"
        )
        pw_entry.pack(fill="x", expand=True)

        # Botones de acción
        buttons_frame = ctk.CTkFrame(card, fg_color="transparent")
        buttons_frame.pack(side="right", padx=10, pady=10)

        # Mostrar / ocultar
        def toggle_password():
            if showing["on"]:
                pw_var.set("*" * max(1, len(datos.get("password", ""))))
                showing["on"] = False
            else:
                pw_var.set(datos.get("password", ""))
                showing["on"] = True

        self.icon_show = ctk.CTkImage(Image.open(resource_path("assets/SHOW_WHITE.png")), size=(30, 24))
        btn_toggle = ctk.CTkButton(
            buttons_frame,
            text="",
            image=self.icon_show,
            font=("Orbitron", 12, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            width=90,
            command=toggle_password
        )
        btn_toggle.pack(side="top", pady=4, anchor="e")

        # Copiar contraseña
        def copiar_pw():
            try:
                pyperclip.copy(datos.get("password", ""))
            except Exception:
                messagebox.showerror("Error", "No se pudo copiar la contraseña")

        self.icon_copy = ctk.CTkImage(Image.open(resource_path("assets/COPY_WHITE.png")), size=(24, 24))
        btn_copy = ctk.CTkButton(
            buttons_frame,
            text="",
            image=self.icon_copy,
            font=("Orbitron", 12, "bold"),
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            width=90,
            command=copiar_pw
        )

        btn_copy.pack(side="top", pady=4, anchor="e")

        # Eliminar
        def eliminar():
            confirm = messagebox.askyesno("Eliminar", f"¿Eliminar contraseña para '{datos.get('plataforma','')}'?")
            if not confirm:
                return
            try:
                db_manager.eliminar_contrasena_platform(self.usuario_activo, datos.get("plataforma", ""))
                self.reload()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

        self.icon_delete = ctk.CTkImage(Image.open(resource_path("assets/TRASH_WHITE.png")), size=(24, 24))

        btn_delete = ctk.CTkButton(
            buttons_frame,
            text="",
            image=self.icon_delete,
            font=("Orbitron", 12, "bold"),
            hover_color="#b30000",
            width=90,
            fg_color="red",
            command=eliminar
        )
        btn_delete.pack(side="top", pady=4, anchor="e")

    def aplicar_filtro(self, query: str):
        """Filtra por plataforma o login que contengan el query (case-insensitive)."""
        self.clear_cards()
        q = (query or "").strip().lower()
        try:
            filas = db_manager.obtener_contrasenas_de_usuario(self.usuario_activo)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar las contraseñas: {e}")
            return

        if not q:
            # sin filtro: recargar todo
            for plataforma, login, password, created_at in filas:
                self.add_password_card({
                    "plataforma": plataforma,
                    "login": login,
                    "password": password,
                    "created_at": created_at
                })
            if callable(self.on_refresh_callback):
                self.on_refresh_callback()
            return

        filtradas = []
        for plataforma, login, password, created_at in filas:
            if q in plataforma.lower() or q in login.lower():
                filtradas.append({
                    "plataforma": plataforma,
                    "login": login,
                    "password": password,
                    "created_at": created_at
                })

        if not filtradas:
            empty = ctk.CTkLabel(
                self.scrollable_frame,
                text="No hay contraseñas que coincidan con la búsqueda.",
                font=("Orbitron", 16, "bold"),
                text_color="white"
            )
            empty.pack(pady=250)
            return

        for datos in filtradas:
            self.add_password_card(datos)

        if callable(self.on_refresh_callback):
            self.on_refresh_callback()
