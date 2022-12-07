"""
Class Files defines all files in a given path, filtered by file extension and a keyword (optionally).
Hidden files can be selected or not.
"""

import csv
import PyPDF2
from pathlib import Path
from typing import Tuple, List


# Valid filetype filters
FILE_EXTENSIONS = {
    'AUDIO': ('.mp3', '.flac', '.m4a', '.wav'),
    'PICTURE': ('.jpg', '.jpeg', '.png', '.gif', '.psd'),
    'VIDEO': ('.mp4', '.avi', '.mkv'),
    'DOCUMENT': ('.txt', '.csv', '.docx', '.pdf', '.xlsx'),
    'ALL': '.'
}


class Files:
    def __init__(self, path: Path, file_ext: Tuple[str, ...] = FILE_EXTENSIONS['ALL'], keyword_filter: str = '',
                 hidden_files: bool = False):
        self.path = path
        self.file_ext = file_ext
        self.keyword_filter = keyword_filter
        self.hidden_files = hidden_files

        # Files
        self._files = sorted([f.name for f in self._get_filepaths()], key=str.casefold)

    def __str__(self) -> str:
        return f"Object that represents files at {self.path}\n" \
               f"View hidden files set to {self.hidden_files}\n" \
               f"Keyword filter: {self.keyword_filter}\n"

    def __getitem__(self, keyword) -> List[str]:
        """
        Get files that contains given keyword.
        Usage: Files_obj[keyword]
        """
        return list(filter(lambda x: keyword in x, self._files))

    def list_files(self) -> List[str]:
        """ Return a list of filenames in the directory. """
        return self._files

    def read_document(self, file: Path, enconding: str = 'utf8') -> str:
        """
        Read document files (files that are in FILE_EXTENSION['DOCUMENT']).
        :param file: filepath as Path object.
        :param enconding: sets an enconding for .txt or .csv files.
        """
        if file.name in self._files:
            if file.suffix in FILE_EXTENSIONS['DOCUMENT']:
                try:
                    if file.suffix == '.txt':
                        with open(file, 'r', encoding=enconding) as f:
                            return f.read()
                    elif file.suffix == '.csv':
                        with open(file, 'r', encoding=enconding) as f:
                            return '\n'.join(str(row) for row in csv.reader(f))
                    elif file.suffix == '.pdf':
                        with open(file, 'rb') as f:
                            pdf_obj = PyPDF2.PdfFileReader(f)
                            return '\n'.join(
                                [pdf_obj.getPage(page).extractText() for page in range(0, pdf_obj.numPages)])
                    else:
                        return "File extension currently not supported."
                except PermissionError:
                    print(f"Permission denied: can't open file {file}")
                except UnicodeDecodeError:
                    print("Encode error. Try different encoding.")
            else:
                return f"File is not of type {FILE_EXTENSIONS['DOCUMENT']}"
        else:
            return "File not found."

    def _get_filepaths(self) -> List[Path]:
        """ Return a list of all the filepaths in the directory. """
        paths = []
        for path in self.path.iterdir():
            if not path.is_file():
                continue
            if not self.hidden_files and (path.name[0] == '.' or path.name == "desktop.ini"):
                continue
            if any(extension in path.suffix for extension in self.file_ext) and \
                    self.keyword_filter in path.stem.lower():
                paths.append(path)
        return paths
