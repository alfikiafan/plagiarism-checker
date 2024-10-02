# view/main_window.py

import customtkinter as ctk
from controller.plagiarism_controller import PlagiarismController
from view.file_selection import FileSelectionFrame
from view.results_display import ResultsFrame
from utils.localization import Localization
from PIL import Image

class MainWindow(ctk.CTk):
    """
    MainWindow is the main window of the application. It contains the main
    components of the application, such as the file selection frame, the
    results frame, and the start button.
    """
    def __init__(self):
        super().__init__()        
        self.current_language = "en"
        self.localization = Localization(self.current_language)
        self.languages = {"English": "en", "Bahasa Indonesia": "id"}
        
        self.controller = PlagiarismController(self.localization)

        # Initialize UI window
        self.title(self.localization.get("app_title"))
        self.geometry("510x350")
        self.resizable(False, False)
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.setup_ui()

    def setup_ui(self):
        # Create a top frame for both title and language dropdown
        top_frame = ctk.CTkFrame(self, fg_color="transparent")  # No background color for the frame
        top_frame.grid_columnconfigure(0, weight=1)  # Allow column 0 (title) to expand
        top_frame.grid_columnconfigure(1, weight=0)  # Language dropdown column should not expand
        top_frame.pack(fill="x", pady=5, padx=10)

        # Main label (title) centered in the window
        self.main_label = ctk.CTkLabel(
            top_frame,
            text=self.localization.get("welcome_message"),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.main_label.grid(row=0, column=0, sticky="w")  # Center the title without background

        # Create a sub-frame for the language icon and dropdown
        lang_frame = ctk.CTkFrame(top_frame, fg_color="transparent")
        lang_frame.grid(row=0, column=1, sticky="e", padx=10)

        # Language dropdown without icon inside
        self.language_var = ctk.StringVar(value="English")
        self.language_dropdown = ctk.CTkOptionMenu(
            lang_frame,
            variable=self.language_var,
            values=list(self.languages.keys()),
            width=130,
            height=30,
            command=self.change_language
        )
        self.language_dropdown.pack(side="left", padx=(0, 0))

        # Frame used for file selection
        self.file_selection = FileSelectionFrame(self, self.controller, self)
        self.file_selection.pack(pady=5, padx=10, fill="both", expand=True)

        # Start button
        self.process_button = ctk.CTkButton(
            self,
            text=self.localization.get("start_button"),
            command=self.file_selection.start_process
        )
        self.process_button.pack(pady=10)

        # Frame used for displaying results
        self.result_frame = ResultsFrame(self)
        self.result_frame.pack(fill="x", padx=10, pady=5)

    def change_language(self, selected_language):
        """
        Handle language change when the user selects a different language from the dropdown.
        """
        # Get the language code from the selected language
        new_language_code = self.languages.get(selected_language)

        # Update the localization object and current language
        self.current_language = new_language_code
        self.localization = Localization(new_language_code)
        
        # Refresh the UI to reflect the new language
        self.refresh_ui()

        # Update the text of the dropdown to the chosen language
        self.language_dropdown.set(selected_language)

    def refresh_ui(self):
        """
        Refresh all UI elements to reflect the current language.
        """
        # Update window title
        self.title(self.localization.get("app_title"))

        # Update main label text
        self.main_label.configure(text=self.localization.get("welcome_message"))

        # Update Start button text
        self.process_button.configure(text=self.localization.get("start_button"))

        # Refresh the UI elements in the FileSelectionFrame and ResultsFrame
        self.file_selection.update_ui_text(self.localization)
        self.result_frame.update_ui_text(self.localization)

    def update_result(self, message):
        """
        Update the result frame with a given message.
        """
        self.result_frame.update_result(message)

