# --- Day 13: Claw Contraption ---
import re
from pathlib import Path

from util import Vec

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str):
    blocks = [block.splitlines() for block in s.split("\n\n")]
    machines = [list(map(parse_vec, block)) for block in blocks]
    return machines


def parse_vec(line: str) -> Vec:
    m = re.match(r".+?X[+=](?P<x>\d+), Y[+=](?P<y>\d+)", line)
    return Vec(x=int(m.group("x")), y=int(m.group("y")))


def solve(a, b, target) -> int:
    count_a = (target.x * b.y - target.y * b.x) / (a.x * b.y - a.y * b.x)
    count_b = (target.y - count_a * a.y) / b.y
    if count_a > 0 and count_b > 0 and count_a.is_integer() and count_b.is_integer():
        return int(count_a * 3 + count_b)
    return 0


def part_1(s: str) -> int:
    machines = parse(s)
    return sum(solve(*m) for m in machines)


def part_2(s: str) -> int:
    machines = parse(s)
    return sum(
        solve(a, b, prize + Vec(10000000000000, 10000000000000))
        for a, b, prize in machines
    )


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
