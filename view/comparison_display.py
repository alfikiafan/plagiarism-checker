# view/comparison_display.py

import customtkinter as ctk
from tkinter import ttk
import difflib
import os

from utils.constants import ASCENDING_ARROW, DESCENDING_ARROW


class ComparisonDisplayWindow(ctk.CTkToplevel):
    def __init__(self, parent, file1, file2, controller):
        """
        Inisialisasi jendela perbandingan teks antara dua file.

        Args:
            parent (ctk.CTk): Induk dari jendela ini.
            file1 (str): Path lengkap ke file pertama.
            file2 (str): Path lengkap ke file kedua.
            controller (PlagiarismController): Instance dari controller untuk mengakses konten file.
        """
        super().__init__(parent)
        self.parent = parent
        self.file1 = file1
        self.file2 = file2
        self.controller = controller

        self.title(f"Perbandingan: {os.path.basename(file1)} vs {os.path.basename(file2)}")
        self.geometry("900x600")
        self.lift()

        self.setup_ui()

    def setup_ui(self):
        # Label judul
        title_label = ctk.CTkLabel(
            self,
            text=f"Perbandingan: {os.path.basename(self.file1)} vs {os.path.basename(self.file2)}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)

        # Frame untuk teks
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame kiri untuk file 1
        text1_frame = ctk.CTkFrame(text_frame)
        text1_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Text widget untuk menampilkan teks file 1
        text1_widget = ctk.CTkTextbox(text1_frame, wrap="none")
        text1_widget.pack(side="left", fill="both", expand=True)
        content1 = self.controller.get_file_content(self.file1)
        text1_widget.insert("1.0", content1)
        text1_widget.configure(state="disabled")  # Tidak bisa diedit

        # Atur font sesuai tipe file
        self.set_programming_font(text1_widget, self.file1)

        # Frame kanan untuk file 2
        text2_frame = ctk.CTkFrame(text_frame)
        text2_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Text widget untuk menampilkan teks file 2
        text2_widget = ctk.CTkTextbox(text2_frame, wrap="none")
        text2_widget.pack(side="left", fill="both", expand=True)
        content2 = self.controller.get_file_content(self.file2)
        text2_widget.insert("1.0", content2)
        text2_widget.configure(state="disabled")  # Tidak bisa diedit

        # Atur font sesuai tipe file
        self.set_programming_font(text2_widget, self.file2)

        # Scrollbar sinkron untuk kedua teks
        sync_scroll_verticalbar = ctk.CTkScrollbar(text_frame, command=lambda *args: self.sync_scroll_vertical(text1_widget, text2_widget, *args))
        sync_scroll_verticalbar.pack(side="right", fill="y")

        # Menghubungkan yscrollcommand kedua widget ke scrollbar sinkron
        text1_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))
        text2_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))

        # Scrollbar horizontal sinkron di luar frame teks (di bawah kedua widget teks)
        sync_scrollbar_horizontal = ctk.CTkScrollbar(self, command=lambda *args: self.sync_scroll_horizontal(text1_widget, text2_widget, *args), orientation="horizontal")
        sync_scrollbar_horizontal.pack(side="bottom", fill="x")

        # Menghubungkan xscrollcommand kedua widget ke scrollbar horizontal sinkron
        text1_widget.configure(xscrollcommand=lambda *args: sync_scrollbar_horizontal.set(*args))
        text2_widget.configure(xscrollcommand=lambda *args: sync_scrollbar_horizontal.set(*args))

        # Highlight bagian yang sama
        self.highlight_similarities(text1_widget, text2_widget, content1, content2)

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

    def sync_scroll_vertical(self, text1_widget, text2_widget, *args):
        """
        Mensinkronkan scroll vertikal kedua widget teks.

        Args:
            text1_widget (CTkTextbox): Widget teks pertama.
            text2_widget (CTkTextbox): Widget teks kedua.
            *args: Argument tambahan untuk yview.
        """
        text1_widget.yview(*args)
        text2_widget.yview(*args)

    def sync_scroll_horizontal(self, text1_widget, text2_widget, *args):
        """
        Mensinkronkan scroll horizontal kedua widget teks.

        Args:
            text1_widget (CTkTextbox): Widget teks pertama.
            text2_widget (CTkTextbox): Widget teks kedua.
            *args: Argument tambahan untuk xview.
        """
        text1_widget.xview(*args)
        text2_widget.xview(*args)

    def highlight_similarities(self, text1_widget, text2_widget, text1, text2):
        """
        Menyorot bagian yang sama antara dua teks menggunakan difflib.

        Args:
            text1_widget (CTkTextbox): Widget teks pertama.
            text2_widget (CTkTextbox): Widget teks kedua.
            text1 (str): Konten teks pertama.
            text2 (str): Konten teks kedua.
        """
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)

        for match in sequence_matcher.get_matching_blocks():
            start1, start2, length = match
            if length > 0:
                # Highlight di teks 1 dengan warna #4B5632
                text1_widget.tag_add("highlight", f"1.0+{start1}c", f"1.0+{start1+length}c")
                text1_widget.tag_config("highlight", background="#4B5632", foreground="white")

                # Highlight di teks 2 dengan warna yang sama
                text2_widget.tag_add("highlight", f"1.0+{start2}c", f"1.0+{start2+length}c")
                text2_widget.tag_config("highlight", background="#4B5632", foreground="white")
