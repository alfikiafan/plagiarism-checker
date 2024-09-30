# view/results_display.py

import customtkinter as ctk
from tkinter import ttk
import pandas as pd
import os
from utils.constants import ASCENDING_ARROW, DESCENDING_ARROW
from view.comparison_display import ComparisonDisplayWindow
from view.file_content_display import FileContentDisplayWindow

class ResultsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color="#2B2B2B")
        self.parent = parent  # Reference to MainWindow
        self.setup_ui()

    def setup_ui(self):
        # Result description box
        self.result_label = ctk.CTkLabel(self, text="", wraplength=500)
        self.result_label.pack(padx=5, pady=5)

    def update_result(self, message):
        self.result_label.configure(text=message)

    def show_output_window(self, df_similarity, df_reduction, output_file, file_cluster_mapping):
        # Save results to Excel
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_reduction.to_excel(writer, sheet_name='Score Deduction', index=False)
                df_similarity.to_excel(writer, sheet_name='Similarity', index=False)
        except Exception as e:
            self.update_result(f"Error saving Excel file: {e}")
            return

        # Add "Cluster" column to df_reduction
        df_reduction["Cluster"] = df_reduction["File Name"].apply(lambda file_name: file_cluster_mapping.get(os.path.basename(file_name), 'N/A'))

        # Create a new window to display the results
        output_window = ctk.CTkToplevel(self)
        output_window.title("Plagiarism Check Results")
        output_window.geometry("800x600")

        # Table 1: Similarity Percentage (without the Cluster column)
        similarity_label = ctk.CTkLabel(output_window, text="Similarity Percentage", font=ctk.CTkFont(size=18, weight="bold"))
        similarity_label.pack(pady=5)

        # Search box for the Similarity Percentage table
        search_frame_similarity = ctk.CTkFrame(output_window)
        search_frame_similarity.pack(pady=5, padx=10, fill="x")

        search_label_similarity = ctk.CTkLabel(search_frame_similarity, text="Search:", font=ctk.CTkFont(size=14))
        search_label_similarity.pack(side="left", padx=5)

        search_entry_similarity = ctk.CTkEntry(search_frame_similarity, placeholder_text="Enter search keyword...")
        search_entry_similarity.pack(side="left", fill="x", expand=True, padx=5)

        similarity_frame = ctk.CTkFrame(output_window)
        similarity_frame.pack(pady=5, padx=10, fill="both", expand=True)

        similarity_scroll = ctk.CTkScrollbar(similarity_frame, orientation='vertical')
        similarity_scroll.pack(side="right", fill="y")

        similarity_columns = ["File 1", "File 2", "Similarity (%)"]
        similarity_table = ttk.Treeview(similarity_frame, columns=similarity_columns, show='headings', height=8, yscrollcommand=similarity_scroll.set)

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

        # Function to populate the similarity table with data
        def populate_similarity_table(data):
            similarity_table.delete(*similarity_table.get_children())  # Clear existing data
            for index, row in data.iterrows():
                similarity_table.insert('', 'end', values=list(row))

        # Function to sort and populate table by a specific column
        def sort_similarity_table(col):
            ascending = sort_states_similarity[col]
            sorted_data = df_similarity.sort_values(by=[col], ascending=ascending)
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
            if col == "File 1" or col == "File 2":
                similarity_table.heading(col, text=col, command=lambda _col=col: sort_similarity_table(_col))
                similarity_table.column(col, anchor='w', width=150)
            else:
                similarity_table.heading(col, text=col, command=lambda _col=col: sort_similarity_table(_col))
                similarity_table.column(col, anchor='center', width=150)

        # Populate the table with the full data initially
        populate_similarity_table(df_similarity)

        # Function to filter data based on search query in similarity table
        def search_similarity_table(*args):
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
        reduction_label = ctk.CTkLabel(output_window, text="Score Deduction", font=ctk.CTkFont(size=18, weight="bold"))
        reduction_label.pack(pady=5)

        # Search box for the Score Deduction table
        search_frame_reduction = ctk.CTkFrame(output_window)
        search_frame_reduction.pack(pady=5, padx=10, fill="x")

        search_label_reduction = ctk.CTkLabel(search_frame_reduction, text="Search:", font=ctk.CTkFont(size=14))
        search_label_reduction.pack(side="left", padx=5)

        search_entry_reduction = ctk.CTkEntry(search_frame_reduction, placeholder_text="Enter search keyword...")
        search_entry_reduction.pack(side="left", fill="x", expand=True, padx=5)

        reduction_frame = ctk.CTkFrame(output_window)
        reduction_frame.pack(pady=5, padx=10, fill="both", expand=True)

        reduction_scroll = ctk.CTkScrollbar(reduction_frame, orientation='vertical')
        reduction_scroll.pack(side="right", fill="y")

        reduction_columns = [str(col) for col in df_reduction.columns]
        reduction_table = ttk.Treeview(reduction_frame, columns=reduction_columns, show='headings', height=8, yscrollcommand=reduction_scroll.set)

        reduction_scroll.configure(command=reduction_table.yview)

        sort_states_reduction = {col: True for col in reduction_columns}

        for col in reduction_columns:
            reduction_table.heading(col, text=col, command=lambda _col=col: sort_reduction_table(_col))
            reduction_table.column(col, anchor='w' if col == "File Name" else 'center', width=150)

        # Function to populate the reduction table with data
        def populate_reduction_table(data):
            reduction_table.delete(*reduction_table.get_children())
            for index, row in data.iterrows():
                reduction_table.insert('', 'end', values=list(row))

        # Function to sort and populate reduction table by a specific column
        def sort_reduction_table(col):
            ascending = sort_states_reduction[col]
            sorted_data = df_reduction.sort_values(by=[col], ascending=ascending)
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
        similarity_table.bind("<Double-1>", lambda event: self.open_comparison_window(event, df_similarity))
        reduction_table.bind("<Double-1>", lambda event: self.open_file_content_window(event, df_reduction))

    def open_comparison_window(self, event, df_similarity):
        selected_item = event.widget.selection()
        if not selected_item:
            return

        # Get the file names from the selected row
        item = event.widget.item(selected_item)
        file1, file2 = item['values'][0], item['values'][1]

        # Create a comparison window
        ComparisonDisplayWindow(self, file1, file2, self.parent.controller)

    def open_file_content_window(self, event, df_reduction):
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
            self.update_result(f"Error retrieving file content: {e}")
            return

        # Create a window to display the file content
        FileContentDisplayWindow(self, file_name, content, self.parent.controller)
