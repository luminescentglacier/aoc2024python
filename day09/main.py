# --- Day 9: Disk Fragmenter ---

from pathlib import Path

INPUT_FILE = Path(__file__).parent / "input.txt"


def part_1(s: str) -> int:
    disk = []
    file_id = 0
    for i, val in enumerate(s.strip()):
        is_file = i % 2 == 0
        if is_file:
            disk.extend([file_id] * int(val))
            file_id += 1
        else:
            disk.extend([None] * int(val))

    for i in range(len(disk)):
        if i >= len(disk):
            break
        while disk[i] is None:
            try:
                disk[i] = disk.pop(-1)
            except IndexError:
                break

    checksum = sum(i * val for i, val in enumerate(disk))
    return checksum


def part_2(s: str) -> int:
    files = []
    free = []
    file_id = 0
    pos = 0
    for i, val in enumerate(s.strip()):
        is_file = i % 2 == 0
        if is_file:
            files.append((pos, int(val), file_id))
            file_id += 1
        else:
            free.append((pos, int(val)))
        pos += int(val)

    defrag_files = []
    for file_pos, file_size, file_id in files[::-1]:
        for i, (free_pos, free_size) in enumerate(free):
            if free_pos > file_pos:
                defrag_files.append((file_id, file_size, file_pos))
                break
            if free_size < file_size:
                continue

            defrag_files.append((file_id, file_size, free_pos))
            if free_size == file_size:
                free.pop(i)
            else:
                free[i] = (free_pos + file_size, free_size - file_size)
            break

    checksum = sum(
        file_id * int(arithmetic_series(file_pos, file_pos + file_size - 1, file_size))
        for file_id, file_size, file_pos in defrag_files
    )
    return checksum


def arithmetic_series(start: int, end: int, steps: int) -> float:
    return (steps * (start + end)) / 2


if __name__ == "__main__":
    s = INPUT_FILE.read_text()
    print(f"Part 1: {part_1(s)}")
    print(f"Part 2: {part_2(s)}")
