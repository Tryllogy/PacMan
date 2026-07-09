import json5
from pathlib import Path
from pydantic import BaseModel, Field, model_validator


class ErrorParsing(Exception):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)


class Level(BaseModel):
    name: str = Field(min_length=1, max_length=20)
    width: int = Field(ge=10, default=10)
    height: int = Field(ge=10, default=10)


class Data(BaseModel):
    highscore_filename: str = 'score.json'
    levels: list[Level] = Field(min_items=10)
    lives: int = Field(ge=3, default=3)
    points_per_pacgum: int = Field(ge=1, default=10)
    points_per_super_pacgum: int = Field(ge=1, default=50)
    points_per_ghost: int = Field(ge=1, default=200)
    seed: int = 42
    level_max_time: int = Field(ge=60, default=90)

    @model_validator(mode='after')
    def filename_validator(self) -> 'Data':
        if not self.highscore_filename.endswith('.json'):
            raise ErrorParsing(
                'highscore filename is not a json file: '
                f'{self.highscore_filename}'
            )
        return self


class Parser():
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = self.clean_json()

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
                    if raw_file[i] == '#':
                        i += 1
                        while i < len(raw_file) and raw_file[i] != '\n':
                            i += 1
                        continue
                result += c
                i += 1
        return json5.loads(result)

    def get_data(self) -> Data:
        data = Data.model_validate(self.data[0])
        return data
