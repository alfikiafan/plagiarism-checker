# view/file_content_display.py

import customtkinter as ctk
from tkinter import ttk
import os

class FileContentDisplayWindow(ctk.CTkToplevel):
    """
    A window to display the content of a selected file in a read-only text view.

    This class is responsible for creating a pop-up window that displays the content
    of a file and configures the display based on the file type, adjusting font
    settings accordingly.

    Attributes:
        parent (ctk.CTk): The parent window that launched this window.
        file_name (str): The name of the file to display.
        content (str): The actual content of the file.
        controller (PlagiarismController): The controller instance for accessing settings and configurations.
        localization (object): Localization object for dynamic language switching.
    """
    def __init__(self, parent, file_name, content, controller):
        """
        Initializes the window for displaying file content.

        Args:
            parent (ctk.CTk): The parent window of this window.
            file_name (str): The name of the file to display.
            content (str): The content of the file.
            controller (PlagiarismController): The controller for accessing app configurations.
        """
        super().__init__(parent)
        self.parent = parent
        self.file_name = file_name
        self.content = content
        self.controller = controller
        self.localization = controller.localization  # Use the localization object from the controller

        # Window properties
        self.title(self.localization.get("file_content_title").format(file_name=self.file_name))
        self.geometry("900x600")

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for displaying file content, including a title,
        text view, and scrollbars for navigation.
        """
        # Title label displaying the file name
        title_label = ctk.CTkLabel(
            self,
            text=self.localization.get("file_content_title").format(file_name=self.file_name),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_label.pack(pady=10)

        # Frame to contain the text widget and scrollbars
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Text widget for displaying the file content in a non-editable manner
        text_widget = ctk.CTkTextbox(text_frame, wrap="none")
        text_widget.pack(side="left", fill="both", expand=True)
        text_widget.insert("1.0", self.content)  # Insert content into the text widget
        text_widget.configure(state="disabled")  # Make the text view read-only

        # Set the appropriate font based on the file type
        self.set_programming_font(text_widget, self.file_name)

        # Vertical scrollbar for navigating the file content
        sync_scroll_verticalbar = ctk.CTkScrollbar(text_frame, command=text_widget.yview)
        sync_scroll_verticalbar.pack(side="right", fill="y")
        text_widget.configure(yscrollcommand=sync_scroll_verticalbar.set)

        # Horizontal scrollbar for navigating long lines of text
        sync_scrollbar_horizontal = ctk.CTkScrollbar(self, command=text_widget.xview, orientation="horizontal")
        sync_scrollbar_horizontal.pack(side="bottom", fill="x")
        text_widget.configure(xscrollcommand=sync_scrollbar_horizontal.set)

    def set_programming_font(self, widget, filepath):
        """
        Sets the font of the text widget based on the file extension.
        Programming files get a monospace font for better readability.

        Args:
            widget (CTkTextbox): The text widget whose font will be adjusted.
            filepath (str): The complete file path to determine the file extension.
        """
        # Get the file extension
        ext = os.path.splitext(filepath)[1].lower()

        # If the file is a programming file, use a monospace font like Consolas
        if ext in self.controller.file_reader.programming_extensions:
            widget.configure(font=("Consolas", 12))
        else:
            # Otherwise, use a standard sans-serif font
            widget.configure(font=("Open Sans", 12))
