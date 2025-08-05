import customtkinter as ctk
from tkinter import messagebox, scrolledtext
from gui.colors import COLOR_PRINCIPAL, COLOR_HOVER
from datetime import datetime
from db.db import crear_llave_recuperacion, registrar_lectura_llave
import os

class RecoveryKeyPopup(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)
        self.title("Llave de recuperación")
        self.geometry("700x600")
        self.usuario = usuario

        ctk.CTkLabel(self, text="Llave de recuperación", font=("Orbitron", 24, "bold")).pack(pady=(10,5))
        ctk.CTkLabel(
            self,
            text="Esta llave te permitirá recuperar tu cuenta. Guárdala en un lugar seguro.",
            wraplength=650,
            justify="left",
            font=("Orbitron", 14)
        ).pack(padx=10, pady=(0,10))

        # Generar y guardar en DB
        key_id, llave = crear_llave_recuperacion(self.usuario)

        # Mostrar llave (solo lectura)
        self.text_area = scrolledtext.ScrolledText(self, wrap="word", height=20)
        self.text_area.insert("1.0", llave)
        self.text_area.configure(state="disabled")
        self.text_area.pack(fill="both", expand=True, padx=10, pady=10)

        # Registrar que se mostró / leyó
        registrar_lectura_llave(key_id)

        # Botones
        botones_frame = ctk.CTkFrame(self, fg_color="transparent")
        botones_frame.pack(pady=10)

        def copiar():
            try:
                self.clipboard_clear()
                self.clipboard_append(llave)
                messagebox.showinfo("Copiado", "Llave copiada al portapapeles.")
            except Exception:
                messagebox.showerror("Error", "No se pudo copiar.")

        def guardar_en_archivo():
            nombre = f"recovery_key_{self.usuario}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.txt"
            ruta = nombre
            try:
                with open(ruta, "w", encoding="utf-8") as f:
                    f.write(llave)
                messagebox.showinfo("Guardado", f"Llave guardada en archivo:\n{os.path.abspath(ruta)}")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

        btn_copy = ctk.CTkButton(botones_frame, text="Copiar", command=copiar, font=("Orbitron", 14, "bold"), fg_color=COLOR_PRINCIPAL(), hover_color=COLOR_HOVER())
        btn_copy.pack(side="left", padx=10)
        btn_file = ctk.CTkButton(botones_frame, text="Guardar como archivo", font=("Orbitron", 14, "bold"), command=guardar_en_archivo, fg_color=COLOR_PRINCIPAL(), hover_color=COLOR_HOVER())
        btn_file.pack(side="left", padx=10)

        ctk.CTkButton(self, text="Cerrar", command=self.destroy, font=("Orbitron", 14, "bold"), fg_color=COLOR_PRINCIPAL(), hover_color=COLOR_HOVER()).pack(pady=(0,10))
