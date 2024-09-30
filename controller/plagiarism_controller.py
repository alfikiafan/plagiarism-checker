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

        # Memeriksa apakah ada file yang berhasil dibaca
        if len(self.files_content) < 2:
            if len(error_files) == len(file_paths):
                raise ValueError("Semua file gagal dibaca. Tidak ada file yang bisa dibandingkan.")
            raise ValueError("Pastikan ada setidaknya dua file yang berhasil dibaca untuk dibandingkan.")

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

    def cluster_files_by_content(self, files_content, n_clusters=5):
        """
        Melakukan clustering terhadap file berdasarkan isi konten mereka.

        Args:
            files_content (dict): Dictionary berisi path file dan konten file.
            n_clusters (int): Jumlah cluster yang diinginkan.

        Returns:
            dict: Mapping dari basename file ke nomor cluster.
        """
        # Step 1: Vectorize the content of each file using TF-IDF
        vectorizer = TfidfVectorizer(stop_words='english')
        file_paths = list(files_content.keys())  # Path lengkap file
        contents = list(files_content.values())

        # Mengubah konten file menjadi representasi numerik
        tfidf_matrix = vectorizer.fit_transform(contents)

        # Step 2: Lakukan clustering dengan KMeans
        kmeans = KMeans(n_clusters=n_clusters, random_state=0)
        kmeans.fit(tfidf_matrix)

        # Step 3: Hasil clustering (basename file_name -> cluster_number)
        file_cluster_mapping = {os.path.basename(file_paths[i]): kmeans.labels_[i] for i in range(len(file_paths))}

        return file_cluster_mapping