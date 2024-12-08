import math
from dataclasses import dataclass
from itertools import chain
from typing import Self, Any, Iterator


@dataclass(frozen=True)
class Vec:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Vec(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Self) -> Self:
        return Vec(self.x - other.x, self.y - other.y)

    def __neg__(self) -> Self:
        return Vec(-self.x, -self.y)

    def rot(self, degrees: int) -> Self:
        # counterclockwise
        return Vec(
            x=int(
                math.cos(math.radians(degrees)) * self.x
                - math.sin(math.radians(degrees)) * self.y
            ),
            y=int(
                math.sin(math.radians(degrees)) * self.x
                + math.cos(math.radians(degrees)) * self.y
            ),
        )


class Grid:
    def __init__(self, grid: list[list]):
        self.grid = grid

    @classmethod
    def from_string(cls, s: str) -> Self:
        return Grid([list(line) for line in s.splitlines()])

    def get(self, item: Vec, default: Any = None) -> Any:
        try:
            return self.grid[item.y][item.x]
        except IndexError:
            return default

    def find(self, value: Any) -> Vec | None:
        for y, row in enumerate(self):
            try:
                x = row.index(value)
            except ValueError:
                continue
            return Vec(x, y)
        return None

    def find_iter(self, value: Any) -> Iterator[Vec]:
        for y, row in enumerate(self):
            for x, val in enumerate(row):
                if val == value:
                    yield Vec(x, y)

    def oob(self, pos: Vec) -> bool:
        return not (0 <= pos.x < len(self.grid) and 0 <= pos.y < len(self.grid))

    def __getitem__(self, item: Vec) -> Any:
        return self.grid[item.y][item.x]

    def __setitem__(self, item: Vec, value: Any) -> None:
        self.grid[item.y][item.x] = value

    def __repr__(self):
        return f"Grid(rows={len(self.grid)}, cols={len(self.grid[0])})"

    def __str__(self) -> str:
        s = []
        for row in self:
            s.append("".join(row))
        return "\n".join(s)

    def __iter__(self) -> Iterator[list]:
        yield from self.grid

    def __len__(self) -> int:
        return len(self.grid)


def flatten(v):
    return list(chain(*v))
