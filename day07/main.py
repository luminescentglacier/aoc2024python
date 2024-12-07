# --- Day 7: Bridge Repair ---
import itertools
from operator import mul, add
from pathlib import Path
from typing import Callable

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> list[tuple[int, list[int]]]:
    vals = []
    for line in s.splitlines():
        result, nums = line.split(": ")
        nums = [int(num) for num in nums.split()]
        vals.append((int(result), nums))
    return vals


def is_valid(
    result: int, nums: list[int], operators: list[Callable[[int, int], int]]
) -> bool:
    # TODO: prob should keep partial result to reduce compute, this is a tree problem kinda
    for ops in itertools.product(operators, repeat=len(nums) - 1):
        a = nums[0]
        for op, b in zip(ops, nums[1:]):
            a = op(a, b)
        if a == result:
            return True
    return False


def part_1(s: str) -> int:
    vals = parse(s)
    ops = [mul, add]
    res = sum(result for result, nums in vals if is_valid(result, nums, ops))
    return res


def concat(a: int, b: int) -> int:
    return int(f"{a}{b}")


def part_2(s: str) -> int:
    vals = parse(s)
    ops = [mul, add, concat]
    res = sum(result for result, nums in vals if is_valid(result, nums, ops))
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
