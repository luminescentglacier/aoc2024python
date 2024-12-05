# --- Day 5: Print Queue ---
from collections import defaultdict
from copy import deepcopy
from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def parse(s: str) -> tuple[dict[int, set[int]], list[list[int]]]:
    rules_lines, update_lines = s.split("\n\n")

    rules = defaultdict(set)
    for line in rules_lines.splitlines():
        before, after = line.split("|")
        rules[int(before)].add(int(after))

    updates = [list(map(int, line.split(","))) for line in update_lines.splitlines()]
    for update in updates:
        assert len(update) == len(set(update))

    return rules, updates


def is_valid(update: list[int], rules: dict[int, set[int]]) -> bool:
    for before, after in rules.items():
        try:
            index = update.index(before)
        except ValueError:
            continue
        pages_before = set(update[:index])
        if pages_before.intersection(after):
            return False
    return True


def fix_order(update: list[int], rules: dict[int, set[int]]) -> list[int]:
    update = deepcopy(update)
    for before, after in rules.items():
        try:
            error_index = update.index(before)
        except ValueError:
            continue
        pages_before = set(update[:error_index])
        if errors := pages_before.intersection(after):
            earliest_index = min(update.index(e) for e in errors)
            update.pop(error_index)
            update.insert(earliest_index, before)
    assert is_valid(update, rules)
    return update


def part_1(s: str) -> int:
    rules, updates = parse(s)
    res = 0
    for update in updates:
        if is_valid(update, rules):
            middle = update[(len(update) // 2)]
            res += middle
    return res


def part_2(s: str) -> int:
    rules, updates = parse(s)
    res = 0
    invalid_updates = [u for u in updates if not is_valid(u, rules)]
    for update in invalid_updates:
        update = fix_order(update, rules)
        middle = update[(len(update) // 2)]
        res += middle
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
