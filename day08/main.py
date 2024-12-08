# --- Day 8: Resonant Collinearity ---
import itertools
from pathlib import Path
from util import Grid, Vec

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> tuple[Grid, dict[str, list[Vec]]]:
    grid = Grid.from_string(s)
    freqs = dict()
    for freq in set(s) - {".", "\n"}:
        freqs[freq] = list(grid.find_iter(freq))
    return grid, freqs


def part_1(s: str) -> int:
    grid, freqs = parse(s)
    antinodes = set()
    for freq, positions in freqs.items():
        for a, b in itertools.combinations(positions, 2):
            delta = b - a
            antinodes.add(b + delta)
            antinodes.add(a - delta)
    return sum(not grid.oob(pos) for pos in antinodes)


def part_2(s: str) -> int:
    grid, freqs = parse(s)
    antinodes = set(itertools.chain.from_iterable(freqs.values()))
    for freq, positions in freqs.items():
        for a, b in itertools.combinations(positions, 2):
            delta = b - a
            for pos, d in ((a, -delta), (b, delta)):
                while not grid.oob(pos := pos + d):
                    antinodes.add(pos)
    return len(antinodes)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
