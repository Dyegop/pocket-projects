"""
A simple program to rename files sequentially.
Class Files defines all files in a given path, filtered by file extension.
Optionally, hidden files can be selected or not.
"""

import sys
from pathlib import Path
from typing import Tuple, List




# Default directory
TEST_PATH = Path("~/Documents/Rename").expanduser()

# Filetype filters
VALID_FILETYPES = {
    'AUDIO': ('.mp3', '.flac', '.m4a', '.wav'),
    'PICTURE': ('.jpg', '.jpeg', '.png', '.gif', '.psd'),
    'VIDEO': ('.mp4', '.avi', '.mkv'),
    'DOCUMENT': ('.txt', '.docx', '.pdf', '.xlsx'),
    'ALL': '.'
}


class Files:
    # By default,
    def __init__(self, path: Path, filetype: Tuple[str], view_hidden: bool = False):
        self.path = path
        self.filetype = filetype
        self.view_hidden = view_hidden

    def __str__(self) -> str:
        return f"Object representing of files located at {self.path}"

    def list_files(self) -> List[str]:
        """
        Return a list of filenames in the directory
        """
        return sorted([f.name for f in self._get_filepaths()], key=str.casefold)

    def rename_files(self, pattern: str) -> None:
        """
        Rename a group of files using a pattern.
        """
        files = self._get_filepaths()

        print(f"Found the following files at {self.path}:")
        print(*self.list_files(), sep='\n')

        for file in files:
            new_name = self._get_new_name(file.name, pattern)
            if files.index(file) == 0:
                print(f"Files will be renamed in the following format: {new_name}")
                _continue = input("Continue? -> Y/N\n").upper()
                if _continue == "Y":
                    pass
                elif _continue == "N":
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
            if not self.view_hidden and (path.name[0] == '.' or path.name == "desktop.ini"):
                continue
            else:
                if path.is_file() and any(extension in path.suffix for extension in self.filetype):
                    paths.append(path)
        return paths

    @staticmethod
    def _get_new_name(filename: str, pattern: str) -> str:
        """
        Return new filename for a given pattern.
        Current supported pattern:
            -REMOVE_WHITESPACES -> remove whitespaces of a string
            -OPPO_PICTURE -> remame Oppo phone photos in the format YYYYMMDD_hhmmss
            -OPPO_VIDEO -> remame Oppo phone videos in the format VID_YYYYMMDD_hhmmss
            -LG_PICTURE -> remame LG phone photos in the format YYYYMMDD_hhmmss
            -LG_VIDEO -> remame LG phone videos in the format VID_YYYYMMDD_hhmmss
        """
        if pattern == "REMOVE_WHITESPACES":
            return f"{filename.replace(' ', '')}"
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




if __name__ == "__main__":
    print("A script to rename files sequentially")

    user_path = input("Type a path where files to rename are located: ")
    print("Select a file filter: AUDIO, PICTURE, VIDEO, DOCUMENT or ALL")
    user_file_types = input().upper()

    try:
        F = Files(path=Path(user_path), filetype=VALID_FILETYPES[user_file_types])
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

    print("Select pattern to rename files: \n"
          "-REMOVE_WHITESPACES -> remove whitespaces of a string\n"
          "-OPPO_PICTURE       -> remame Oppo phone photos in the format YYYYMMDD_hhmmss\n"
          "-OPPO_VIDEO         -> remame Oppo phone videos in the format VID_YYYYMMDD_hhmmss\n"
          "-LG_PICTURE         -> remame LG phone photos in the format YYYYMMDD_hhmmss\n"
          "-LG_VIDEO           -> remame LG phone videos in the format VID_YYYYMMDD_hhmmss")
    rename_pattern = input().upper()

    F.rename_files(rename_pattern)
