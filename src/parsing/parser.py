import copy
import json5
from pathlib import Path
from typing import Any, Mapping
from pydantic import BaseModel, Field, ValidationError, model_validator


class ErrorParsing(Exception):
    def __init__(self, *args: str) -> None:
        super().__init__(*args)


def _default_levels() -> list["Level"]:
    return [Level(name=f"Level {i + 1}") for i in range(10)]


class Level(BaseModel):
    name: str = Field(default="Level", min_length=1, max_length=20)
    width: int = Field(ge=10, default=10)
    height: int = Field(ge=10, default=10)


class Data(BaseModel):
    highscore_filename: str = 'score.json'
    levels: list[Level] = Field(default_factory=_default_levels, min_length=10)
    lives: int = Field(ge=3, default=3)
    points_per_pacgum: int = Field(ge=1, default=10)
    points_per_super_pacgum: int = Field(ge=1, default=50)
    points_per_ghost: int = Field(ge=1, default=200)
    seed: int = 42
    level_max_time: int = Field(ge=60, default=90)

    @model_validator(mode='after')
    def filename_validator(self) -> 'Data':
        if not self.highscore_filename.endswith('.json'):
            print(
                "Config: 'highscore_filename' is not a .json file "
                f"({self.highscore_filename!r}); using default 'score.json'"
            )
            self.highscore_filename = 'score.json'
        return self


class Parser():
    def __init__(self, path: Path) -> None:
        self.path = path
        self.data = self.clean_json()

    def clean_json(self) -> Any:
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
        raw = self.data
        if isinstance(raw, list):
            raw = raw[0] if raw else {}
        if not isinstance(raw, dict):
            print("Config: root is not an object; using default configuration")
            return Data()
        return self._sanitize(raw)

    def _sanitize(self, raw: dict) -> Data:
        """Clamp invalid/missing values to safe defaults and continue.

        On any validation error, the offending value is dropped (so the field
        default applies), a clear message is logged, and validation is retried.
        """
        data: dict = copy.deepcopy(raw)
        for _ in range(100):
            try:
                return Data.model_validate(data)
            except ValidationError as e:
                if not self._repair(data, e.errors()[0]):
                    print("Config: unrecoverable errors; using defaults")
                    return Data()
        return Data()

    def _repair(self, data: dict, err: Mapping[str, Any]) -> bool:
        loc = list(err.get('loc', ()))
        msg = err.get('msg', 'invalid value')
        if not loc:
            return False
        container: Any = data
        for key in loc[:-1]:
            try:
                container = container[key]
            except (KeyError, IndexError, TypeError):
                return False
        last = loc[-1]
        path = '.'.join(str(p) for p in loc)
        if isinstance(container, dict) and last in container:
            print(f"Config: invalid '{path}' ({msg}); using default")
            del container[last]
            return True
        if isinstance(container, list) and isinstance(last, int):
            if 0 <= last < len(container):
                print(f"Config: invalid level at index {last} "
                      f"({msg}); dropping it")
                del container[last]
                return True
        if loc[0] in data:
            print(f"Config: invalid '{loc[0]}' ({msg}); using default")
            del data[loc[0]]
            return True
        return False
