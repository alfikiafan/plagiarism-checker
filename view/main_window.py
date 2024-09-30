# view/main_window.py

import customtkinter as ctk
from controller.plagiarism_controller import PlagiarismController
from view.file_selection import FileSelectionFrame
from view.results_display import ResultsFrame

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = PlagiarismController()
        self.title("Pengecek Plagiasi")
        self.geometry("510x350")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.sorting_order = {}
        self.setup_ui()

    def setup_ui(self):
        # Label utama
        main_label = ctk.CTkLabel(
            self, 
            text="Pengecek Plagiasi", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        main_label.pack(pady=5)

        # Frame untuk pemilihan file dan parameter
        self.file_selection = FileSelectionFrame(self, self.controller, self)
        self.file_selection.pack(pady=5, padx=10, fill="both", expand=True)

        # Tombol untuk memulai pengecekan
        process_button = ctk.CTkButton(
            self, 
            text="Mulai Pengecekan", 
            command=self.file_selection.start_process
        )
        process_button.pack(pady=10)

        # Frame untuk menampilkan hasil
        self.result_frame = ResultsFrame(self)
        self.result_frame.pack(fill="x", padx=10, pady=5)

    def update_result(self, message):
        self.result_frame.update_result(message)
