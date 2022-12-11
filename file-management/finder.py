import base
import sys
import re
from pathlib import Path


class FileFinder(base.Files):
    def find_files(self, pattern: str) -> str:
        """ Return a list of filenames in a directory that matches a pattern """
        matches = [file for file in self.list_files() if re.search(re.compile(pattern, re.VERBOSE), file)]
        return '\n'.join(matches)

    def find_pattern_in_file(self, file: Path, pattern: str, enconding: str = 'utf8') -> str:
        """ Find lines in a document that matches a pattern.
        :param file: filepath as Path object.
        :param pattern: pattern to find.
        :param enconding: enconding for .txt or .csv files.
        """
        file_text = self.read_document(file, enconding=enconding)

        if type(file_text) is tuple and not file_text[0]:
            return file_text[1]
        return '\n'.join(re.findall(re.compile(pattern, re.VERBOSE), file_text))

    def execute_action(self, pattern: str) -> str:
        """ """
        print("Select action to execute: \n"
              "1) FIND_FILES                  -> find files that has the given pattern in their name\n"
              "2) FIND_PATTERN_IN_FILE        -> find files that contains the given pattern \n")

        action = input().upper()
        if action in ('1', 'FIND_FILES'):

            return self.find_files(pattern)
        elif action in ('2', 'FIND_PATTERN_IN_FILE'):
            try:
                filepath = input("Filepath: ")
                encoding = input("Encoding [leave it blank to use utf-8]: ")
                if encoding:
                    return self.find_pattern_in_file(Path(filepath), pattern, encoding)
                else:
                    return self.find_pattern_in_file(Path(filepath), pattern)
            except FileNotFoundError:
                print("File not found in the given path.")
                print("Are you sure this file exists?")
                raise sys.exit(1)
        else:
            print("ERROR - Invalid pattern")
            raise sys.exit(1)

    @staticmethod
    def select_pattern() -> str:
        """ Return regex pattern based on user input. """
        print("Select pattern to find in a file: \n"
              "1) EMAIL\n"
              "2) MOBILE_PHONE\n"
              "3) URL\n")

        pattern = input().upper()
        if pattern in ('1', 'EMAIL'):
            return r'([a-zA-Z\d._%+-]+@[a-zA-Z\d.-]+\.[a-zA-Z]{2,3})'
        elif pattern in ('2', 'MOBILE_PHONE'):
            return r'(6\d{8})'
        elif pattern in ('3', 'URL'):
            return 'https?://(?:[a-zA-Z]|\\d|[$-_@.&+]|[!*(),]|(:%[\\da-fA-F][\\da-fA-F]))+'
        else:
            print("ERROR - Invalid pattern.")
            raise sys.exit(1)




if __name__ == '__main__':
    print("---- Script to find files/patterns ----\n")

    try:
        user_path, user_file_ext, user_keyword, user_hidden_files = base.get_user_input()

        F = FileFinder(path=Path(user_path),
                       file_ext=base.FILE_EXTENSIONS[user_file_ext],
                       keyword_filter=user_keyword,
                       hidden_files=user_hidden_files)
        print(f"Found the following file-management at {user_path}:")
        print(*F.list_files(), sep='\n')
        print()

        user_pattern = F.select_pattern()
        result = F.execute_action(user_pattern)
        print("Found the following occurrences for the selected pattern: ")
        print(result)

    except KeyboardInterrupt:
        print("Program interrupted by user.")
        raise sys.exit(1)
