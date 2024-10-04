# view/results_display.py

import customtkinter as ctk
from tkinter import ttk
import pandas as pd
import os
from utils.constants import ASCENDING_ARROW, DESCENDING_ARROW
from view.comparison_display import ComparisonDisplayWindow
from view.file_content_display import FileContentDisplayWindow

class ResultsFrame(ctk.CTkFrame):
    """
    ResultsFrame is a frame that displays the results of the plagiarism check,
    including the similarity percentage and score deduction for each file pair.
    """
    def __init__(self, parent):
        """
        Initializes the ResultsFrame with the parent window.

        Args:
            parent (ctk.CTk): The parent window or frame.
        """
        super().__init__(parent, fg_color="#2B2B2B")
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the user interface for the results frame, including labels and a text area
        to display the results of the plagiarism check.
        """
        self.result_label = ctk.CTkLabel(self, text="", wraplength=500)
        self.result_label.pack(padx=5, pady=5)

    def update_result(self, message):
        """
        Updates the result label with the given message.

        Args:
            message (str): The message to display in the result label.
        """
        self.result_label.configure(text=message)

    def show_output_window(self, df_similarity, df_reduction, output_file, file_cluster_mapping):
        """
        Displays the results of the plagiarism check in a new window, including the similarity
        percentage and score deduction for each file pair. The results are displayed in two tables.
        
        Args:
            df_similarity (pd.DataFrame): DataFrame containing the similarity percentage between file pairs.
            df_reduction (pd.DataFrame): DataFrame containing the score deduction for each file.
            output_file (str): The path to the output Excel file containing the results.
            file_cluster_mapping (dict): A dictionary mapping file names to cluster labels.
        """
        error = self.parent.controller.save_results_to_excel(df_similarity, df_reduction, output_file, file_cluster_mapping)

        if error:
            self.update_result(f"{self.parent.localization.get('error_saving_file')} {error}")
            return

        # Add "Cluster" column to df_reduction
        df_reduction["Cluster"] = df_reduction["File Name"].apply(lambda file_name: file_cluster_mapping.get(os.path.basename(file_name), 'N/A'))

        # Create a new window to display the results
        output_window = ctk.CTkToplevel(self)
        output_window.title(self.parent.localization.get("results_window_title"))
        output_window.geometry("800x600")

        # Table 1: Similarity Percentage (without the Cluster column)
        similarity_label = ctk.CTkLabel(output_window, text=self.parent.localization.get("similarity_percentage"), font=ctk.CTkFont(size=18, weight="bold"))
        similarity_label.pack(pady=5)

        # Search box for the Similarity Percentage table
        search_frame_similarity = ctk.CTkFrame(output_window)
        search_frame_similarity.pack(pady=5, padx=10, fill="x")

        search_label_similarity = ctk.CTkLabel(search_frame_similarity, text=self.parent.localization.get("search_label"), font=ctk.CTkFont(size=14))
        search_label_similarity.pack(side="left", padx=5)

        search_entry_similarity = ctk.CTkEntry(search_frame_similarity, placeholder_text=self.parent.localization.get("search_placeholder"))
        search_entry_similarity.pack(side="left", fill="x", expand=True, padx=5)

        similarity_frame = ctk.CTkFrame(output_window)
        similarity_frame.pack(pady=5, padx=10, fill="both", expand=True)

        similarity_scroll = ctk.CTkScrollbar(similarity_frame, orientation='vertical')
        similarity_scroll.pack(side="right", fill="y")

        similarity_columns = [
            self.parent.localization.get("file_1"),
            self.parent.localization.get("file_2"),
            self.parent.localization.get("similarity_percent")
        ]
        similarity_table = ttk.Treeview(similarity_frame, columns=similarity_columns, show='headings', height=8, yscrollcommand=similarity_scroll.set)

        column_mapping = {
            self.parent.localization.get("file_1"): "File 1",
            self.parent.localization.get("file_2"): "File 2",
            self.parent.localization.get("similarity_percent"): "Similarity (%)"
        }
        sort_states_similarity = {col: True for col in similarity_columns}

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

        def populate_similarity_table(data):
            """
            Populate the similarity table with data from the DataFrame.

            Args:
                data (pd.DataFrame): The DataFrame containing the similarity data
            """
            similarity_table.delete(*similarity_table.get_children())  # Clear existing data
            for index, row in data.iterrows():
                similarity_table.insert('', 'end', values=list(row))

        def sort_similarity_table(col):
            """
            Sort the similarity table by a specific column and populate the table with the sorted data.
            
            Args:
                col (str): The column to sort by.
            """
            internal_col = column_mapping[col]
            ascending = sort_states_similarity[col]
            sorted_data = df_similarity.sort_values(by=[internal_col], ascending=ascending)
            populate_similarity_table(sorted_data)
            
            for column in similarity_columns:
                # Set header text with arrow for the sorted column
                if column == col:
                    arrow = ASCENDING_ARROW if ascending else DESCENDING_ARROW
                    similarity_table.heading(column, text=f"{column} {arrow}")
                else:
                    similarity_table.heading(column, text=column)

            sort_states_similarity[col] = not ascending

        for col in similarity_columns:
            if col == self.parent.localization.get("file_1") or col == self.parent.localization.get("file_2"):
                similarity_table.heading(col, text=col, command=lambda _col=col: sort_similarity_table(_col))
                similarity_table.column(col, anchor='w', width=150)
            else:
                similarity_table.heading(col, text=col, command=lambda _col=col: sort_similarity_table(_col))
                similarity_table.column(col, anchor='center', width=150)

        # Populate the table with the full data initially
        populate_similarity_table(df_similarity)

        def search_similarity_table(*args):
            """
            Filter the similarity table based on the search query in the search entry.
            
            Args:
                *args: Additional arguments passed to the function.
            """
            query = search_entry_similarity.get().lower()
            if query == "":  # If the search box is empty, show all data
                populate_similarity_table(df_similarity)
            else:
                filtered_data = df_similarity[
                    df_similarity.apply(lambda row: any(query in str(val).lower() for val in row), axis=1)
                ]
                populate_similarity_table(filtered_data)

        # Bind the search function to the search entry
        search_entry_similarity.bind('<KeyRelease>', search_similarity_table)

        similarity_table.pack(fill="both", expand=True)

        # Table 2: Score Deduction (with Cluster column)
        reduction_label = ctk.CTkLabel(output_window, text=self.parent.localization.get("score_deduction"), font=ctk.CTkFont(size=18, weight="bold"))
        reduction_label.pack(pady=5)

        # Search box for the Score Deduction table
        search_frame_reduction = ctk.CTkFrame(output_window)
        search_frame_reduction.pack(pady=5, padx=10, fill="x")

        search_label_reduction = ctk.CTkLabel(search_frame_reduction, text=self.parent.localization.get("search_label"), font=ctk.CTkFont(size=14))
        search_label_reduction.pack(side="left", padx=5)

        search_entry_reduction = ctk.CTkEntry(search_frame_reduction, placeholder_text=self.parent.localization.get("search_placeholder"))
        search_entry_reduction.pack(side="left", fill="x", expand=True, padx=5)

        reduction_frame = ctk.CTkFrame(output_window)
        reduction_frame.pack(pady=5, padx=10, fill="both", expand=True)

        reduction_scroll = ctk.CTkScrollbar(reduction_frame, orientation='vertical')
        reduction_scroll.pack(side="right", fill="y")

        reduction_columns = [
            self.parent.localization.get("file_name"),
            self.parent.localization.get("score_reduction_percentage"),
            self.parent.localization.get("cluster")
        ]

        reduction_column_mapping = {
            self.parent.localization.get("file_name"): "File Name",
            self.parent.localization.get("score_reduction_percentage"): "Score Reduction Percentage (%)",
            self.parent.localization.get("cluster"): "Cluster"
        }

        reduction_table = ttk.Treeview(reduction_frame, columns=reduction_columns, show='headings', height=8, yscrollcommand=reduction_scroll.set)

        reduction_scroll.configure(command=reduction_table.yview)

        sort_states_reduction = {col: True for col in reduction_columns}

        for col in reduction_columns:
            reduction_table.heading(col, text=col, command=lambda _col=col: sort_reduction_table(_col))
            reduction_table.column(col, anchor='w' if col == self.parent.localization.get("file_name") else 'center', width=150)

        def populate_reduction_table(data):
            """
            Populate the score deduction table with data from the DataFrame.

            Args:
                data (pd.DataFrame): The DataFrame containing the score deduction data
            """
            reduction_table.delete(*reduction_table.get_children())
            for index, row in data.iterrows():
                reduction_table.insert('', 'end', values=list(row))

        def sort_reduction_table(col):
            """
            Sort the score deduction table by a specific column and populate the table with the sorted data.

            Args:
                col (str): The column to sort by.
            """
            internal_col = reduction_column_mapping[col]
            ascending = sort_states_reduction[col]
            sorted_data = df_reduction.sort_values(by=[internal_col], ascending=ascending)
            populate_reduction_table(sorted_data)

            for column in reduction_columns:
                # Set header text with arrow for the sorted column
                if column == col:
                    arrow = ASCENDING_ARROW if ascending else DESCENDING_ARROW
                    reduction_table.heading(column, text=f"{column} {arrow}")
                else:
                    reduction_table.heading(column, text=column)

            sort_states_reduction[col] = not ascending

        # Populate the table with the full data initially
        populate_reduction_table(df_reduction)

        # Function to filter data based on search query in reduction table
        def search_reduction_table(*args):
            """
            Filter the score deduction table based on the search query in the search entry.
            
            Args:
                *args: Additional arguments passed to the function.
            """
            query = search_entry_reduction.get().lower()
            if query == "":  # If the search box is empty, show all data
                populate_reduction_table(df_reduction)
            else:
                filtered_data = df_reduction[
                    df_reduction.apply(lambda row: any(query in str(val).lower() for val in row), axis=1)
                ]
                populate_reduction_table(filtered_data)

        # Bind the search function to the search entry
        search_entry_reduction.bind('<KeyRelease>', search_reduction_table)
        reduction_table.pack(fill="both", expand=True)

        # Double click event to display text comparison
        similarity_table.bind("<Double-1>", lambda event: self.open_comparison_window(event))
        reduction_table.bind("<Double-1>", lambda event: self.open_file_content_window(event))

    def open_comparison_window(self, event):
        """
        Opens a new window to display the comparison between two files when a row is double-clicked.
        
        Args:
            event (tk.Event): The event object containing information about the event.
        """
        selected_item = event.widget.selection()
        if not selected_item:
            return

        # Get the file names from the selected row
        item = event.widget.item(selected_item)
        file1, file2 = item['values'][0], item['values'][1]

        # Create a comparison window
        ComparisonDisplayWindow(self, file1, file2, self.parent.controller)

    def open_file_content_window(self, event):
        """
        Opens a new window to display the content of a file when a row is double-clicked.

        Args:
            event (tk.Event): The event object containing information about the event.
        """
        selected_item = event.widget.selection()
        if not selected_item:
            return

        # Get the file name from the selected row
        item = event.widget.item(selected_item)
        file_name = item['values'][0]  # Assuming "File Name" is in the first column

        # Get the file content from the controller
        try:
            content = self.parent.controller.get_file_content(file_name)
        except Exception as e:
            self.update_result(f"{self.parent.localization.get('error_retrieving_file_content')}: {e}")
            return

        # Create a window to display the file content
        FileContentDisplayWindow(self, file_name, content, self.parent.controller)