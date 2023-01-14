"""
A simple program to rename file-management sequentially, using predetermined formats
"""

import sys
import base
from pathlib import Path
from typing import Optional


class FileRenamer(base.Files):
    def rename_files(self, pattern: str, text_to_remove: Optional[str] = None) -> None:
        """ Rename a group of file-management using a pattern. """
        _files = self._get_filepaths()

        for file in _files:
            if text_to_remove:
                new_name = self._replace_filename(file.name, pattern, text_to_remove)
            else:
                new_name = self._replace_filename(file.name, pattern)

            if _files.index(file) == 0:
                print(f"Files will be renamed in the following format: {new_name}")
                _continue = input("Continue? -> Y/N\n").upper()
                if _continue in ('Y', 'YES'):
                    pass
                elif _continue == ('N', 'NO'):
                    print("Process cancelled")
                    break
                else:
                    print("Invalid option. Process stopped")
                    break
            file.rename(Path(f'{file.parents[0]}\\{new_name}'))
            print(f"{file.name} renamed to {new_name}")

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
        if pattern in ('REMOVE_WHITESPACES', '1'):
            return f"{filename.replace(' ', '')}"
        elif pattern in ('REMOVE_TEXT', '2'):
            return f"{filename.replace(text_to_remove, '')}"
        elif pattern in ('PIXEL_PICTURE', '3'):
            return f"{filename[4:18]}_{filename[22:]}"
        elif pattern in ('PIXEL_VIDEO', '4'):
            return f""
        elif pattern in ('OPPO_PICTURE', '5'):
            return f"{filename[3:11]}_{filename[11:]}"
        elif pattern in ('OPPO_VIDEO', '6'):
            return f"{filename[0:3]}_{filename[3:11]}_{filename[11:]}"
        elif pattern in ('LG_PICTURE', '7'):
            return f"{filename[4:12]}_{filename[13:19]}.jpg"
        elif pattern in ('LG_VIDEO', '8'):
            return f"{filename[0:19]}.mp4"
        else:
            print("ERROR - Invalid pattern.")
            raise sys.exit(1)

    @staticmethod
    def select_pattern() -> str:
        """ Return rename pattern selected by the user. """
        print("Select pattern to rename file-management: \n"
              "1) REMOVE_WHITESPACES -> remove whitespaces from filename\n"
              "2) REMOVE_TEXT        -> remove a given text from filename\n"
              "3) PIXEL_PICTURE      -> remame Pixel photos in the format YYYYMMDD_hhmmss\n"
              "4) PIXEL_VIDEO        -> remame Pixel videos in the format VID_YYYYMMDD_hhmmss\n"
              "5) OPPO_PICTURE       -> remame Oppo photos in the format YYYYMMDD_hhmmss\n"
              "6) OPPO_VIDEO         -> remame Oppo videos in the format VID_YYYYMMDD_hhmmss\n"
              "7) LG_PICTURE         -> remame LG photos in the format YYYYMMDD_hhmmss\n"
              "8) LG_VIDEO           -> remame LG videos in the format VID_YYYYMMDD_hhmmss")
        return input().upper()




if __name__ == "__main__":
    print("---- Script to rename file-management ----\n")
    try:
        user_path, user_file_ext, user_keyword, user_hidden_files = base.get_user_input()

        F = FileRenamer(path=Path(user_path),
                        file_ext=base.FILE_EXTENSIONS[user_file_ext],
                        keyword_filter=user_keyword,
                        hidden_files=user_hidden_files)
        print(f"Found the following files at {user_path}:")
        print(*F.list_files(), sep='\n')
        print()

        if not F.list_files():
            print(f"No files found at {user_path}")
            raise sys.exit(0)

        rename_pattern = F.select_pattern()

        if rename_pattern in ('REMOVE_TEXT', '2'):
            user_text_to_remove = input("Type text to remove: ")  # case sensitive
            F.rename_files(rename_pattern, user_text_to_remove)
        else:
            F.rename_files(rename_pattern)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
        raise sys.exit(1)
