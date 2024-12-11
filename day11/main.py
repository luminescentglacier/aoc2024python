# --- Day 11: Plutonian Pebbles ---
import collections
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def stones_at(s: str, steps: int) -> int:
    # Once number digit count is even, it breaks down to single digits after
    # log2(len(str(num))) steps. Therefore every single input number will enter the loop
    # at some point. The loop for all 10 digits is quite small.
    # 0 -> 1
    # 1 -> 2024 -> 20 24 -> 2 0 2 4
    # ...
    # 9 -> 18216 -> 36869184 -> 3686 9184 -> 36 86 91 84 -> 3 6 8 6 9 1 8 4
    stones = collections.Counter(map(int, s.split()))
    for i in range(steps):
        new_stones = collections.Counter()
        for num, count in stones.items():
            if count == 0:
                continue
            if num == 0:
                new_stones[1] += count
            elif len(num_str := str(num)) % 2 == 0:
                left = int(num_str[: len(num_str) // 2])
                right = int(num_str[len(num_str) // 2 :])
                new_stones[left] += count
                new_stones[right] += count
            else:
                new_stones[num * 2024] += count
        stones = new_stones
    return sum(stones.values())


def part_1(s: str) -> int:
    return stones_at(s, 25)


def part_2(s: str) -> int:
    return stones_at(s, 75)


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
