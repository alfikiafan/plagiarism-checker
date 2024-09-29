# /controller/plagiarism_controller.py

from model.file_reader import FileReader
from model.plagiarism_checker import PlagiarismChecker
import os

class PlagiarismController:
    def __init__(self):
        self.file_reader = FileReader()
        self.plagiarism_checker = PlagiarismChecker()
        self.files_content = {}  # Menyimpan konten file yang telah dibaca

    def process_files(self, file_paths, threshold, max_reduction):
        """
        Memproses file-file yang dipilih untuk pengecekan plagiasi.

        Args:
            file_paths (list): Daftar path file yang akan diproses.
            threshold (float): Batas minimum persentase kesamaan untuk mengurangi nilai.
            max_reduction (float): Pengurangan maksimal nilai yang diperbolehkan.

        Returns:
            tuple: (df_similarity, df_reduction, error_files)
                - df_similarity (pd.DataFrame): DataFrame berisi persentase kesamaan antar file.
                - df_reduction (pd.DataFrame): DataFrame berisi persentase pengurangan nilai per file.
                - error_files (dict): Dictionary berisi file yang gagal diproses beserta error-nya.
        """
        self.files_content = {}
        error_files = {}

        # Membaca semua file yang dipilih
        for path in file_paths:
            try:
                content = self.file_reader.read_file(path)
                self.files_content[path] = content
            except IOError as e:
                error_files[path] = str(e)

        # Memeriksa apakah ada cukup file untuk dibandingkan
        if len(self.files_content) < 2:
            raise ValueError("Pastikan ada setidaknya dua file untuk dibandingkan.")

        # Memproses plagiasi menggunakan PlagiarismChecker
        df_similarity, df_reduction = self.plagiarism_checker.process_plagiarism(
            self.files_content, threshold, max_reduction
        )

        return df_similarity, df_reduction, error_files

    def get_file_content(self, filename):
        """
        Mengambil konten file berdasarkan nama file.

        Args:
            filename (str): Nama file.

        Returns:
            str: Konten file.

        Raises:
            KeyError: Jika file tidak ditemukan.
        """
        # Mencari file berdasarkan basename
        for path, content in self.files_content.items():
            if os.path.basename(path) == filename:
                return content
        raise KeyError(f"File {filename} tidak ditemukan.")
