import customtkinter as ctk
from PIL import Image
import webbrowser
import os

from gui.colors import *
from gui.route import *

class DeveloperFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=COLOR_FONDO_SECUNDARIO())
        self.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        ctk.CTkLabel(
            self,
            text="Desarrollador",
            font=("Orbitron", 30, "bold"),
            text_color="white"
        ).pack(pady=(10, 10))

        # Credito
        ctk.CTkLabel(
            self,
            text="Este programa fue desarrollado por MrSot0",
            font=("Orbitron", 18),
            text_color="white"
        ).pack(pady=(0, 5))

        # Más proyectos
        ctk.CTkLabel(
            self,
            text="Más proyectos en:",
            font=("Orbitron", 20, "bold"),
            text_color="white"
        ).pack(pady=(20, 5))

        proyectos_frame = ctk.CTkFrame(self, fg_color="transparent", width=100,
            height=100,)
        proyectos_frame.pack(pady=5)

        # GitHub button
        github_img = None
        try:
            github_img = ctk.CTkImage(Image.open(resource_path("assets/GITHUB.png")), size=(64, 64))
        except Exception:
            pass
        btn_github = ctk.CTkButton(
            proyectos_frame,
            text="",
            image=github_img,
            compound="left",
            font=("Orbitron", 20, "bold"),
            width=32,
            height=32,
            corner_radius=32,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=lambda: webbrowser.open_new_tab("https://github.com/MrSot0") 
        )
        btn_github.pack(side="left", padx=10, pady=(10,0))

        # Sección Social Media
        ctk.CTkLabel(
            self,
            text="Social Media",
            font=("Orbitron", 20, "bold"),
            text_color="white"
        ).pack(pady=(50, 10))

        social_frame = ctk.CTkFrame(self, fg_color="transparent")
        social_frame.pack(pady=5)

        # Instagram
        insta_img = None
        try:
            insta_img = ctk.CTkImage(Image.open(resource_path("assets/INSTAGRAM.png")), size=(64, 64))
        except Exception:
            pass
        btn_insta = ctk.CTkButton(
            social_frame,
            text="",
            image=insta_img,
            compound="left",
            font=("Orbitron", 14),
            width=32,
            height=32,
            corner_radius=32,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=lambda: webbrowser.open_new_tab("https://instagram.com/mrsot0?igsh=OHhqdWR3ODNyMnVz") 
        )
        btn_insta.pack(side="left", padx=10)

        # TikTok
        tiktok_img = None
        try:
            tiktok_img = ctk.CTkImage(Image.open(resource_path("assets/TIKTOK.png")), size=(64, 64))
        except Exception:
            pass
        btn_tiktok = ctk.CTkButton(
            social_frame,
            text="",
            image=tiktok_img,
            compound="left",
            font=("Orbitron", 14),
            width=32,
            height=32,
            corner_radius=32,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=lambda: webbrowser.open_new_tab("https://www.tiktok.com/@mrsot0")  
        )
        btn_tiktok.pack(side="left",padx=10)

        # Telegram
        telegram_img = None
        try:
            telegram_img = ctk.CTkImage(Image.open(resource_path("assets/TELEGRAM.png")), size=(64, 64))
        except Exception:
            pass
        btn_telegram = ctk.CTkButton(
            social_frame,
            text="",
            image=telegram_img,
            compound="left",
            font=("Orbitron", 14),
            width=32,
            height=32,
            corner_radius=32,
            fg_color=COLOR_PRINCIPAL(),
            hover_color=COLOR_HOVER(),
            command=lambda: webbrowser.open_new_tab("https://t.me/Mr_Sot0")  
        )
        btn_telegram.pack(side="left", padx=10)

        # Footer
        ctk.CTkLabel(
            self,
            text="Gracias por usar la aplicación.",
            font=("Orbitron", 12),
            text_color="gray70"
        ).pack(side="bottom", pady=10)
