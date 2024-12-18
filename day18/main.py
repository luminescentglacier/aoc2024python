# --- Day 18: RAM Run ---
from enum import Enum
from pathlib import Path

from util import Grid, Vec

INPUT_FILE = Path(__file__).parent / "input.txt"

WIDTH = 71 if INPUT_FILE.stem == "input" else 7
HEIGHT = WIDTH

DIRECTIONS = (
    Vec(0, 1),
    Vec(0, -1),
    Vec(1, 0),
    Vec(-1, 0),
)


class Node(str, Enum):
    SPACE = "."
    CORRUPT = "#"

    def __str__(self) -> str:
        return self.value


class Maze(Grid):
    def dijkstra(self, start: Vec, end: Vec):
        distances = {
            Vec(x, y): float("inf")
            for y in range(self.height)
            for x in range(self.width)
        }
        distances[start] = 0.0
        unvisited = set(distances.keys())

        while unvisited:
            pos, d = min(
                ((k, v) for k, v in distances.items() if k in unvisited),
                key=lambda x: x[1],
            )
            unvisited.remove(pos)
            if pos == end:
                return distances

            for new_pos in (pos + direction for direction in DIRECTIONS):
                if self.oob(new_pos) or self[new_pos] == Node.CORRUPT:
                    continue
                distances[new_pos] = min(distances[new_pos], d + 1)

        return distances


def parse(s: str) -> tuple[Maze, list[Vec], Vec, Vec]:
    blocks = [Vec(*map(int, line.split(","))) for line in s.splitlines()]
    grid = Maze(grid=[[Node.SPACE] * WIDTH for _ in range(HEIGHT)])
    start = Vec(0, 0)
    end = Vec(WIDTH - 1, HEIGHT - 1)
    return grid, blocks, start, end


def part_1(s: str) -> int:
    grid, blocks, start, end = parse(s)
    for pos in blocks[:1024]:
        grid[pos] = Node.CORRUPT
    dist = grid.dijkstra(start, end)[end]
    return int(dist)


def part_2(s: str) -> str:
    grid, blocks, start, end = parse(s)
    for block in blocks:
        grid[block] = Node.CORRUPT
    for block in blocks[:1024:-1]:
        # prob should save distances and invalidate paths or use binary search but w/e
        grid[block] = Node.SPACE
        dist = grid.dijkstra(end, start)[start]
        if dist != float("inf"):
            return f"{block.x},{block.y}"


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
