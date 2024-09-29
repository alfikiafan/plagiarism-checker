# /model/plagiarism_checker.py

import difflib
import itertools
import pandas as pd
import os

class PlagiarismChecker:
    def calculate_similarity(self, text1, text2):
        """
        Menghitung rasio kesamaan antara dua teks menggunakan difflib.

        Args:
            text1 (str): Teks pertama.
            text2 (str): Teks kedua.

        Returns:
            float: Rasio kesamaan antara 0.0 hingga 1.0.
        """
        return difflib.SequenceMatcher(None, text1, text2).ratio()

    def calculate_reduction(self, plagiarism_percent, threshold=80, max_reduction=20):
        """
        Menghitung pengurangan nilai berdasarkan persentase plagiasi.

        Args:
            plagiarism_percent (float): Persentase plagiasi.
            threshold (float, optional): Batas minimum persentase plagiasi untuk pengurangan nilai. Default adalah 80.
            max_reduction (float, optional): Pengurangan nilai maksimal yang diizinkan. Default adalah 20.

        Returns:
            float: Persentase pengurangan nilai.
        """
        if plagiarism_percent <= threshold:
            return 0.0
        elif plagiarism_percent >= 100:
            return max_reduction
        else:
            return ((plagiarism_percent - threshold) / (100 - threshold)) * max_reduction

    def process_plagiarism(self, files_content, threshold, max_reduction):
        """
        Memproses pengecekan plagiasi antara berbagai file.

        Args:
            files_content (dict): Dictionary dengan key sebagai nama file dan value sebagai konten file.
            threshold (float): Batas minimum persentase kesamaan untuk mengurangi nilai.
            max_reduction (float): Pengurangan maksimal nilai yang diperbolehkan.

        Returns:
            tuple: (df_similarity, df_reduction)
                - df_similarity (pd.DataFrame): DataFrame berisi persentase kesamaan antar file.
                - df_reduction (pd.DataFrame): DataFrame berisi persentase pengurangan nilai per file.
        """
        if len(files_content) < 2:
            raise ValueError("Pastikan ada setidaknya dua file untuk dibandingkan.")

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
                "Nama File": student,
                "Persentase Pengurangan Nilai (%)": round(reduction, 2) if isinstance(reduction, float) else reduction
            }
            for student, reduction in reduction_dict.items()
        ]

        df_reduction = pd.DataFrame(data_reduction)
        df_reduction = df_reduction.sort_values(by="Persentase Pengurangan Nilai (%)", ascending=False)

        data_similarity = [
            {
                "File 1": file1,
                "File 2": file2,
                "Kesamaan (%)": sim
            }
            for file1, file2, sim in similarities
        ]

        df_similarity = pd.DataFrame(data_similarity)
        df_similarity = df_similarity.sort_values(by="Kesamaan (%)", ascending=False)

        return df_similarity, df_reduction
