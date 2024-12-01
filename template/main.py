from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def part_1(s: str) -> int: ...


def part_2(s: str) -> int: ...


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
