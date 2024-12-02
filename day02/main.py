# --- Day 2: Red-Nosed Reports ---

from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def part_1(s: str) -> int:
    reports = map(str.split, s.splitlines())
    res = 0
    for r in reports:
        diff = [int(a) - int(b) for a, b in zip(r, r[1:])]
        values_ok = all(1 <= abs(level) <= 3 for level in diff)
        all_positive = all(level > 0 for level in diff)
        all_negative = all(level < 0 for level in diff)
        if values_ok and (all_positive or all_negative):
            res += 1
    return res


increasing = lambda x: x > 0
decreasing = lambda x: x < 0
normal = lambda x: 1 <= abs(x) <= 3


def is_ok(report):
    diff = [int(a) - int(b) for a, b in zip(report, report[1:])]
    if sum(map(increasing, diff)) > sum(map(decreasing, diff)):
        filt = lambda x: increasing(x) and normal(x)
    else:
        filt = lambda x: decreasing(x) and normal(x)
    values = list(map(filt, diff))

    distance = sum(not x for x in values)
    if distance == 0:
        return True, set()
    elif 1 <= distance <= 2:
        # distance == 1 case:
        # [1, 2, 7] -> [True, False]: [1, 2] -> [True]
        # distance == 2 case:
        # [1, 7, 2] -> [False, False]: [1, 2] -> [True]
        candidates = set()
        for i, v in enumerate(values):
            if v:
                continue
            candidates.add(i)
            if i + 1 < len(report):
                candidates.add(i + 1)
        return False, candidates
    else:
        return False, set()


def part_2(s: str) -> int:
    reports = map(str.split, s.splitlines())
    res = 0
    for r in reports:
        ok, candidates = is_ok(r)
        if ok:
            res += 1
            continue

        for i in candidates:
            r_copy = r.copy()
            r_copy.pop(i)
            ok, _ = is_ok(r_copy)
            if ok:
                res += 1
                break
    return res


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
