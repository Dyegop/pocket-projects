"""
A simple program to rename files sequentially.
Class Files defines all files in a given path, filtered by file extension.
Optionally, hidden files can be selected or not.
"""

import sys
from pathlib import Path
from typing import Tuple, List, Optional




# Default directory
DEFAULT_PATH = Path("~/Documents/Rename").expanduser()


# Filetype filters
VALID_FILETYPES = {
    'AUDIO': ('.mp3', '.flac', '.m4a', '.wav'),
    'PICTURE': ('.jpg', '.jpeg', '.png', '.gif', '.psd'),
    'VIDEO': ('.mp4', '.avi', '.mkv'),
    'DOCUMENT': ('.txt', '.docx', '.pdf', '.xlsx'),
    'ALL': '.'
}



class Files:
    def __init__(self, path: Path, filetype: Tuple[str], keyword_filter: str = '', hidden_files: bool = False):
        self.path = path
        self.filetype = filetype
        self.keyword_filter = keyword_filter
        self.hidden_files = hidden_files

    def __str__(self) -> str:
        return f"Object representation of files located at {self.path}\n" \
               f"View hidden files set to {self.hidden_files}\n" \
               f"Keyword filter used: {self.keyword_filter}\n"

    def list_files(self) -> List[str]:
        """
        Return a list of filenames in the directory.
        """
        return sorted([f.name for f in self._get_filepaths()], key=str.casefold)

    def rename_files(self, pattern: str, text_to_remove: Optional[str] = None) -> None:
        """
        Rename a group of files using a pattern.
        """
        files = self._get_filepaths()

        for file in files:
            if text_to_remove:
                new_name = self._replace_filename(file.name, pattern, text_to_remove)
            else:
                new_name = self._replace_filename(file.name, pattern)

            if files.index(file) == 0:
                print(f"Files will be renamed in the following format: {new_name}")
                _continue = input("Continue? -> Y/N\n").upper()
                if _continue == "Y" or _continue == "YES":
                    pass
                elif _continue == "N" or _continue == "NO":
                    print("Process cancelled")
                    break
                else:
                    print("Invalid option. Process stopped")
                    break
            file.rename(Path(f'{file.parents[0]}\\{new_name}'))
            print(f"{file.name} renamed to {new_name}")

    def _get_filepaths(self) -> List[Path]:
        """
        Return a list of all the filepaths in the directory.
        """
        paths = []
        for path in self.path.iterdir():
            if not path.is_file():
                continue
            if not self.hidden_files and (path.name[0] == '.' or path.name == "desktop.ini"):
                continue
            if any(extension in path.suffix for extension in self.filetype) and self.keyword_filter in path.stem.lower():
                paths.append(path)
        return paths

    @staticmethod
    def _replace_filename(filename: str, pattern: str, text_to_remove: Optional[str] = None) -> str:
        """
        Return new filename for a given pattern.
        Current supported pattern:
            -REMOVE_WHITESPACES -> remove whitespaces
            -REMOVE_TEXT -> remove a given string
            -OPPO_PICTURE -> remame Oppo phone photos in the format YYYYMMDD_hhmmss
            -OPPO_VIDEO -> remame Oppo phone videos in the format VID_YYYYMMDD_hhmmss
            -LG_PICTURE -> remame LG phone photos in the format YYYYMMDD_hhmmss
            -LG_VIDEO -> remame LG phone videos in the format VID_YYYYMMDD_hhmmss
        """
        if pattern == "REMOVE_WHITESPACES":
            return f"{filename.replace(' ', '')}"
        if pattern == "REMOVE_TEXT":
            return f"{filename.replace(text_to_remove, '')}"
        elif pattern == "OPPO_PICTURE":
            return f"{filename[3:11]}_{filename[11:]}"
        elif pattern == "OPPO_VIDEO":
            return f"{filename[0:3]}_{filename[3:11]}_{filename[11:]}"
        elif pattern == "LG_PICTURE":
            return f"{filename[4:12]}_{filename[13:19]}.jpg"
        elif pattern == "LG_VIDEO":
            return f"{filename[0:19]}.mp4"
        else:
            print("ERROR - Invalid pattern")
            raise sys.exit(1)


def select_user_input() -> Tuple[str, str, str, bool]:
    """
    Return selected input by the user.
    """
    path = input("Root path: ")
    filetype = input("Select filetype AUDIO/PICTURE/VIDEO/DOCUMENT/ALL: ").upper()
    keyword_filter = input("Filter files by keyword (leave it blank to skip): ").lower()  # NOT CASE SENSITIVE
    hidden_files = input("Show hidden files? Y/N: ").upper()
    if not filetype:
        filetype = 'ALL'
    if hidden_files == "Y" or hidden_files == "YES":
        return path, filetype, keyword_filter, True
    elif hidden_files == "N" or hidden_files == "NO":
        print("Process cancelled")
        return path, filetype, keyword_filter, False
    else:
        print("Invalid option. Process stopped")
        raise sys.exit(1)


def select_rename_pattern() -> str:
    """
    Return rename pattern selected by the user.
    """
    print("Select pattern to rename files: \n"
          "-REMOVE_WHITESPACES -> remove whitespaces from filename\n"
          "-REMOVE_TEXT        -> remove a given text from filename\n"
          "-OPPO_PICTURE       -> remame Oppo phone photos in the format YYYYMMDD_hhmmss\n"
          "-OPPO_VIDEO         -> remame Oppo phone videos in the format VID_YYYYMMDD_hhmmss\n"
          "-LG_PICTURE         -> remame LG phone photos in the format YYYYMMDD_hhmmss\n"
          "-LG_VIDEO           -> remame LG phone videos in the format VID_YYYYMMDD_hhmmss")
    return input().upper()




if __name__ == "__main__":
    print("Script to rename files")
    user_path, user_filetypes, user_keyword, user_hidden_files = select_user_input()

    try:
        F = Files(path=Path(user_path),
                  filetype=VALID_FILETYPES[user_filetypes],
                  keyword_filter=user_keyword,
                  hidden_files=user_hidden_files)
        print(f"Found the following files at {user_path}:")
        print(*F.list_files(), sep='\n')
        print()
    except KeyError:
        print("Incorrect file type selected")
        print("Valid options: AUDIO, PICTURE, VIDEO, DOCUMENT, ALL")
        raise sys.exit(1)
    except FileNotFoundError:
        print("Incorrect path selected")
        print("Please, provide a valid directory")
        raise sys.exit(1)

    if not F.list_files():
        print(f"No files found at {user_path}")
        raise sys.exit(0)

    rename_pattern = select_rename_pattern()

    if rename_pattern == 'REMOVE_TEXT':
        user_text_to_remove = input("Type text to remove: ")  # case sensitive
        F.rename_files(rename_pattern, user_text_to_remove)
    else:
        F.rename_files(rename_pattern)
