# --- Day 22: Monkey Market ---
import collections
import itertools
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def sliding_window(iterable, n):
    "Collect data into overlapping fixed-length chunks or blocks."
    # sliding_window('ABCDEFG', 4) → ABCD BCDE CDEF DEFG
    iterator = iter(iterable)
    window = collections.deque(itertools.islice(iterator, n - 1), maxlen=n)
    for x in iterator:
        window.append(x)
        yield tuple(window)


class RNGGenerator:
    def __init__(self, seed: int) -> None:
        self.seed = seed
        self.cur = seed

    def __next__(self) -> tuple[int, int, int]:
        old_price = self.price()
        # always 24 bits; probably some clever bit mapping via xor shifting
        self.cur = ((self.cur << 6) ^ self.cur) & 0b1111_1111_1111_1111_1111_1111
        self.cur = (self.cur >> 5) ^ self.cur
        self.cur = ((self.cur << 11) ^ self.cur) & 0b1111_1111_1111_1111_1111_1111
        new_price = self.price()
        return self.cur, new_price, new_price - old_price

    def __iter__(self) -> tuple[int, int, int]:
        while True:
            yield next(self)

    def price(self) -> int:
        return int(str(self.cur)[-1])

    def nth(self, n: int) -> int:
        for i in range(n):
            next(self)
        return self.cur


def part_1(s: str) -> int:
    res = 0
    for seed in map(int, s.splitlines()):
        res += RNGGenerator(seed).nth(2000)
    return res


def part_2(s: str) -> int:
    sequences_scores = collections.Counter()
    for seed in map(int, s.splitlines()):
        gen = RNGGenerator(seed)
        seen = set()
        for seq in sliding_window(itertools.islice(gen, 2000), n=4):
            deltas = tuple(el[2] for el in seq)
            if deltas in seen:
                continue
            score = seq[-1][1]
            sequences_scores[deltas] += score
            seen.add(deltas)
    return sequences_scores.most_common(1)[0][1]


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
