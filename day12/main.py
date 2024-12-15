# --- Day 12: Garden Groups ---
import collections
from collections import defaultdict
from pathlib import Path
from typing import Iterator

from util import Vec, Grid

INPUT_FILE = Path(__file__).parent / "test.txt"

DIRECTIONS = (
    Vec(0, 1),
    Vec(0, -1),
    Vec(1, 0),
    Vec(-1, 0),
)

CORNERS_EDGES = (
    (Vec(x=0, y=1), Vec(x=1, y=0)),
    (Vec(x=0, y=1).rot(90), Vec(x=1, y=0).rot(90)),
    (Vec(x=0, y=1).rot(180), Vec(x=1, y=0).rot(180)),
    (Vec(x=0, y=1).rot(270), Vec(x=1, y=0).rot(270)),
)


class Garden(Grid):
    def __init__(self, grid: list[list]):
        super().__init__(grid)
        self.region_grid = Grid([[None] * len(row) for row in grid])
        self.region_list = []
        self._region_count = 0

        for y in range(len(self.grid)):
            for x in range(len(self.grid)):
                pos = Vec(x, y)
                self._fill_region(pos)

    def _fill_region(self, start: Vec):
        if self.region_of(start) is not None:
            return

        q = collections.deque()
        q.append(start)
        visited = {start}
        while q:
            pos = q.popleft()
            for node in self._region_neighbours(pos):
                if node not in visited:
                    visited.add(node)
                    q.append(node)

        for node in visited:
            self.region_grid[node] = self._region_count
        self.region_list.append((self._region_count, visited))
        self._region_count += 1

    def _region_neighbours(self, pos: Vec) -> Iterator[Vec]:
        for node in neighbours(pos):
            if not self.oob(node) and self[node] == self[pos]:
                yield node

    def region_of(self, pos: Vec) -> int | None:
        return self.region_grid.get(pos, None)


def neighbours(pos: Vec) -> list[Vec]:
    return [pos + d for d in DIRECTIONS]


def neighbours_directions(pos: Vec) -> list[tuple[Vec, Vec]]:
    return [(pos + d, d) for d in DIRECTIONS]


def part_1(s: str) -> int:
    garden = Garden.from_string(s)
    res = 0
    for region_id, region in garden.region_list:
        perimeter = 0
        for node in region:
            for neighbour in neighbours(node):
                if garden.region_of(node) != garden.region_of(neighbour):
                    perimeter += 1
        res += perimeter * len(region)
    return res


def part_2(s: str) -> int:
    garden = Garden.from_string(s)

    res = 0
    for region_id, region_nodes in garden.region_list:
        fences = defaultdict(list)
        for node in region_nodes:
            for neighbour, direction in neighbours_directions(node):
                if garden.region_of(node) != garden.region_of(neighbour):
                    # we need both region node and neighbour node because
                    # inverted corners touch region nodes only once
                    fences[node, True].append(direction)
                    fences[neighbour, False].append(direction.rot(180))

        corners = 0
        for (node, is_region), borders in fences.items():
            for edges in CORNERS_EDGES:
                if not all(edge in borders for edge in edges):
                    continue
                if is_region:
                    corners += 1
                    continue
                opposite = node + edges[0] + edges[1]
                if garden.region_of(opposite) == region_id:
                    corners += 1
        res += corners * len(region_nodes)

    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
