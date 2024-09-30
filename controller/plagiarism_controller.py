# /controller/plagiarism_controller.py

from model.file_reader import FileReader
from model.plagiarism_checker import PlagiarismChecker
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import os

class PlagiarismController:
    def __init__(self):
        self.file_reader = FileReader()
        self.plagiarism_checker = PlagiarismChecker()
        self.files_content = {}  # Stores the content of the read files

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
                error_files[path] = str(e)

        # Check if at least two files were successfully read
        if len(self.files_content) < 2:
            if len(error_files) == len(file_paths):
                raise ValueError("All files failed to be read. No files to compare.")
            raise ValueError("Make sure at least two files have been successfully read for comparison.")

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
        raise KeyError(f"File {filename} not found.")

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
