import io
import pytest

from src.reader import Reader
from src.lexer.lexer import Lexer, get_tokens
from src.token.token import Token
from src.token.token_types import TokenType


def get_all_tokens(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return get_tokens(lexer)


def test_string_with_comment():
    tokens = get_all_tokens("#111\njakisid")
    assert [token.type for token in tokens] == [TokenType.COMMENT, TokenType.ID, TokenType.EOF]
    assert [token.position for token in tokens] == [(1, 1), (2, 1), (3, 0)]


def test_ids_with_space():
    text = "jakis_id jakis_id2 jakis_id3"
    tokens = get_all_tokens(text)
    assert [token.type for token in tokens] == [TokenType.ID, TokenType.ID, TokenType.ID, TokenType.EOF]
    assert [token.value for token in tokens] == ['jakis_id', 'jakis_id2', 'jakis_id3', '']
    assert [token.position for token in tokens] ==[(1, 1), (1, 10), (1, 20), (2, 0)]


def test_ints_with_space():
    text = "10 20 30"
    tokens = get_all_tokens(text)
    assert [token.type for token in tokens] == [TokenType.INT_VALUE, TokenType.INT_VALUE, TokenType.INT_VALUE, TokenType.EOF]
    assert [token.value for token in tokens] == [10, 20, 30, '']
    assert [token.position for token in tokens] == [(1, 1), (1, 4), (1, 7), (2, 0)]


def test_integers_with_whitespaces():
    tokens = get_all_tokens("1 \n2\n3")
    assert [token.position for token in tokens] == [(1, 1), (2, 1), (3, 1), (4, 0)]
    assert [token.type for token in tokens] == [TokenType.INT_VALUE, TokenType.INT_VALUE, TokenType.INT_VALUE, TokenType.EOF]


def test_pair():
    str = "Pair<int, string>\n"
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [
        TokenType.PAIR, TokenType.LESS_SIGN, TokenType.INT_KEYWORD,
        TokenType.COMMA, TokenType.STRING_KEYWORD, TokenType.GREATER_SIGN, TokenType.EOF]


def test_dict():
    str = "Dict<int, string>\n"
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [
        TokenType.DICT, TokenType.LESS_SIGN, TokenType.INT_KEYWORD,
        TokenType.COMMA, TokenType.STRING_KEYWORD, TokenType.GREATER_SIGN, TokenType.EOF]
    assert [token.position for token in tokens] == [(1, 1), (1, 5), (1, 6), (1, 9), (1, 11), (1, 17), (3, 0)]


def test_list():
    str = "List<int>\n"
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [
        TokenType.LIST, TokenType.LESS_SIGN, TokenType.INT_KEYWORD,
        TokenType.GREATER_SIGN, TokenType.EOF]
    assert [token.position for token in tokens] == [(1, 1), (1, 5), (1, 6), (1, 9), (3, 0)]


def test_add_operation_with_space():
    str = ("10 + 20 = 30")
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [TokenType.INT_VALUE, TokenType.ADD_SIGN,
                                                TokenType.INT_VALUE, TokenType.ASSIGN,
                                                TokenType.INT_VALUE, TokenType.EOF]
    assert [token.value for token in tokens] == [10, '', 20, '', 30, '']
    assert [token.position for token in tokens] == [(1, 1), (1, 4), (1, 6), (1, 9), (1, 11), (2, 0)]


def test_int_minus():
    str = ("-3")
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [TokenType.SUB_SIGN, TokenType.INT_VALUE, TokenType.EOF]
    assert [token.value for token in tokens] == ['', 3, '']
    assert [token.position for token in tokens] == [(1, 1), (1, 2), (2, 0)]


def test_float_minus():
    str = ("-3.14")
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [TokenType.SUB_SIGN, TokenType.FLOAT_VALUE, TokenType.EOF]
    assert [token.value for token in tokens] == ['', 3.14, '']
    assert [token.position for token in tokens] == [(1, 1), (1, 2), (2, 0)]


def test_declaration():
    str = "int a;"
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [TokenType.INT_KEYWORD, TokenType.ID, TokenType.SEMICOLON, TokenType.EOF]
    assert [token.value for token in tokens] == ['int', 'a', '', '']
    assert [token.position for token in tokens] == [(1, 1), (1, 5), (1, 6), (2, 0)]


def test_declaration_with_assignment():
    str = "int a = 10;"
    tokens = get_all_tokens(str)
    assert [token.type for token in tokens] == [TokenType.INT_KEYWORD, TokenType.ID,
                                                TokenType.ASSIGN, TokenType.INT_VALUE, TokenType.SEMICOLON, TokenType.EOF]
    assert [token.value for token in tokens] == ['int', 'a', '', 10, '', '']
    assert [token.position for token in tokens] == [(1, 1), (1, 5), (1, 7), (1, 9), (1, 11), (2, 0)]