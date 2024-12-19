# --- Day 19: Linen Layout ---
import functools
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> tuple[set[str], list[str]]:
    patterns, designs = s.strip().split("\n\n")
    patterns = set(patterns.split(", "))
    designs = designs.split("\n")
    return patterns, designs


def part_1(s: str) -> int:
    patterns, designs = parse(s)

    def solve(design: str) -> bool:
        paths = [design]
        while paths:
            d = paths.pop()
            if not d:
                return True
            for p in patterns:
                if d.startswith(p):
                    paths.append(d.removeprefix(p))
        return False

    return sum(solve(design) for design in designs)


def part_2(s: str) -> int:
    patterns, designs = parse(s)

    @functools.cache
    def solve(d: str) -> int:
        if not d:
            return 1
        return sum(solve(d.removeprefix(p)) for p in patterns if d.startswith(p))

    return sum(solve(design) for design in designs)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
