# view/file_content_display.py

import customtkinter as ctk
from tkinter import ttk
import os

class FileContentDisplayWindow(ctk.CTkToplevel):
    def __init__(self, parent, file_name, content, controller):
        """
        Inisialisasi jendela untuk menampilkan isi file.

        Args:
            parent (ctk.CTk): Induk dari jendela ini.
            file_name (str): Nama file yang akan ditampilkan.
            content (str): Konten dari file.
            controller (PlagiarismController): Instance dari controller untuk mengakses pengaturan.
        """
        super().__init__(parent)
        self.parent = parent
        self.file_name = file_name
        self.content = content
        self.controller = controller

        self.title(f"Isi File: {self.file_name}")
        self.geometry("900x600")

        self.setup_ui()

    def setup_ui(self):
        # Label judul
        title_label = ctk.CTkLabel(
            self,
            text=f"Isi File: {self.file_name}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)

        # Frame untuk teks
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget untuk menampilkan isi file
        text_widget = ctk.CTkTextbox(text_frame, wrap="none")
        text_widget.pack(side="left", fill="both", expand=True)
        text_widget.insert("1.0", self.content)
        text_widget.configure(state="disabled")  # Tidak bisa diedit

        # Atur font sesuai tipe file
        self.set_programming_font(text_widget, self.file_name)

        # Scrollbar sinkron vertikal
        sync_scroll_verticalbar = ctk.CTkScrollbar(text_frame, command=text_widget.yview)
        sync_scroll_verticalbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=sync_scroll_verticalbar.set)

        # Scrollbar horizontal
        sync_scrollbar_horizontal = ctk.CTkScrollbar(self, command=text_widget.xview, orientation="horizontal")
        sync_scrollbar_horizontal.pack(side="bottom", fill="x")
        text_widget.configure(xscrollcommand=sync_scrollbar_horizontal.set)

    def set_programming_font(self, widget, filepath):
        """
        Mengatur font widget teks berdasarkan ekstensi file.

        Args:
            widget (CTkTextbox): Widget teks yang akan diatur font-nya.
            filepath (str): Path lengkap ke file.
        """
        ext = os.path.splitext(filepath)[1].lower()
        if ext in self.controller.file_reader.programming_extensions:
            widget.configure(font=("Consolas", 12))
        else:
            widget.configure(font=("Open Sans", 12))
