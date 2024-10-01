import os
from docx import Document
from utils.constants import PROGRAMMING_EXTENSIONS
import PyPDF2

class FileReader:
    programming_extensions = PROGRAMMING_EXTENSIONS

    def __init__(self, localization):
        """
        Initializes the FileReader with a localization object for error messages.

        Args:
            localization (object): Localization object to fetch localized messages.
        """
        self.localization = localization

    def read_file(self, filepath):
        """
        Reads a file based on its extension and returns the content as a string.

        Args:
            filepath (str): Full path to the file to be read.

        Returns:
            str: The content of the file as a string.

        Raises:
            IOError: If an error occurs while reading the file.
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
            raise IOError(self.localization.get("file_read_error").format(filepath=filepath, error=str(e)))

    def read_text(self, filepath):
        """
        Reads a text file (.txt).

        Args:
            filepath (str): Full path to the .txt file.

        Returns:
            str: The content of the text file.
        """
        with open(filepath, 'r', encoding='utf-8') as file:
            return file.read()

    def read_docx(self, filepath):
        """
        Reads a .docx file.

        Args:
            filepath (str): Full path to the .docx file.

        Returns:
            str: The content of the .docx file.
        """
        doc = Document(filepath)
        return '\n'.join([para.text for para in doc.paragraphs])

    def read_pdf(self, filepath):
        """
        Reads a .pdf file.

        Args:
            filepath (str): Full path to the .pdf file.

        Returns:
            str: The content of the .pdf file.
        """
        with open(filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text
        return text
