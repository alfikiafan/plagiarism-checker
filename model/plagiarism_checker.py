# /model/plagiarism_checker.py

import difflib
import itertools
import pandas as pd
import os

class PlagiarismChecker:
    def __init__(self, localization):
        """
        Constructor for the PlagiarismChecker that accepts a localization object for translating messages.
        """
        self.localization = localization

    def calculate_similarity(self, text1, text2):
        """
        Calculates the similarity ratio between two texts using difflib.

        Args:
            text1 (str): The first text.
            text2 (str): The second text.

        Returns:
            float: Similarity ratio between 0.0 and 1.0.
        """
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def calculate_reduction(self, plagiarism_percent, threshold=80, max_reduction=20):
        """
        Calculates the score reduction based on the percentage of plagiarism.

        Args:
            plagiarism_percent (float): The percentage of plagiarism.
            threshold (float, optional): The minimum plagiarism percentage threshold for score reduction. Default is 80.
            max_reduction (float, optional): The maximum allowed score reduction. Default is 20.

        Returns:
            float: Percentage of score reduction.
        """
        if plagiarism_percent <= threshold:
            return 0.0
        elif plagiarism_percent >= 100:
            return max_reduction
        else:
            return ((plagiarism_percent - threshold) / (100 - threshold)) * max_reduction

    def process_plagiarism(self, files_content, threshold, max_reduction):
        """
        Processes plagiarism checking between multiple files.

        Args:
            files_content (dict): Dictionary with file names as keys and file content as values.
            threshold (float): Minimum similarity percentage threshold for score reduction.
            max_reduction (float): Maximum allowed score reduction.

        Returns:
            tuple: (df_similarity, df_reduction)
                - df_similarity (pd.DataFrame): DataFrame containing similarity percentages between files.
                - df_reduction (pd.DataFrame): DataFrame containing score reduction percentages per file.
        """
        if len(files_content) < 2:
            raise ValueError(self.localization.get("two_files_required"))

        reduction_dict = {os.path.basename(filename): 0.0 for filename in files_content.keys()}
        similarities = []

        file_pairs = itertools.combinations(files_content.keys(), 2)
        for file1, file2 in file_pairs:
            text1 = files_content[file1]
            text2 = files_content[file2]
            similarity_ratio = self.calculate_similarity(text1, text2) * 100

            similarities.append((os.path.basename(file1), os.path.basename(file2), round(similarity_ratio, 2)))

            if similarity_ratio > threshold:
                reduction = self.calculate_reduction(similarity_ratio, threshold, max_reduction)
                reduction_dict[os.path.basename(file1)] = max(reduction_dict[os.path.basename(file1)], reduction)
                reduction_dict[os.path.basename(file2)] = max(reduction_dict[os.path.basename(file2)], reduction)

        data_reduction = [
            {
                self.localization.get("file_name"): student,
                self.localization.get("score_reduction_percentage"): round(reduction, 2) if isinstance(reduction, float) else reduction
            }
            for student, reduction in reduction_dict.items()
        ]

        df_reduction = pd.DataFrame(data_reduction)
        df_reduction = df_reduction.sort_values(by=self.localization.get("score_reduction_percentage"), ascending=False)

        data_similarity = [
            {
                self.localization.get("file_1"): file1,
                self.localization.get("file_2"): file2,
                self.localization.get("similarity_percent"): sim
            }
            for file1, file2, sim in similarities
        ]

        df_similarity = pd.DataFrame(data_similarity)
        df_similarity = df_similarity.sort_values(by=self.localization.get("similarity_percent"), ascending=False)

        return df_similarity, df_reduction
