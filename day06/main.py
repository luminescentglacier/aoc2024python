# --- Day 6: Guard Gallivant ---
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from util import Grid, Vec

import tqdm

INPUT_FILE = Path(__file__).parent / "input.txt"


def traverse(grid: Grid, pos: Vec, direction: Vec):
    visited = defaultdict(set)
    visited[pos].add(direction)
    while True:
        next_pos = pos + direction
        if grid.oob(next_pos):
            break
        elif grid[next_pos] == "#":
            direction = direction.rot(90)
            continue

        loop = next_pos in visited and direction in visited[next_pos]
        if loop:
            return visited, False
        pos = next_pos
        visited[pos].add(direction)
    return visited, True


def part_1(s: str) -> int:
    grid = Grid.from_string(s)
    pos = grid.find("^")
    direction = Vec(y=-1, x=0)
    visited, _ = traverse(grid, pos, direction)
    return len(visited)


def part_2(s: str) -> int:
    grid = Grid.from_string(s)
    orig_pos = grid.find("^")
    orig_direction = Vec(y=-1, x=0)
    visited, _ = traverse(grid, orig_pos, orig_direction)

    res = 0
    for pos, directions in tqdm.tqdm(visited.items()):
        for direction in directions:
            # TODO: keep track of time when pos was entered from direction
            # TODO: check if placing rock at step N will break the timeline
            # TODO: (guard visited this square before)
            # TODO: otherwise try to travers as normal; if at some point pos and
            # TODO: direction line up with previous path, then we entered the loop
            # TODO: loop itself can be pretty complicated
            # TODO: this will still require a lot of compute
            grid_c = deepcopy(grid)
            grid_c[pos] = "#"
            _, has_exit = traverse(grid_c, orig_pos, orig_direction)
            if not has_exit:
                res += 1
                break

    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
