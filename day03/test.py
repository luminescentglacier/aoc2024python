from pathlib import Path

import pytest

from .main import part_1, part_2

TEST_INPUT_FILE = Path(__file__).parent / "test.txt"
TEST_PART2_INPUT_FILE = Path(__file__).parent / "test2.txt"


@pytest.fixture
def puzzle_input():
    return TEST_INPUT_FILE.read_text()


@pytest.fixture
def puzzle_input_part_2():
    return TEST_PART2_INPUT_FILE.read_text()


def test_part_1(puzzle_input):
    assert part_1(puzzle_input) == 161


def test_part_2(puzzle_input_part_2):
    assert part_2(puzzle_input_part_2) == 48
