# /controller/plagiarism_controller.py

import pandas as pd
from model.file_reader import FileReader
from model.plagiarism_checker import PlagiarismChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.constants import THRESHOLD_DEFAULT, MAX_REDUCTION_DEFAULT
from sklearn.cluster import KMeans
import os

class PlagiarismController:
    """
    PlagiarismController is responsible for handling the plagiarism checking process.
    """
    def __init__(self, localization):
        """
        PlagiarismController constructor that accepts a localization object for translating messages.

        Args:
            localization (object): Localization object for fetching localized messages.
        """
        self.localization = localization
        self.file_reader = FileReader(self.localization)
        self.plagiarism_checker = PlagiarismChecker(self.localization)
        self.files_content = {}

    def process_files(self, file_paths, threshold, max_reduction):
        """
        Processes the selected files for plagiarism checking.

        Args:
            file_paths (list): List of file paths to be processed.
            threshold (float): Minimum similarity percentage to trigger score reduction.
            max_reduction (float): Maximum allowed score reduction.

        Returns:
            tuple: (df_similarity, df_reduction, error_files)
                - df_similarity (pd.DataFrame): DataFrame containing similarity percentages between files.
                - df_reduction (pd.DataFrame): DataFrame containing the percentage of score reduction per file.
                - error_files (dict): Dictionary containing files that failed to be processed along with their errors.
        """
        self.files_content = {}
        error_files = {}

        # Read all selected files
        for path in file_paths:
            try:
                content = self.file_reader.read_file(path)
                self.files_content[path] = content
            except IOError as e:
                error_files[path] = self.localization.get("file_read_error").format(path=path, error=str(e))

        # Check if at least two files were successfully read
        if len(self.files_content) < 2:
            if len(error_files) == len(file_paths):
                raise ValueError(self.localization.get("all_files_failed"))
            raise ValueError(self.localization.get("two_files_required"))

        # Process plagiarism using PlagiarismChecker
        df_similarity, df_reduction = self.plagiarism_checker.process_plagiarism(
            self.files_content, threshold, max_reduction
        )

        return df_similarity, df_reduction, error_files

    def get_file_content(self, filename):
        """
        Retrieves file content based on the file name.

        Args:
            filename (str): File name.

        Returns:
            str: File content.

        Raises:
            KeyError: If the file is not found.
        """
        # Search for the file by its basename
        for path, content in self.files_content.items():
            if os.path.basename(path) == filename:
                return content
        raise KeyError(self.localization.get("file_not_found").format(filename=filename))

    def cluster_files_by_content(self, files_content, n_clusters=5):
        """
        Clusters files based on their content.

        Args:
            files_content (dict): Dictionary containing file paths and their content.
            n_clusters (int): The desired number of clusters.

        Returns:
            dict: Mapping of the file basename to the cluster number.
        """
        # Step 1: Vectorize the content of each file using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        file_paths = list(files_content.keys())  # Full file paths
        contents = list(files_content.values())

        # Convert file content into numerical representation
        tfidf_matrix = vectorizer.fit_transform(contents)

        # Step 2: Perform clustering with KMeans
        unique_points = len(set(tuple(row.toarray()[0]) for row in tfidf_matrix))  # Number of unique points
        if n_clusters > unique_points:
            n_clusters = unique_points
            
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(tfidf_matrix)

        # Step 3: Clustering results (basename file_name -> cluster_number)
        file_cluster_mapping = {os.path.basename(file_paths[i]): kmeans.labels_[i] for i in range(len(file_paths))}

        return file_cluster_mapping
    
    def run_plagiarism_process(self, files, threshold_value, reduction_value, output_file):
        """
        Runs the plagiarism checking process with the selected files.

        Args:
            files (list): List of file paths to be processed.
            threshold_value (str): Threshold value for similarity percentage.
            reduction_value (str): Maximum reduction value for score.
            output_file (str): Path to the output file.

        Returns:
            tuple: (result, error)
                - result (tuple): Tuple containing the DataFrames and file-cluster mapping.
                - error (str): Error message if an error occurred.
        """
        try:
            threshold = float(threshold_value) if threshold_value else THRESHOLD_DEFAULT
        except ValueError:
            return None, "error_threshold_number"
        
        try:
            max_reduction = float(reduction_value) if reduction_value else MAX_REDUCTION_DEFAULT
        except ValueError:
            return None, "error_max_reduction_number"

        if not files or len(files) < 2:
            return None, "error_select_two_files"
        
        if not output_file:
            return None, "error_select_output"

        # Plagiarism and clustering process
        df_similarity, df_reduction, error_files = self.process_files(files, threshold, max_reduction)

        if error_files:
            error_messages = "\n".join([f"{os.path.basename(k)}: {v}" for k, v in error_files.items()])
            return None, f"{self.localization.get('error_reading_files')}:\n{error_messages}"

        files_content = self.files_content
        file_cluster_mapping = self.cluster_files_by_content(files_content)

        df_similarity['Cluster'] = df_similarity['File 1'].apply(lambda x: file_cluster_mapping.get(os.path.basename(x), 'N/A'))

        return (df_similarity, df_reduction, file_cluster_mapping), None
    
    def save_results_to_excel(self, df_similarity, df_reduction, output_file, file_cluster_mapping):
        """
        Saves the plagiarism checking results to an Excel file.

        Args:
            df_similarity (pd.DataFrame): DataFrame containing similarity percentages between files.
            df_reduction (pd.DataFrame): DataFrame containing score reduction percentages per file.
            output_file (str): Path to the output Excel file.
            file_cluster_mapping (dict): Mapping of the file basename to the cluster number.

        Returns:
            str: Error message if an error occurred, otherwise None.
        """
        try:
            with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
                df_reduction.to_excel(writer, sheet_name='Score Deduction', index=False)
                df_similarity.to_excel(writer, sheet_name='Similarity', index=False)
                df_cluster_mapping = pd.DataFrame(list(file_cluster_mapping.items()), columns=['File Name', 'Cluster'])
                df_cluster_mapping.to_excel(writer, sheet_name='Cluster Mapping', index=False)
            return None
        except Exception as e:
            return str(e)
