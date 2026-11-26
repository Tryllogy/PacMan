import copy
import json5
from pathlib import Path
from typing import Any, Iterable, Mapping
from pydantic import BaseModel, Field, ValidationError, model_validator

DEFAULT_CONFIG = {
    "highscore_filename": "score.json",
    "levels": [],
    "lives": 3,
    "points_per_pacgum": 10,
    "points_per_super_pacgum": 50,
    "points_per_ghost": 200,
    "seed": 42,
    "level_max_time": 90
}


class ErrorParsing(Exception):
    """Raised when the configuration file cannot be parsed."""

    def __init__(self, *args: str) -> None:
        """Forward the error message(s) to the base ``Exception``."""
        super().__init__(*args)


def _default_levels() -> list["Level"]:
    """Return the 10 default levels used when none are provided."""
    return [Level(name=f"Level {i + 1}") for i in range(10)]


class Level(BaseModel):
    """A single game level with its name and grid dimensions."""

    name: str = Field(default="Level", min_length=1, max_length=20)
    width: int = Field(ge=10, default=10)
    height: int = Field(ge=10, default=10)


class Data(BaseModel):
    """Validated game configuration with defaults for every field."""

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
        """Force 'highscore_filename' back to the default if it isn't a .json.
        """
        if not self.highscore_filename.endswith('.json'):
            print(
                "Config: 'highscore_filename' is not a .json file "
                f"({self.highscore_filename!r}); using default 'score.json'"
            )
            self.highscore_filename = 'score.json'
        return self


class Parser():
    """Read a config file and expose it as validated :class:`Data`."""

    def __init__(self, path: Path) -> None:
        """Parse ``path``, falling back to defaults if it can't be read."""
        self.path = path
        self.duplicate_keys: set[str] = set()
        try:
            self.data = self.clean_json()
        except Exception:
            print(f"Config: failed to parse {self.path}; "
                  "using default configuration")
            self.data = Data()

    def clean_json(self) -> Any:
        """Strip ``#`` comments outside strings and parse the JSON5 content."""
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
        return json5.loads(result, object_pairs_hook=self._dedup)

    def get_data(self) -> Data:
        """Return the validated config, unwrapping a list-wrapped root object.
        """
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
        duplicate_keys: set[str] = getattr(self, "duplicate_keys", set())
        copy_data: dict = copy.deepcopy(raw)
        data: dict = {}
        for k, v in copy_data.items():
            if k not in DEFAULT_CONFIG:
                print(f"Config: unknown key '{k}'; ignoring it")
            else:
                data[k] = v
        for k in DEFAULT_CONFIG:
            if k in duplicate_keys:
                print(f"Config: duplicate key '{k}' found; using "
                      "default value")
            elif k not in data:
                print(f"Config: missing key '{k}'; using default value")
        for _ in range(100):
            try:
                return Data.model_validate(data)
            except ValidationError as e:
                if not self._repair(data, e.errors()[0]):
                    print("Config: unrecoverable errors; using defaults")
                    return Data()
        return Data()

    def _repair(self, data: dict, err: Mapping[str, Any]) -> bool:
        """Drop the value flagged by one pydantic error; return whether it did.

        Locates the offending field from the error's ``loc`` path and removes
        it (or the invalid level) so its default applies. Returns ``False``
        when nothing could be repaired, letting the caller give up.
        """
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

    def _dedup(self, pairs: Iterable[tuple[str, Any]]) -> dict:
        """Drop duplicate keys from every object so defaults apply.

        Called by ``json5.loads`` for each JSON object (nested ones too). A key
        appearing more than once is removed entirely from the object, so the
        model default takes over. Duplicates in the top-level config object are
        recorded in ``self.duplicate_keys`` for reporting; duplicates inside
        nested objects (e.g. a level) are dropped silently.
        """
        pairs = list(pairs)  # iterated twice below
        counts: dict[str, int] = {}
        for key, _ in pairs:
            counts[key] = counts.get(key, 0) + 1
        duplicates = {k for k, c in counts.items() if c > 1}
        if duplicates and any(k in DEFAULT_CONFIG for k in counts):
            self.duplicate_keys |= duplicates
        return {key: value for key, value in pairs if counts[key] == 1}
