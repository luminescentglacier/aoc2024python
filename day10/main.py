# --- Day 10: Hoof It ---
from collections import deque
from pathlib import Path
from typing import Iterator, Self

from util import Grid, Vec

INPUT_FILE = Path(__file__).parent / "input.txt"


class TopologyMap(Grid):
    @classmethod
    def from_string(cls, s: str) -> Self:
        tm = super().from_string(s)
        for i, row in enumerate(tm.grid):
            tm.grid[i] = [int(v) if v != "." else -1 for v in row]
        return tm

    def bfs_iter(self, start: Vec, adj_func) -> Iterator[Vec]:
        q = deque()
        q.append(start)
        visited = {start}
        while q:
            pos = q.popleft()
            yield pos
            for node in adj_func(self, pos):
                if node not in visited:
                    visited.add(node)
                    q.append(node)

    def bfs_iter_no_visited(self, start: Vec, adj_func) -> Iterator[Vec]:
        q = deque()
        q.append(start)
        while q:
            pos = q.popleft()
            yield pos
            for node in adj_func(self, pos):
                q.append(node)

    def __str__(self) -> str:
        s = []
        for row in self:
            s.append("".join(str(v) if v != -1 else "." for v in row))
        return "\n".join(s)


def good_adj(grid: TopologyMap, pos: Vec) -> Iterator[Vec]:
    adj = (pos + Vec(0, 1), pos + Vec(0, -1), pos + Vec(1, 0), pos + Vec(-1, 0))
    for node in adj:
        if grid.oob(node):
            continue
        delta = grid[node] - grid[pos]
        if delta == 1:
            yield node


def part_1(s: str) -> int:
    grid = TopologyMap.from_string(s)

    res = 0
    for start in grid.find_iter(0):
        score = sum(1 for pos in grid.bfs_iter(start, good_adj) if grid[pos] == 9)
        res += score
    return res


def part_2(s: str) -> int:
    grid = TopologyMap.from_string(s)

    res = 0
    for start in grid.find_iter(0):
        score = sum(
            1 for pos in grid.bfs_iter_no_visited(start, good_adj) if grid[pos] == 9
        )
        res += score
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
