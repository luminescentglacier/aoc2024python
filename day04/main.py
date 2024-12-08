# --- Day 4: Ceres Search ---
from pathlib import Path
from typing import Iterable

from util import flatten

INPUT_FILE = Path(__file__).parent / "input.txt"


def region(field: list | list[list], m: int, n: int) -> Iterable[list[list]]:
    if not isinstance(field[0], list):
        field = [field]
    for i in range(len(field) - m + 1):
        for j in range(len(field[0]) - n + 1):
            matrix = [
                [field[i + i_offset][j + j_offset] for j_offset in range(n)]
                for i_offset in range(m)
            ]
            yield matrix


def _diag_coords(n: int) -> Iterable[list[tuple[int, int]]]:
    for i in range(n):
        d = []
        for j in range(n):
            if i + j >= n:
                break
            d.append((i + j, j))
        yield d
        if i != 0:
            yield [xy[::-1] for xy in d]


def diags(field: list[list]) -> list:
    for d in _diag_coords(len(field)):
        yield [field[i][j] for i, j in d]


class Matrix:
    def __init__(self, s: str | list[list[str]]):
        if isinstance(s, str):
            self.field = [list(line) for line in s.splitlines()]
        else:
            self.field = s
        assert len(self.field) == len(self.field[0])

    def iter_all(self, n: int) -> Iterable[list[str]]:
        yield from map(flatten, self.region(n, 1))
        yield from map(flatten, self.region(1, n))
        for d in self.diags:
            yield from map(flatten, region(d, 1, n))

    def region(self, m: int, n: int) -> Iterable[list[list[str]]]:
        return region(self.field, m, n)

    @property
    def main(self) -> list:
        main = []
        for i in range(len(self.field)):
            main.append(self.field[i][i])
        return main

    @property
    def anti(self) -> list:
        anti = []
        for i in range(len(self.field)):
            anti.append(self.field[i][len(self.field) - i - 1])
        return anti

    @property
    def diags(self) -> Iterable[list[str]]:
        main_diags = diags(self.field)
        anti_diags = diags([line[::-1] for line in self.field])
        for a, b in zip(main_diags, anti_diags):
            yield a
            yield b


def part_1(s: str) -> int:
    matrix = Matrix(s)
    res = 0
    xmas = "XMAS"
    for word in matrix.iter_all(len(xmas)):
        word = "".join(word)
        if word == xmas or word[::-1] == xmas:
            res += 1
    return res


def part_2(s: str) -> int:
    search = Matrix(s)
    res = 0
    word = "MAS"
    for matrix in search.region(3, 3):
        matrix = Matrix(matrix)
        main = "".join(matrix.main)
        anti = "".join(matrix.anti)
        if (main == word or main[::-1] == word) and (
            anti == word or anti[::-1] == word
        ):
            res += 1
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
