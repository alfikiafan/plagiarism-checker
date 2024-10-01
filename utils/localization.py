import json
import os

class Localization:
    def __init__(self, lang="en"):
        """
        Initialize the Localization class with the given language code.
        Default language is English ("en").
        """
        self.lang = lang
        self.translations = self.load_translations()

    def load_translations(self):
        """
        Load the translations from the JSON file for the specified language.
        Raises an exception if the file is not found.
        """
        try:
            file_path = os.path.join(os.path.dirname(__file__), f'../locales/{self.lang}.json')
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Translation file for '{self.lang}' not found. Falling back to English.")
            return self.load_default_language()

    def load_default_language(self):
        """
        Load English as the default language if the specified language file is missing.
        """
        file_path = os.path.join(os.path.dirname(__file__), '../locales/en.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def get(self, key):
        """
        Retrieve the translation for the specified key.
        If the key is not found, return the key itself (as a fallback).
        """
        return self.translations.get(key, key)
