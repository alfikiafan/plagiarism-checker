# /model/file_reader.py

import os
from docx import Document
import PyPDF2

class FileReader:
    programming_extensions = [
        '.py', '.java', '.js', '.c', '.cpp', '.h', '.hpp', 
        '.html', '.css', '.php', '.sql', '.rb', '.go', 
        '.rs', '.kt', '.swift'
    ]

    def read_file(self, filepath):
        """
        Membaca file berdasarkan ekstensi dan mengembalikan konten sebagai string.

        Args:
            filepath (str): Path lengkap ke file yang akan dibaca.

        Returns:
            str: Konten file dalam bentuk string.

        Raises:
            IOError: Jika terjadi kesalahan saat membaca file.
        """
        ext = os.path.splitext(filepath)[1].lower()
        try:
            if ext == '.docx':
                return self.read_docx(filepath)
            elif ext == '.pdf':
                return self.read_pdf(filepath)
            else:
                return self.read_text(filepath)
        except Exception as e:
            raise IOError(f"Error membaca file {filepath}: {e}")

    def read_text(self, filepath):
        """
        Membaca file teks (.txt).

        Args:
            filepath (str): Path lengkap ke file .txt.

        Returns:
            str: Konten file teks.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    def read_docx(self, filepath):
        """
        Membaca file .docx.

        Args:
            filepath (str): Path lengkap ke file .docx.

        Returns:
            str: Konten file .docx.
        """
        doc = Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])

    def read_pdf(self, filepath):
        """
        Membaca file .pdf.

        Args:
            filepath (str): Path lengkap ke file .pdf.

        Returns:
            str: Konten file .pdf.
        """
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
        return text
