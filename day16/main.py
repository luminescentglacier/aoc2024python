# --- Day 16: Reindeer Maze ---
import collections
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import Self

import tqdm

from util import Grid, Vec

INPUT_FILE = Path(__file__).parent / "input.txt"

DIRECTIONS = (
    Vec(0, 1),
    Vec(0, -1),
    Vec(1, 0),
    Vec(-1, 0),
)


class Node(str, Enum):
    WALL = "#"
    START = "S"
    END = "E"
    SPACE = "."

    def __str__(self):
        return self.value


class Maze(Grid):
    @classmethod
    def from_string(cls, s: str) -> Self:
        return cls([list(map(Node, line)) for line in s.splitlines()])

    def dijkstra(self, start: Vec, end: Vec):
        distances = {
            (pos, direction): float("inf")
            for y in range(self.height)
            for x in range(self.width)
            for direction in DIRECTIONS
            if self[pos := Vec(x, y)] != Node.WALL
        }
        distances[(start, Vec(-1, 0))] = 0.0
        unvisited = set(distances.keys())
        prev = defaultdict(set)

        with tqdm.tqdm(total=len(unvisited)) as pbar:
            while unvisited:
                (pos, direction), distance = min(
                    ((k, v) for k, v in distances.items() if k in unvisited),
                    key=lambda x: x[1],
                )
                unvisited.remove((pos, direction))
                pbar.update(1)

                neighbours = [
                    (pos + direction, direction, 1),
                    (pos + direction.rot(90), direction.rot(90), 1000 + 1),
                    (pos + direction.rot(180), direction.rot(180), 2 * 1000 + 1),
                    (pos + direction.rot(270), direction.rot(270), 1000 + 1),
                ]

                for new_pos, new_direction, cost in neighbours:
                    if (new_pos, new_direction) not in unvisited:
                        continue
                    if self.get(new_pos, Node.WALL) == Node.WALL:
                        continue
                    new_distance = distance + cost
                    old_distance = distances[(new_pos, new_direction)]
                    if new_distance < old_distance:
                        distances[(new_pos, new_direction)] = new_distance
                        prev[(new_pos, new_direction)] = {(pos, direction)}
                    elif new_distance == old_distance:
                        prev[(new_pos, new_direction)].add((pos, direction))

        best_score = int(min(v for (pos, d), v in distances.items() if pos == end))
        best_spots = set()
        for i in range(4):
            direction = Vec(-1, 0).rot(90 * i)
            if distances[(end, direction)] != best_score:
                continue
            for path in self.reconstruct_paths(start, end, direction, prev):
                best_spots.update(pos for pos, _ in path)

        return best_score, len(best_spots)

    def reconstruct_paths(
        self,
        start: Vec,
        end_pos: Vec,
        end_direction,
        prev: dict[(Vec, Vec), set[(Vec, Vec)]],
    ):
        q = collections.deque([[(end_pos, end_direction)]])
        while q:
            path = q.pop()
            pos, direction = path[-1]
            if pos == start and direction == Vec(-1, 0):
                yield path
            for neighbour in prev[(pos, direction)]:
                new_path = deepcopy(path)
                new_path.append(neighbour)
                q.append(new_path)


def main(s: str):
    maze = Maze.from_string(s)
    start, end = maze.find(Node.START), maze.find(Node.END)
    best_score, best_spots = maze.dijkstra(start, end)
    print(f"Part 1: {best_score}")
    print(f"Part 2: {best_spots}")


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    main(s)
