import re
from PyPDF2 import PdfFileReader
import os
from dataclasses import dataclass
import pandas as pd


@dataclass
class PDFParser:
    """Base class to parse PDF and find some elements by regex."""
    path: str

    def __post_init__(self):
        data = self.get_data_from_parsed_pdf()
        self.data = pd.DataFrame(
            data, columns=["UII", 'UII parsed', "Investment Title parsed"])

    def get_files(self):
        _, _, files = list(os.walk(self.path))[0]
        return files

    def get_data_from_parsed_pdf(self):
        data = []
        files = self.get_files()
        for filename in files:
            if filename.split('.')[-1] == 'pdf':
                name = f"{self.path}/{filename}"
                raw = PdfFileReader(name)
                text = raw.getPage(0).extractText()
                names_regex = r"^1. Name of this Investment:\s+([^\n\r]*)"
                uii_regex = r"^2. Unique Investment Identifier \x28UII\x29:\s+([^\n\r]*)"
                r1 = self.find_text_by_key(names_regex, text)
                r2 = self.find_text_by_key(uii_regex, text)
                uui = filename.split('.')[0]
                data.append([uui, r2, r1])
        return data

    def find_text_by_key(self, regex, text):
        matches = re.finditer(regex, text, re.MULTILINE)
        for _, match in enumerate(matches, start=1):
            return match.groups()[0]
