# --- Day 1: Historian Hysteria ---

from pathlib import Path
from collections import Counter

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s) -> tuple[list[int], list[int]]:
    columns = [line.split() for line in s.splitlines()]
    left = sorted(int(c[0]) for c in columns)
    right = sorted(int(c[1]) for c in columns)
    return left, right


def part_1(s: str) -> int:
    left, right = parse(s)
    return sum(abs(a - b) for a, b in zip(left, right))


def part_2(s: str) -> int:
    left, right = parse(s)
    occ = Counter(right)
    return sum(x * occ[x] for x in left)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
