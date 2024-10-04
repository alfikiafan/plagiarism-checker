# view/file_selection.py

import threading
import time
import customtkinter as ctk
from tkinter import filedialog
from utils.constants import THRESHOLD_DEFAULT, MAX_REDUCTION_DEFAULT
import os

class FileSelectionFrame(ctk.CTkFrame):
    """
    FileSelectionFrame is a frame that contains the widgets for selecting files
    and setting the similarity threshold and maximum score deduction. It also
    contains the logic for starting the plagiarism check process.
    """
    def __init__(self, parent, controller, main_window):
        """
        Initializes the FileSelectionFrame with the parent window, controller, and main window.
        
        Args:
            parent (ctk.CTk): The parent window or frame.
            controller (PlagiarismController): The controller for handling the plagiarism checking process.
            main_window (MainWindow): The main window instance for updating results and displaying output.
        """
        super().__init__(parent)
        self.controller = controller
        self.main_window = main_window
        self.sorting_order = {}
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the file selection frame, including labels,
        entry fields, and buttons for selecting files and setting parameters.
        """
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(pady=5, padx=10, fill="both", expand=True)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=0)

        # File input (2 or more)
        self.file_label = ctk.CTkLabel(self.frame, text=self.main_window.localization.get("select_file"))
        self.file_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.file_entry = ctk.CTkEntry(self.frame, placeholder_text=self.main_window.localization.get("file_entry_placeholder"))
        self.file_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.file_button = ctk.CTkButton(self.frame, text=self.main_window.localization.get("browse_button"), command=self.browse_files)
        self.file_button.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Threshold for similarity percentage
        self.threshold_label = ctk.CTkLabel(self.frame, text=self.main_window.localization.get("threshold_label"))
        self.threshold_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.threshold_entry = ctk.CTkEntry(self.frame, placeholder_text=self.main_window.localization.get("threshold_placeholder"))
        self.threshold_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Maximum score deduction
        self.max_reduction_label = ctk.CTkLabel(self.frame, text=self.main_window.localization.get("max_reduction_label"))
        self.max_reduction_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.max_reduction_entry = ctk.CTkEntry(self.frame, placeholder_text=self.main_window.localization.get("max_reduction_placeholder"))
        self.max_reduction_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky="ew")

        # Select output location with a browse button
        self.output_label = ctk.CTkLabel(self.frame, text=self.main_window.localization.get("select_output"))
        self.output_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.output_entry = ctk.CTkEntry(self.frame, placeholder_text=self.main_window.localization.get("output_placeholder"))
        self.output_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.output_button = ctk.CTkButton(self.frame, text=self.main_window.localization.get("browse_button"), command=self.browse_output_location)
        self.output_button.grid(row=3, column=2, padx=5, pady=5, sticky="e")

    def update_ui_text(self, localization):
        """
        Update the text of all UI elements when the language changes.

        Args:
            localization (dict): The localization dictionary for the selected language
        """
        self.file_label.configure(text=localization.get("select_file"))
        self.file_button.configure(text=localization.get("browse_button"))
        self.file_entry.configure(placeholder_text=localization.get("file_entry_placeholder"))
        self.threshold_label.configure(text=localization.get("threshold_label"))
        self.threshold_entry.configure(placeholder_text=localization.get("threshold_placeholder"))
        self.max_reduction_label.configure(text=localization.get("max_reduction_label"))
        self.max_reduction_entry.configure(placeholder_text=localization.get("max_reduction_placeholder"))
        self.output_label.configure(text=localization.get("select_output"))
        self.output_entry.configure(placeholder_text=localization.get("output_placeholder"))
        self.output_button.configure(text=localization.get("browse_button"))

    def browse_files(self):
        """
        Opens a file dialog to select multiple files for plagiarism
        checking. The selected file paths are displayed in the entry field.
        """
        file_paths = filedialog.askopenfilenames(
            title=self.main_window.localization.get("select_files_title"),
            filetypes=[("Supported files",
                        "*.txt;*.docx;*.pdf;*.py;*.java;*.c;*.cpp;*.h;*.hpp;*.cs;*.js;*.html;*.css;*.php;*.sql;*.rb;*.pl;*.sh;*.swift;*.kt;*.go;*.rs;*.lua;*.r;*.m;*.json;*.xml;*.yaml;*.yml;*.ini;*.cfg;*.conf;*.md;*.rst;*.csv;*.tsv;*.xls;*.xlsx;*.ppt;*.pptx;*.odt;*.ods;*.odp")]
        )
        if len(file_paths) < 2:
            self.main_window.update_result(self.main_window.localization.get("error_select_two_files"))
            return
        self.file_entry.delete(0, 'end')
        self.file_entry.insert(0, ', '.join(file_paths))

    def browse_output_location(self):
        """
        Opens a file dialog to select the output location for saving the
        plagiarism check results. The selected path is displayed in the entry field.
        """
        output_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title=self.main_window.localization.get("select_output_title")
        )
        if output_path:
            self.output_entry.delete(0, 'end')
            self.output_entry.insert(0, output_path)

    def start_process(self):
        """
        Starts the plagiarism checking process with the selected files and parameters.
        """
        self.main_window.config(cursor="watch")
        self.main_window.update()
        self.disable_widgets()

        def run_plagiarism_check():
            try:
                time.sleep(0.1)
                files = self.file_entry.get().split(', ')
                output_file = self.output_entry.get()

                threshold_value = self.threshold_entry.get()
                reduction_value = self.max_reduction_entry.get()

                # Panggil controller untuk memproses logika plagiarisme
                result, error = self.controller.run_plagiarism_process(files, threshold_value, reduction_value, output_file)

                if error:
                    self.main_window.update_result(self.main_window.localization.get(error))
                    return

                df_similarity, df_reduction, file_cluster_mapping = result
                self.main_window.update_result(f"{self.main_window.localization.get('output_saved_successfully')} {output_file}")

                self.main_window.result_frame.show_output_window(df_similarity, df_reduction, output_file, file_cluster_mapping)

            except Exception as e:
                self.main_window.update_result(str(e))
            finally:
                self.main_window.config(cursor="")
                self.main_window.update()
                self.enable_widgets()

        # Jalankan proses di thread terpisah
        process_thread = threading.Thread(target=run_plagiarism_check)
        process_thread.start()

    def disable_widgets(self):
        """
        Disable all widgets in this frame.
        """
        for widget in self.winfo_children():
            try:
                widget.configure(state="disabled")
            except:
                pass

    def enable_widgets(self):
        """
        Enable all widgets in this frame.
        """
        for widget in self.winfo_children():
            try:
                widget.configure(state="normal")
            except:
                pass
