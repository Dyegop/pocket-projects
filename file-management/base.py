"""
Class Files defines all files in a given path, filtered by file extension and a keyword (optionally).
Hidden files can be selected or not.
"""

import sys
import csv
import PyPDF2
from pathlib import Path
from typing import Tuple, List, Union


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
               f"Keyword filter: {self.keyword_filter}.\n"

    def __getitem__(self, keyword) -> List[str]:
        """
        Get files that contains given keyword.
        Usage: Files_obj[keyword]
        """
        return list(filter(lambda x: keyword in x, self._files))

    def list_files(self) -> List[str]:
        """ Return a list of filenames in the directory. """
        return self._files

    def read_document(self, file: Path, enconding: str = 'utf8') -> Union[str, Tuple[bool, str]]:
        """
        Read document files (files that are in FILE_EXTENSION['DOCUMENT']).
        :param file: filepath as Path object.
        :param enconding: enconding for .txt or .csv files.
        """
        if file.name not in self._files:
            return False, "File not found."

        if file.suffix not in FILE_EXTENSIONS['DOCUMENT']:
            return False, f"File is not of type {FILE_EXTENSIONS['DOCUMENT']}."

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
                    return '\n'.join([pdf_obj.getPage(page).extractText() for page in range(0, pdf_obj.numPages)])
            else:
                return False, "File extension currently not supported."
        except PermissionError:
            print(f"Permission denied: can't open file {file}")
        except UnicodeDecodeError:
            print("Encode error. Try different encoding.")

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



def get_user_input() -> Tuple[str, str, str, bool]:
    """ Return user input. """
    try:
        path = input("Root path: ")
        file_ext = input("Select file extension: from AUDIO/PICTURE/VIDEO/DOCUMENT/ALL: ").upper()

        if not file_ext:
            file_ext = 'ALL'
        print(f"{file_ext} selected")

        keyword_filter = input("Filter file-management by keyword [leave it blank to skip]: ").lower()  # NOT CASE SENSITIVE
        hidden_files = input("Show hidden file-management? Y/N: ").upper()
        print()

        if hidden_files in ("Y", "YES"):
            return path, file_ext, keyword_filter, True
        elif hidden_files in ("N", "NO"):
            return path, file_ext, keyword_filter, False
        else:
            print("ERROR - Invalid input given.")
            raise sys.exit(1)

    except KeyError:
        print("ERROR - Incorrect file type selected.")
        print("Valid options: AUDIO, PICTURE, VIDEO, DOCUMENT, ALL.")
        raise sys.exit(1)

    except FileNotFoundError:
        print("ERROR - Incorrect path selected.")
        print("Please, provide a valid directory.")
        raise sys.exit(1)
