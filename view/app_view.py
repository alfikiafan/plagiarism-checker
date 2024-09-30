# /view/app_view.py

import customtkinter as ctk
from tkinter import filedialog, ttk
from controller.plagiarism_controller import PlagiarismController
import pandas as pd
import os
import difflib

class PlagiarismApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.controller = PlagiarismController()
        self.title("Pengecek Plagiasi")
        self.geometry("510x300")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.setup_ui()

    def setup_ui(self):
        # Label utama
        main_label = ctk.CTkLabel(self, text="Pengecek Plagiasi", font=ctk.CTkFont(size=18, weight="bold"))
        main_label.pack(pady=5)

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

        # Tombol untuk memulai pengecekan plagiasi
        process_button = ctk.CTkButton(self, text="Mulai Pengecekan", command=self.start_process)
        process_button.pack(pady=10)

        # Kotak keterangan hasil
        self.result_frame = ctk.CTkFrame(self, fg_color="#2B2B2B")
        self.result_frame.pack(fill="x", padx=10, pady=5)

        self.result_label = ctk.CTkLabel(self.result_frame, text="", wraplength=500)
        self.result_label.pack(padx=5, pady=5)

    def browse_files(self):
        file_paths = filedialog.askopenfilenames(
            title="Pilih 2 atau lebih file", 
            filetypes=[("Supported files", 
                        "*.txt;*.docx;*.pdf;*.py;*.java;*.c;*.cpp;*.h;*.hpp;*.cs;*.js;*.html;*.css;*.php;*.sql;*.rb;*.pl;*.sh;*.swift;*.kt;*.go;*.rs;*.lua;*.r;*.m;*.json;*.xml;*.yaml;*.yml;*.ini;*.cfg;*.conf;*.md;*.rst;*.csv;*.tsv;*.xls;*.xlsx;*.ppt;*.pptx;*.odt;*.ods;*.odp")]
        )
        if len(file_paths) < 2:
            self.result_label.configure(text="Pastikan memilih setidaknya dua file.")
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
        files = self.file_entry.get().split(', ')
        output_file = self.output_entry.get()

        try:
            threshold = float(self.threshold_entry.get())
            max_reduction = float(self.max_reduction_entry.get())
        except ValueError:
            self.result_label.configure(text="Threshold dan pengurangan maksimal harus berupa angka.")
            return

        if not files or len(files) < 2:
            self.result_label.configure(text="Silakan pilih minimal dua file untuk diperiksa.")
            return

        if not output_file:
            self.result_label.configure(text="Silakan pilih lokasi untuk menyimpan hasil.")
            return

        try:
            # Proses plagiasi dan clustering
            df_similarity, df_reduction, error_files = self.controller.process_files(files, threshold, max_reduction)
            
            if error_files:
                error_messages = "\n".join([f"{os.path.basename(k)}: {v}" for k, v in error_files.items()])
                self.result_label.configure(text=f"Beberapa file gagal dibaca:\n{error_messages}")
            else:
                self.result_label.configure(text=f"Output berhasil disimpan ke {output_file}")
            
            # Step 1: Baca konten file
            files_content = self.controller.files_content  # Konten file sudah dibaca di controller

            # Step 2: Cluster file berdasarkan konten file
            file_cluster_mapping = self.controller.cluster_files_by_content(files_content)

            # Step 3: Tambahkan kolom 'Cluster' ke df_similarity berdasarkan 'File 1'
            df_similarity['Cluster'] = df_similarity['File 1'].apply(lambda x: file_cluster_mapping.get(os.path.basename(x), 'N/A'))

            # Tampilkan hasil pada window baru
            self.show_output_window(df_similarity, df_reduction, output_file)
        except Exception as e:
            self.result_label.configure(text=str(e))

    def show_output_window(self, df_similarity, df_reduction, output_file):
        # Simpan hasil ke Excel
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_reduction.to_excel(writer, sheet_name='Pengurangan Nilai', index=False)
                df_similarity.to_excel(writer, sheet_name='Kesamaan', index=False)
        except Exception as e:
            self.result_label.configure(text=f"Error menyimpan file Excel: {e}")
            return

        # Membuat jendela baru untuk menampilkan hasil
        output_window = ctk.CTkToplevel(self)
        output_window.title("Hasil Pengecekan Plagiasi")
        output_window.geometry("800x600")
        output_window.attributes("-topmost", True)

        # Tabel 1: Persentase Kesamaan
        similarity_label = ctk.CTkLabel(output_window, text="Persentase Kesamaan", font=ctk.CTkFont(size=18, weight="bold"))
        similarity_label.pack(pady=5)

        similarity_frame = ctk.CTkFrame(output_window)
        similarity_frame.pack(pady=5, padx=10, fill="both", expand=True)

        similarity_scroll = ctk.CTkScrollbar(similarity_frame, orientation='vertical')
        similarity_scroll.pack(side="right", fill="y")

        # Kolom dengan cluster ditambahkan
        similarity_columns = ["File 1", "File 2", "Kesamaan (%)", "Cluster"]
        similarity_table = ttk.Treeview(similarity_frame, columns=similarity_columns, show='headings', height=8, yscrollcommand=similarity_scroll.set)

        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        rowheight=35,
                        fieldbackground="#343638",
                        bordercolor="#343638",
                        borderwidth=0,
                        font=('Segoe UI', 14))
        style.map('Treeview', background=[('selected', '#22559b')])

        style.configure("Treeview.Heading",
                        background="#565b5e",
                        foreground="white",
                        relief="flat",
                        font=('Segoe UI', 14))
        style.map("Treeview.Heading", background=[('active', '#3484F0')])

        similarity_scroll.configure(command=similarity_table.yview)

        # Set header untuk tabel dengan cluster
        for col in similarity_columns:
            similarity_table.heading(col, text=col)
            similarity_table.column(col, anchor='center', width=150)

        # Menampilkan data ke tabel
        for index, row in df_similarity.iterrows():
            similarity_table.insert('', 'end', values=list(row))

        similarity_table.pack(fill="both", expand=True)

        # Tabel 2: Pengurangan Nilai
        reduction_label = ctk.CTkLabel(output_window, text="Pengurangan Nilai", font=ctk.CTkFont(size=18, weight="bold"))
        reduction_label.pack(pady=5)

        reduction_frame = ctk.CTkFrame(output_window)
        reduction_frame.pack(pady=5, padx=10, fill="both", expand=True)

        reduction_scroll = ctk.CTkScrollbar(reduction_frame, orientation='vertical')
        reduction_scroll.pack(side="right", fill="y")

        reduction_columns = [str(col) for col in df_reduction.columns]
        reduction_table = ttk.Treeview(reduction_frame, columns=reduction_columns, show='headings', height=8, yscrollcommand=reduction_scroll.set)

        reduction_scroll.configure(command=reduction_table.yview)

        for col in reduction_columns:
            reduction_table.heading(col, text=col)
            reduction_table.column(col, anchor='center', width=150)

        for index, row in df_reduction.iterrows():
            reduction_table.insert('', 'end', values=list(row))

        reduction_table.pack(fill="both", expand=True)

        # Event double click untuk menampilkan perbandingan teks
        similarity_table.bind("<Double-1>", lambda event: self.compare_texts(event, df_similarity))

    def compare_texts(self, event, df_similarity):
        selected_item = event.widget.selection()
        if not selected_item:
            return

        # Ambil nama file dari baris yang dipilih
        item = event.widget.item(selected_item)
        file1, file2 = item['values'][0], item['values'][1]

        # Dapatkan teks dari controller
        try:
            content1 = self.controller.get_file_content(file1)
            content2 = self.controller.get_file_content(file2)
        except Exception as e:
            self.result_label.configure(text=f"Error saat mengambil konten file: {e}")
            return

        # Buat jendela baru untuk menampilkan perbandingan teks
        comparison_window = ctk.CTkToplevel(self)
        comparison_window.title(f"Perbandingan: {file1} vs {file2}")
        comparison_window.geometry("900x600")

        comparison_window.attributes("-topmost", True)

        # Label judul
        title_label = ctk.CTkLabel(comparison_window, text=f"Perbandingan: {file1} vs {file2}", font=ctk.CTkFont(size=18, weight="bold"))
        title_label.pack(pady=10)

        # Frame untuk teks
        text_frame = ctk.CTkFrame(comparison_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame kiri untuk file 1
        text1_frame = ctk.CTkFrame(text_frame)
        text1_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Text widget untuk menampilkan teks file 1
        text1_widget = ctk.CTkTextbox(text1_frame, wrap="none")
        text1_widget.pack(side="left", fill="both", expand=True)
        text1_widget.insert("1.0", content1)
        text1_widget.configure(state="disabled")  # Tidak bisa diedit

        # Atur font sesuai tipe file
        self.set_programming_font(text1_widget, file1)

        # Frame kanan untuk file 2
        text2_frame = ctk.CTkFrame(text_frame)
        text2_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Text widget untuk menampilkan teks file 2
        text2_widget = ctk.CTkTextbox(text2_frame, wrap="none")
        text2_widget.pack(side="left", fill="both", expand=True)
        text2_widget.insert("1.0", content2)
        text2_widget.configure(state="disabled")  # Tidak bisa diedit

        # Atur font sesuai tipe file
        self.set_programming_font(text2_widget, file2)

        # Scrollbar sinkron untuk kedua teks
        sync_scroll_verticalbar = ctk.CTkScrollbar(text_frame, command=lambda *args: self.sync_scroll_vertical(text1_widget, text2_widget, *args))
        sync_scroll_verticalbar.pack(side="right", fill="y")

        # Menghubungkan yscrollcommand kedua widget ke scrollbar sinkron
        text1_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))
        text2_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))

        # Scrollbar horizontal sinkron di luar frame teks (di bawah kedua widget teks)
        sync_scrollbar_horizontal = ctk.CTkScrollbar(comparison_window, command=lambda *args: self.sync_scroll_horizontal(text1_widget, text2_widget, *args), orientation="horizontal")
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
            widget.configure(font=("Consolas", 12))  # Set font Consolas untuk file kode
        else:
            widget.configure(font=("Open Sans", 12))  # Default font jika bukan file kode

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
