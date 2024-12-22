# --- Day 21: Keypad Conundrum ---
# this is a mess
import collections
import functools
import itertools
from collections import defaultdict
from copy import deepcopy
from pathlib import Path
from typing import Self

from util import Grid, Vec

INPUT_FILE = Path(__file__).parent / "input.txt"

DIRECTIONS = (
    Vec(0, 1),
    Vec(0, -1),
    Vec(1, 0),
    Vec(-1, 0),
)
DIRECTIONS_MAPPING = {Vec(0, 1): "v", Vec(0, -1): "^", Vec(1, 0): ">", Vec(-1, 0): "<"}


class Keypad(Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.mapping = defaultdict(dict)
        for pos, button in self.items():
            if button is not None:
                self._calc_distance(pos)

    def items(self):
        for pos, button in super().items():
            if button is not None:
                yield pos, button

    def _calc_distance(self, start: Vec) -> None:
        distances = {
            Vec(x, y): float("inf")
            for y in range(self.height)
            for x in range(self.width)
        }
        distances[start] = 0.0
        unvisited = set(distances.keys())
        prev = defaultdict(list)

        while unvisited:
            pos, distance = min(
                ((k, v) for k, v in distances.items() if k in unvisited),
                key=lambda x: x[1],
            )
            unvisited.remove(pos)

            for direction in DIRECTIONS:
                new_pos = pos + direction
                if new_pos not in unvisited or self[new_pos] is None:
                    continue

                old_distance = distances[new_pos]
                new_distance = distance + 1
                if new_distance < old_distance:
                    distances[new_pos] = new_distance
                    prev[new_pos] = [pos]
                elif new_distance == old_distance:
                    prev[new_pos].append(pos)

        for pos, button in self.items():
            if button is None:
                continue
            paths = list(self._calc_paths(pos, start, prev))
            self.mapping[self[start]][button] = paths

    def _calc_paths(
        self, start: Vec, end: Vec, prev: dict[Vec, list[Vec]]
    ) -> list[list[Vec]]:
        q = collections.deque([[start]])
        while q:
            path = q.pop()
            pos = path[-1]
            if pos == end and len(path) > 1:
                yield list(a - b for a, b in itertools.pairwise(path))[::-1]
            for neighbour in prev[pos]:
                new_path = deepcopy(path)
                new_path.append(neighbour)
                q.append(new_path)

    def get_sequences_raw(self, start: str, end: str) -> list[list[Vec]]:
        return self.mapping[start][end]

    def get_sequences(self, start: str, end: str) -> list[list[str]]:
        if start == end:
            return [["A"]]
        # convert vec positions into directional inputs
        return [
            [*(DIRECTIONS_MAPPING[d] for d in path), "A"]
            for path in self.get_sequences_raw(start, end)
        ]

    def get_sequences_best(self, start: str, end: str) -> list[list[str]]:
        # trim zigzag paths because they require more inputs from previous keypad
        score = lambda seq: sum(a != b for a, b in itertools.pairwise(seq))
        weighted = [(score(seq), seq) for seq in self.get_sequences(start, end)]
        best = min(score for score, seq in weighted)
        return [seq for score, seq in weighted if score == best]


NUMERIC_KEYPAD = Keypad(
    [
        ["7", "8", "9"],
        ["4", "5", "6"],
        ["1", "2", "3"],
        [None, "0", "A"],
    ],
)

DIRECTIONAL_KEYPAD = Keypad(
    [
        [None, "^", "A"],
        ["<", "v", ">"],
    ]
)


class KeypadStack:
    def __init__(self, keypads: list[Keypad]):
        self.keypad = keypads[0]
        self.next_stack = KeypadStack(keypads[1:]) if len(keypads) > 1 else None

    @classmethod
    def from_count(cls, n: int) -> Self:
        return cls([NUMERIC_KEYPAD, *[DIRECTIONAL_KEYPAD for _ in range(n)]])

    @functools.cache
    def best_sequence(self, start: str, end: str) -> int:
        if self.next_stack is None:
            return len(self.keypad.get_sequences_best(start, end)[0])
        sequences = self.keypad.get_sequences_best(start, end)
        return min(self.next_stack.resolve(seq) for seq in sequences)

    def resolve(self, seq: list[str]) -> int:
        # keypads always start and end on "A"
        seq = ["A", *seq]
        assert seq[-1] == "A"
        return sum(self.best_sequence(a, b) for a, b in itertools.pairwise(seq))


def part_1(s: str) -> int:
    stack = KeypadStack.from_count(2)
    return sum(stack.resolve(line) * int(line[:-1]) for line in s.splitlines())


def part_2(s: str) -> int:
    stack = KeypadStack.from_count(25)
    return sum(stack.resolve(line) * int(line[:-1]) for line in s.splitlines())


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
