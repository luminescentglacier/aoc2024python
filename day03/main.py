# --- Day 3: Mull It Over ---

from pathlib import Path
import re

INPUT_FILE = Path(__file__).parent / "input.txt"


def part_1(s: str) -> int:
    pattern = re.compile(r"mul\((\d+),(\d+)\)")
    matches = pattern.findall(s)
    res = sum(int(m[0]) * int(m[1]) for m in matches)
    return res


def part_2(s: str) -> int:
    pattern = re.compile(r"(?P<op>mul|do|don't)\(((?P<argv1>\d+),(?P<argv2>\d+))?\)")
    res = 0
    do = True
    for m in pattern.finditer(s):
        op, argv1, argv2 = m.group("op"), m.group("argv1"), m.group("argv2")
        match op:
            case "do":
                do = True
            case "don't":
                do = False
            case "mul" if do:
                res += int(argv1) * int(argv2)
            case _:
                continue
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
