import io
import pytest

from src.exceptions.lexer_exception import (
    LexerException,
    CommentTooLongException,
    StringTooLongException,
    UnclosedStringException,
    IdentifierTooLongException,
    NumberException
)
from src.reader import Reader
from src.lexer.lexer import Lexer, get_tokens


def get_all_tokens(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return get_tokens(lexer)


def test_too_long_comment():
    with pytest.raises(CommentTooLongException) as e:
        tokens = get_all_tokens("#Za dlugi komentarz" * 10_000 + "\n")


# def test_too_long_string():
#     with pytest.raises(StringTooLongException) as e:
#         tokens = get_all_tokens('"Mam na imie Kacper"')


def test_too_long_identifier():
    with pytest.raises(IdentifierTooLongException) as e:
        tokens = get_all_tokens("ID1" * 100)


def test_too_big_int():
    with pytest.raises(NumberException) as e:
        tokens = get_all_tokens("11000000")


def test_too_big_float():
    with pytest.raises(NumberException) as e:
        tokens = get_all_tokens("10000000.1")


def test_unclosed_string_EOF():
    with pytest.raises(UnclosedStringException) as e:
        tokens = get_all_tokens('"Hello World')


def test_unclosed_string_newline():
    with pytest.raises(UnclosedStringException) as e:
        tokens = get_all_tokens('"Hello World\n')
