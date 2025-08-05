import customtkinter as ctk
from PIL import Image
import webbrowser
from gui.colors import *
from gui.route import *

class SupportFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_FONDO_SECUNDARIO())
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Título / agradecimiento
        ctk.CTkLabel(
            self,
            text="¡Gracias por usar esta aplicación!",
            font=("Orbitron", 28, "bold"),
            text_color="white"
        ).pack(pady=(30, 5))

        ctk.CTkLabel(
            self,
            text="Tu apoyo ayuda a mantener y mejorar PyKey.",
            font=("Orbitron", 16),
            text_color="white"
        ).pack(pady=(0, 15))

        ctk.CTkLabel(
            self,
            text="Si quisieras apoyar este proyecto, hazlo en:",
            font=("Orbitron", 18),
            text_color="white"
        ).pack(pady=(10, 20))    

        # Contenedor centrado para el botón de Patreon
        boton_frame = ctk.CTkFrame(self, fg_color="transparent")
        boton_frame.pack(pady=10)
        boton_frame.place(relx=0.5, rely=0.5, anchor="n")

        ctk.CTkLabel(
            self,
            text="PATREON",
            font=("Orbitron", 20, "bold"),
            text_color="white"
        ).place(relx=0.44, rely=0.42)

        # Cargar logo de Patreon
        patreon_img = None
        try:
            patreon_img = ctk.CTkImage(Image.open(resource_path("assets/PATREON.png")), size=(64, 64))
        except Exception:
            pass

        btn_patreon = ctk.CTkButton(
            boton_frame,
            text="",
            image=patreon_img,
            width=100,
            height=100,
            corner_radius=50,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=lambda: webbrowser.open_new_tab("https://www.patreon.com/MrS0t0"),
        )
        btn_patreon.pack()

        # Pie de página pequeño
        ctk.CTkLabel(
            self,
            text="Cada aporte, por pequeño que sea, cuenta.",
            font=("Orbitron", 12),
            text_color="gray70"
        ).pack(side="bottom", pady=10)
