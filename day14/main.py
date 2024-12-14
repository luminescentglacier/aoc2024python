# --- Day 14: Restroom Redoubt ---
import collections
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Self

from util import Vec, Grid

INPUT_FILE = Path(__file__).parent / "input.txt"

GRID_WIDTH = 101
GRID_HEIGHT = 103

X_CENTER = GRID_WIDTH // 2
Y_CENTER = GRID_HEIGHT // 2


def parse(s: str) -> list[tuple[Vec, Vec]]:
    robots = []
    for line in s.splitlines():
        nums = list(map(int, re.findall(r"-?\d+", line)))
        pos = Vec(nums[0], nums[1])
        vel = Vec(nums[2], nums[3])
        robots.append((pos, vel))
    return robots


class Quadrant:
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

    @classmethod
    def from_pos(cls, pos: Vec) -> Self | None:
        offset = offset_from_center(pos)
        if offset.x == 0 or offset.y == 0:
            return None
        match (offset.x > 0, offset.y > 0):
            case True, True:
                return cls.Q1
            case False, True:
                return cls.Q2
            case False, False:
                return cls.Q3
            case True, False:
                return cls.Q4


def offset_from_center(pos: Vec) -> Vec:
    return Vec(pos.x - X_CENTER, Y_CENTER - pos.y)


def part_1(s: str) -> int:
    robots = parse(s)
    seconds = 100
    count = collections.Counter()
    for pos, vel in robots:
        new_pos = pos + Vec(vel.x * seconds, vel.y * seconds)
        new_pos = Vec(new_pos.x % GRID_WIDTH, new_pos.y % GRID_HEIGHT)
        quadrant = Quadrant.from_pos(new_pos)
        if quadrant is not None:
            count[quadrant] += 1
    return math.prod(count.values())


def create_display_buffer(robots: list[Vec]) -> Grid:
    grid = Grid(grid=[[" "] * GRID_WIDTH for _ in range(GRID_HEIGHT)])
    for i, pos in enumerate(robots):
        if isinstance(grid[pos], int):
            grid[pos] += 1
        else:
            grid[pos] = 1
    return grid


def part_2(s: str) -> int:
    # ok this one was frustrating
    # tree picture is only part of the buffer? why?
    robots = parse(s)
    for seconds in range(7700, 7710):
        positions = []
        for pos, vel in robots:
            new_pos = pos + Vec(vel.x * seconds, vel.y * seconds)
            new_pos = Vec(new_pos.x % GRID_WIDTH, new_pos.y % GRID_HEIGHT)
            positions.append(new_pos)
        os.system("clear")
        print(create_display_buffer(positions))
        print(f"Seconds: {seconds}")
        sys.stdout.flush()
        time.sleep(0.3)

        if seconds > 10703:  # pre computed loop
            print("Not Found")
            exit(1)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
