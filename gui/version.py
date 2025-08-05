import customtkinter as ctk
from PIL import Image
from gui.colors import *
from customtkinter import CTkImage

import webbrowser
import urllib.parse
from datetime import datetime
import traceback
from gui.route import *

class Version(ctk.CTkFrame):
    def __init__(self, master, usuario_activo):
        super().__init__(master, fg_color=COLOR_FONDO_SECUNDARIO())

        self.usuario_activo = usuario_activo

        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Imagen de carita
        carita_img = CTkImage(
            Image.open(resource_path("assets/FACE_WHITE.png")),
            size=(300, 300)
        )

        bug = CTkImage(
            Image.open(resource_path("assets/BUG.png")),
            size=(24, 24)
        )

        carita_label = ctk.CTkLabel(
            self,
            image=carita_img,
            text="",
            fg_color="transparent"
        )
        carita_label.pack(pady=(50, 10))

        # Texto de mensaje
        mensaje_label = ctk.CTkLabel(
            self,
            text="PyKey Beta v1.0.0",
            font=("Orbitron", 22, "bold"),
            text_color="white"
        )
        mensaje_label.pack()

        self.btn_bug = ctk.CTkButton(
            self,
            image=bug,
            text="Reportar un Bug",
            compound="left",
            font=("Orbitron", 12, "bold"),
            width=180,
            height=40,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=self.reporte_default
        )
        

        # Centrar todo
        self.pack_propagate(False)
        carita_label.place(relx=0.5, rely=0.45, anchor="center")
        mensaje_label.place(relx=0.5, rely=0.79, anchor="center")
        self.btn_bug.place(anchor="center", relx=0.5, rely=0.9)

    def reporte(
        self,
        destinatario: str,
        titulo: str,
        descripcion: str,
        usuario: str,
        nivel: str = "ERROR",
        extra_info: str | None = None
    ):
        """
        Abre Gmail con un correo prellenado para reportar el bug.
        """
        ahora = datetime.utcnow().isoformat()
        subject = f"[{nivel}] BUG: {titulo}"

        body_lines = [
            f"Fecha (UTC): {ahora}",
            f"Usuario afectado: {self.usuario_activo}",
            f"Nivel: {nivel}",
            "",
            "Descripción:",
            descripcion.strip()
        ]
        
        body_lines += [
            "",
            "Por favor, adjunta capturas si es necesario antes de enviar."
        ]

        body = "\n".join(body_lines)

        params = {
            "view": "cm",
            "fs": "1",
            "to": destinatario,
            "su": subject,
            "body": body
        }
        query = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        url = f"https://mail.google.com/mail/?{query}"
        webbrowser.open_new_tab(url)

    def reporte_default(self):

        # capturar una excepción reciente:
        try:
            raise RuntimeError("- Excepcion reciente")  
        except Exception:
            extra = traceback.format_exc()
            self.reporte(
                destinatario="mrs0t0reports@gmail.com",
                titulo="ERROR: [Escriba el error aca]",
                descripcion="Se detectó un fallo al: ",
                usuario=self.usuario_activo,
                nivel="CRITICAL",
                extra_info=extra
            )
