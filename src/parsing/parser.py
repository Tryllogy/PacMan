from pathlib import Path
import json


class ErrorParsing(Exception):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)


class Parser():
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = self.clean_json()

    def check_path(self) -> None:
        if not self.path.is_file():
            raise ErrorParsing(
                f"path doesnt exist or is not a file: {self.path}")

    def clean_json(self) -> list:
        result = ""
        i = 0
        in_string = False
        with open(self.path) as f:
            raw_file = f.read()
            while i < len(raw_file):
                c = raw_file[i]

                if c == '"' and (i == 0 or raw_file[i - 1] != '\\'):
                    in_string = not in_string
                if not in_string:
                    if raw_file[i: i + 2] == "//":
                        i += 2
                        while i < len(raw_file) and raw_file[i] != '\n':
                            i += 1
                        continue
                    if raw_file[i: i + 2] == '/*':
                        i += 2
                        while i < len(raw_file) and raw_file[i] != '\n':
                            i += 1
                        continue
                    if raw_file[i] == '#':
                        i += 1
                        while i < len(raw_file) and raw_file[i] != '\n':
                            i += 1
                        continue
                result += c
                i += 1
        return json.loads(result)

    def get_data(self) -> list:
        return self.data
