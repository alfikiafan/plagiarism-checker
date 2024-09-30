# view/file_selection.py

import threading
import time
import customtkinter as ctk
from tkinter import filedialog
from utils.constants import THRESHOLD_DEFAULT, MAX_REDUCTION_DEFAULT
import os

class FileSelectionFrame(ctk.CTkFrame):
    def __init__(self, parent, controller, main_window):
        super().__init__(parent)
        self.controller = controller
        self.main_window = main_window
        self.sorting_order = {}
        self.setup_ui()

    def setup_ui(self):
        # Frame untuk input
        frame = ctk.CTkFrame(self)
        frame.pack(pady=5, padx=10, fill="both", expand=True)

        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=0)

        # Input file (2 atau lebih)
        file_label = ctk.CTkLabel(frame, text="Pilih File:")
        file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_entry = ctk.CTkEntry(frame, placeholder_text="Path to files")
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        file_button = ctk.CTkButton(frame, text="Browse", command=self.browse_files)
        file_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Threshold persentase kesamaan
        threshold_label = ctk.CTkLabel(frame, text="Threshold Kesamaan (%)")
        threshold_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.threshold_entry = ctk.CTkEntry(frame, placeholder_text="80")
        self.threshold_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Pengurangan maksimal nilai
        max_reduction_label = ctk.CTkLabel(frame, text="Pengurangan Maksimal Nilai:")
        max_reduction_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.max_reduction_entry = ctk.CTkEntry(frame, placeholder_text="20")
        self.max_reduction_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Pilih lokasi output dengan tombol browse
        output_label = ctk.CTkLabel(frame, text="Pilih Lokasi Output:")
        output_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.output_entry = ctk.CTkEntry(frame, placeholder_text="Lokasi Output")
        self.output_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        output_button = ctk.CTkButton(frame, text="Browse", command=self.browse_output_location)
        output_button.grid(row=3, column=2, padx=5, pady=5, sticky="e")

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Pilih 2 atau lebih file", 
            filetypes=[("Supported files", 
                        "*.txt;*.docx;*.pdf;*.py;*.java;*.c;*.cpp;*.h;*.hpp;*.cs;*.js;*.html;*.css;*.php;*.sql;*.rb;*.pl;*.sh;*.swift;*.kt;*.go;*.rs;*.lua;*.r;*.m;*.json;*.xml;*.yaml;*.yml;*.ini;*.cfg;*.conf;*.md;*.rst;*.csv;*.tsv;*.xls;*.xlsx;*.ppt;*.pptx;*.odt;*.ods;*.odp")]
        )
        if len(file_paths) < 2:
            self.main_window.update_result("Pastikan memilih setidaknya dua file.")
            return
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, ', '.join(file_paths))

    def browse_output_location(self):
        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx", 
            filetypes=[("Excel files", "*.xlsx")], 
            title="Pilih lokasi dan nama file output"
        )
        if output_path:
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, output_path)

    def start_process(self):
        # Ubah kursor menjadi "watch" (atau "wait") dan segera perbarui tampilan
        self.main_window.config(cursor="watch")
        self.main_window.update()
        self.disable_widgets()

        # Fungsi untuk menjalankan proses pengecekan plagiasi
        def run_plagiarism_check():
            try:
                time.sleep(0.1)
                files = self.file_entry.get().split(', ')
                output_file = self.output_entry.get()

                threshold_value = self.threshold_entry.get()
                reduction_value = self.max_reduction_entry.get()

                if not threshold_value:
                    threshold = THRESHOLD_DEFAULT
                else:
                    try:
                        threshold = float(threshold_value)
                    except ValueError:
                        self.main_window.update_result("Threshold harus berupa angka.")
                        return

                if not reduction_value:
                    max_reduction = MAX_REDUCTION_DEFAULT
                else:
                    try:
                        max_reduction = float(reduction_value)
                    except ValueError:
                        self.main_window.update_result("Pengurangan maksimal harus berupa angka.")
                        return

                if not files or len(files) < 2:
                    self.main_window.update_result("Silakan pilih minimal dua file untuk diperiksa.")
                    return

                if not output_file:
                    self.main_window.update_result("Silakan pilih lokasi untuk menyimpan hasil.")
                    return

                # Proses plagiasi dan clustering
                df_similarity, df_reduction, error_files = self.controller.process_files(files, threshold, max_reduction)

                if error_files:
                    error_messages = "\n".join([f"{os.path.basename(k)}: {v}" for k, v in error_files.items()])
                    self.main_window.update_result(f"Beberapa file gagal dibaca:\n{error_messages}")
                else:
                    self.main_window.update_result(f"Output berhasil disimpan ke {output_file}")

                # Step 1: Baca konten file
                files_content = self.controller.files_content

                # Step 2: Cluster file berdasarkan konten file
                file_cluster_mapping = self.controller.cluster_files_by_content(files_content)

                # Step 3: Tambahkan kolom 'Cluster' ke df_similarity berdasarkan 'File 1'
                df_similarity['Cluster'] = df_similarity['File 1'].apply(lambda x: file_cluster_mapping.get(os.path.basename(x), 'N/A'))

                # Tampilkan hasil pada window baru
                self.main_window.result_frame.show_output_window(df_similarity, df_reduction, output_file, file_cluster_mapping)
                    
            except Exception as e:
                self.main_window.update_result(str(e))
            finally:
                self.main_window.config(cursor="")
                self.main_window.update()
                self.enable_widgets()

        # Jalankan proses dalam thread terpisah agar tidak memblokir GUI
        process_thread = threading.Thread(target=run_plagiarism_check)
        process_thread.start()

    def disable_widgets(self):
        """
        Men-disable semua widget di frame ini.
        """
        for widget in self.winfo_children():
            try:
                widget.configure(state="disabled")
            except:
                pass

    def enable_widgets(self):
        """
        Meng-enable semua widget di frame ini.
        """
        for widget in self.winfo_children():
            try:
                widget.configure(state="normal")
            except:
                pass
