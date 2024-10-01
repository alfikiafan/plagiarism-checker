# view/comparison_display.py

import customtkinter as ctk
from tkinter import ttk
import difflib
import os

class ComparisonDisplayWindow(ctk.CTkToplevel):
    """
    A window for displaying the content of two files side by side, allowing comparison.

    This class creates a pop-up window that loads the content of two files and highlights
    similar sections between them using difflib for text comparison.
    """
    def __init__(self, parent, file1, file2, controller):
        """
        Initializes the comparison window between two files.

        Args:
            parent (ctk.CTk): The parent window of this comparison window.
            file1 (str): Full path to the first file.
            file2 (str): Full path to the second file.
            controller (PlagiarismController): The controller instance to access file content.
        """
        super().__init__(parent)
        self.parent = parent
        self.file1 = file1
        self.file2 = file2
        self.controller = controller
        self.localization = controller.localization

        # Set up the window's properties
        self.title(self.localization.get("file_comparison_title"))
        self.geometry("900x600")
        self.lift()

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for displaying the content of two files side by side.
        """
        # Frame to hold the content of both files
        text_frame = ctk.CTkFrame(self)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame on the left side for file 1
        text1_frame = ctk.CTkFrame(text_frame)
        text1_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Title label for file 1
        file1_label = ctk.CTkLabel(
            text1_frame,
            text=self.localization.get("file_label").format(file_name=os.path.basename(self.file1)),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        file1_label.pack(pady=5)

        # Text widget to display the content of file 1
        text1_widget = ctk.CTkTextbox(text1_frame, wrap="none")
        text1_widget.pack(side="left", fill="both", expand=True)
        content1 = self.controller.get_file_content(self.file1)
        text1_widget.insert("1.0", content1)
        text1_widget.configure(state="disabled")  # Make it read-only

        # Set font based on file type for file 1
        self.set_programming_font(text1_widget, self.file1)

        # Frame on the right side for file 2
        text2_frame = ctk.CTkFrame(text_frame)
        text2_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Title label for file 2
        file2_label = ctk.CTkLabel(
            text2_frame,
            text=self.localization.get("file_label").format(file_name=os.path.basename(self.file2)),
            font=ctk.CTkFont(size=18, weight="bold")
        )
        file2_label.pack(pady=5)

        # Text widget to display the content of file 2
        text2_widget = ctk.CTkTextbox(text2_frame, wrap="none")
        text2_widget.pack(side="left", fill="both", expand=True)
        content2 = self.controller.get_file_content(self.file2)
        text2_widget.insert("1.0", content2)
        text2_widget.configure(state="disabled")  # Make it read-only

        # Set font based on file type for file 2
        self.set_programming_font(text2_widget, self.file2)

        # Synchronized vertical scrollbar for both text widgets
        sync_scroll_verticalbar = ctk.CTkScrollbar(text_frame, command=lambda *args: self.sync_scroll_vertical(text1_widget, text2_widget, *args))
        sync_scroll_verticalbar.pack(side="right", fill="y")

        # Connect both text widgets' yscrollcommand to the synchronized scrollbar
        text1_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))
        text2_widget.configure(yscrollcommand=lambda *args: sync_scroll_verticalbar.set(*args))

        # Synchronized horizontal scrollbar for both text widgets
        sync_scrollbar_horizontal = ctk.CTkScrollbar(self, command=lambda *args: self.sync_scroll_horizontal(text1_widget, text2_widget, *args), orientation="horizontal")
        sync_scrollbar_horizontal.pack(side="bottom", fill="x")

        # Connect both text widgets' xscrollcommand to the synchronized scrollbar
        text1_widget.configure(xscrollcommand=lambda *args: sync_scrollbar_horizontal.set(*args))
        text2_widget.configure(xscrollcommand=lambda *args: sync_scrollbar_horizontal.set(*args))

        # Highlight the similarities between the two text contents
        self.highlight_similarities(text1_widget, text2_widget, content1, content2)

    def set_programming_font(self, widget, filepath):
        """
        Sets the font for the text widget based on the file extension.
        Programming files use a monospace font for better readability.

        Args:
            widget (CTkTextbox): The text widget to apply the font to.
            filepath (str): The full file path to determine the file extension.
        """
        ext = os.path.splitext(filepath)[1].lower()
        if ext in self.controller.file_reader.programming_extensions:
            widget.configure(font=("Consolas", 12))
        else:
            widget.configure(font=("Open Sans", 12))

    def sync_scroll_vertical(self, text1_widget, text2_widget, *args):
        """
        Synchronizes vertical scrolling between the two text widgets.

        Args:
            text1_widget (CTkTextbox): The text widget for file 1.
            text2_widget (CTkTextbox): The text widget for file 2.
            *args: Additional arguments for yview.
        """
        text1_widget.yview(*args)
        text2_widget.yview(*args)

    def sync_scroll_horizontal(self, text1_widget, text2_widget, *args):
        """
        Synchronizes horizontal scrolling between the two text widgets.

        Args:
            text1_widget (CTkTextbox): The text widget for file 1.
            text2_widget (CTkTextbox): The text widget for file 2.
            *args: Additional arguments for xview.
        """
        text1_widget.xview(*args)
        text2_widget.xview(*args)

    def highlight_similarities(self, text1_widget, text2_widget, text1, text2):
        """
        Highlights the similar text segments between the two files using difflib.

        Args:
            text1_widget (CTkTextbox): The text widget for file 1.
            text2_widget (CTkTextbox): The text widget for file 2.
            text1 (str): The content of file 1.
            text2 (str): The content of file 2.
        """
        sequence_matcher = difflib.SequenceMatcher(None, text1, text2)

        for match in sequence_matcher.get_matching_blocks():
            start1, start2, length = match
            if length > 0:
                # Highlight in file 1 with color #4B5632
                text1_widget.tag_add("highlight", f"1.0+{start1}c", f"1.0+{start1+length}c")
                text1_widget.tag_config("highlight", background="#4B5632", foreground="white")

                # Highlight in file 2 with the same color
                text2_widget.tag_add("highlight", f"1.0+{start2}c", f"1.0+{start2+length}c")
                text2_widget.tag_config("highlight", background="#4B5632", foreground="white")
