from pathlib import Path

import pytest

from .main import part_1, part_2

TEST_INPUT_FILE = Path(__file__).parent / "test.txt"


@pytest.fixture
def puzzle_test():
    assert TEST_INPUT_FILE.exists()
    return TEST_INPUT_FILE.read_text()


def test_part_1(puzzle_test):
    assert part_1(puzzle_test) == 11


def test_part_2(puzzle_test):
    assert part_2(puzzle_test) == 31
