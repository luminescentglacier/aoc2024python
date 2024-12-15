# --- Day 15: Warehouse Woes ---
import os
import sys
import tty
from collections import deque
from enum import Enum
from pathlib import Path
from typing import Iterator, Self

from util import Vec, Grid

INPUT_FILE = Path(__file__).parent / "input.txt"

GAME = os.environ.get("GAME", False)
GAME_CONTROLS = {"h": "<", "j": "v", "k": "^", "l": ">"}

if GAME:
    tty.setcbreak(sys.stdin.fileno())


class Node(str, Enum):
    WALL = "#"
    ROBOT = "@"
    BOX = "O"
    BOX_L = "["
    BOX_R = "]"
    SPACE = "."

    def __str__(self):
        return self.value


class Action(str, Enum):
    UP = "^"
    DOWN = "v"
    LEFT = "<"
    RIGHT = ">"

    def __str__(self):
        return self.value

    def vec(self) -> Vec:
        match self:
            case Action.UP:
                return Vec(x=0, y=-1)
            case Action.DOWN:
                return Vec(x=0, y=1)
            case Action.LEFT:
                return Vec(x=-1, y=0)
            case Action.RIGHT:
                return Vec(x=1, y=0)


def parse(s: str):
    grid, moves = s.split("\n\n")
    moves = moves.replace("\n", "")
    moves = list(map(Action, moves))
    grid = Grid([list(map(Node, row)) for row in grid.splitlines()])
    return grid, moves


def part_1(s: str) -> int:
    grid, moves = parse(s)
    robot = grid.find(Node.ROBOT)

    for i, move in enumerate(moves):
        boxes = [robot]
        next_pos = robot
        while True:
            next_pos += move.vec()
            if grid.oob(next_pos):
                next_pos = None
                break
            if grid[next_pos] != Node.BOX:
                break
            boxes.append(next_pos)

        if next_pos is None or grid[next_pos] != Node.SPACE:
            continue

        for box in reversed(boxes):
            grid[box + move.vec()] = grid[box]
            grid[box] = Node.SPACE
        robot += move.vec()

    res = 0
    for box in grid.find_iter(Node.BOX):
        res += box.y * 100 + box.x
    return res


class Warehouse(Grid):
    @classmethod
    def from_string(cls, s: str) -> Self:
        rows = []
        for line in s.splitlines():
            row = []
            for ch in line:
                node = Node(ch)
                match node:
                    case Node.WALL:
                        row.extend((Node.WALL, Node.WALL))
                    case Node.ROBOT:
                        row.extend((Node.ROBOT, Node.SPACE))
                    case Node.BOX:
                        row.extend((Node.BOX_L, Node.BOX_R))
                    case Node.SPACE:
                        row.extend((Node.SPACE, Node.SPACE))
            rows.append(row)
        return cls(grid=rows)

    def bfs_iter(self, start: Vec, move: Vec) -> Iterator[Vec]:
        if self[start] != Node.BOX_L and self[start] != Node.BOX_R:
            return

        q = deque()
        q.append(start)
        visited = {start}
        while q:
            pos = q.popleft()
            yield pos
            for node in self.neighbours(pos, move):
                if node not in visited:
                    visited.add(node)
                    q.append(node)

    def neighbours(self, pos: Vec, move: Vec) -> Iterator[Vec]:
        match self[pos]:
            case Node.BOX_L:
                yield pos + Vec(x=1, y=0)
            case Node.BOX_R:
                yield pos + Vec(x=-1, y=0)

        next_pos = pos + move
        match self[next_pos]:
            case Node.BOX_L | Node.BOX_R:
                yield next_pos
            case Node.WALL:
                raise ValueError("Move blocked by the wall")


def parse_2(s: str):
    grid, moves = s.split("\n\n")
    moves = moves.replace("\n", "")
    moves = list(map(Action, moves))
    return Warehouse.from_string(grid), moves


def part_2(s: str) -> int:
    grid, moves = parse_2(s)
    robot = grid.find(Node.ROBOT)

    for i, move in enumerate(moves):
        if GAME:
            os.system("clear")
            print(grid)
            print("[h/j/k/l]: ", end="")
            sys.stdout.flush()
            while (ch := sys.stdin.read(1)) not in GAME_CONTROLS:
                continue
            move = Action(GAME_CONTROLS[ch])

        next_pos = robot + move.vec()
        try:
            boxes = list(grid.bfs_iter(next_pos, move.vec()))
        except ValueError:
            # some of the boxes touch the wall
            continue

        if not boxes and grid[next_pos] != Node.SPACE:
            # robot touches the wall
            continue

        boxes.insert(0, robot)
        for box in reversed(boxes):
            grid[box + move.vec()] = grid[box]
            grid[box] = Node.SPACE
        robot += move.vec()

    res = 0
    for box in grid.find_iter(Node.BOX_L):
        res += box.y * 100 + box.x
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
