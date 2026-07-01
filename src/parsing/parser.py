from pathlib import Path
from pydantic import BaseModel, Field, model_validator
import json
import os


class ErrorParsing(Exception):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)


class Level(BaseModel):
    width: int = Field(ge=10, default=10)  # 10 / 10
    height: int = Field(ge=10, default=10)  # 10 / 10


class Data(BaseModel):
    highscore_filename: str = 'score.json'  # "Score.json"
    levels: list[Level]
    lives: int = Field(ge=3, default=3)  # 3 / 3
    points_per_pacgum: int = Field(ge=1, default=10)  # 1 / 10
    points_per_super_pacgum: int = Field(ge=1, default=50)  # 1 / 50
    points_per_ghost: int = Field(ge=1, default=200)  # 1 / 200
    seed: int = 42  # 42
    level_max_time: int = Field(ge=60, default=90)  # 60 / 90

    @model_validator(mode='after')
    def filename_validator(self) -> 'Data':
        if not self.highscore_filename.endswith('.json'):
            raise ErrorParsing(
                'highscore filename is not a json file: '
                f'{self.highscore_filename}'
            )
        directory = os.path.dirname(self.highscore_filename)
        if not Path(directory).exists():
            raise ErrorParsing(
                f"highscore's directory doesnt exist: {directory}")
        return self


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

    def get_data(self) -> Data:
        data = Data.model_validate(self.data[0])
        return data
