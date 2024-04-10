import io
import pytest
from src.reader import Reader


def test_read_from_file():
    with open("test_files/reader_test.txt", "r") as file_handle:
        reader = Reader(file_handle)

        characters, positions = get_characters_and_positions(reader)
        assert characters == ['1', '0', '+', '1', '1', '=', '2', '1', '\n', 'EOF']
        assert positions == [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (2, 0)]


def test_read_from_file_empty():
    with open("test_files/reader_test_empty.txt", "r") as file_handle:
        reader = Reader(file_handle)

        characters, positions = get_characters_and_positions(reader)
        assert characters == ["EOF"]
        assert positions == [(1, 0)]


def test_read_from_string():
    src_string = "10+11=21\nkacper\nmaja"
    reader = Reader(io.StringIO(src_string))

    characters, positions = get_characters_and_positions(reader)
    assert characters == ['1', '0', '+', '1', '1', '=', '2', '1', '\n', 'k', 'a', 'c', 'p', 'e', 'r', '\n', 'm', 'a',
                          'j', 'a', 'EOF']
    assert positions == [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (1, 0), (1, 1), (1, 2),
                         (1, 3), (1, 4), (1, 5), (1, 6), (2, 0), (2, 1), (2, 2), (2, 3), (3, 0)]


def test_read_from_string_empty():
    src_string = ""
    reader = Reader(io.StringIO(src_string))

    characters, positions = get_characters_and_positions(reader)
    assert characters == ["EOF"]
    assert positions == [(1, 0)]


def get_characters_and_positions(src):
    characters, positions = [], []

    next_character = src.get_current_char()
    characters.append(next_character)
    positions.append(src.get_current_position())

    src.next()

    while next_character != 'EOF':
        next_character = src.get_current_char()
        characters.append(next_character)
        positions.append(src.get_current_position())

        src.next()

    return characters, positions
