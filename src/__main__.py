import sys
from .parsing.parser import Parser
from pathlib import Path


def main() -> None:
    if len(sys.argv) == 1:
        print("Missing args")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("Too many args")
        sys.exit(1)
    try:
        parser = Parser(Path(sys.argv[1]))
        data = parser.get_data()
        print(data.width)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
