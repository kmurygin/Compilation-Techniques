import io
import pytest

from src.reader import Reader
from src.lexer.lexer import Lexer

from src.token.token import Token
from src.token.token_types import TokenType


def get_one_token(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return lexer.get_next_token()


def test_lexer_EOF():
    token = get_one_token("")
    assert token.type == TokenType.EOF


def test_lexer_whitespaces():
    token = get_one_token(" ")
    assert token.type == TokenType.EOF


def test_lexer_function():
    token = get_one_token("function")
    assert token.type == TokenType.FUNCTION


def test_lexer_for():
    token = get_one_token("for")
    assert token.type == TokenType.FOR


def test_lexer_while():
    token = get_one_token("while")
    assert token.type == TokenType.WHILE


def test_lexer_if():
    token = get_one_token("if")
    assert token.type == TokenType.IF


def test_lexer_else():
    token = get_one_token("else")
    assert token.type == TokenType.ELSE


def test_lexer_return():
    token = get_one_token("return")
    assert token.type == TokenType.RETURN
    assert token.position == (1, 1)


def test_lexer_from():
    token = get_one_token("from")
    assert token.type == TokenType.FROM
    assert token.position == (1, 1)


def test_lexer_in():
    token = get_one_token("in")
    assert token.type == TokenType.IN
    assert token.position == (1, 1)


def test_lexer_where():
    token = get_one_token("where")
    assert token.type == TokenType.WHERE
    assert token.position == (1, 1)


def test_lexer_select():
    token = get_one_token("select")
    assert token.type == TokenType.SELECT
    assert token.position == (1, 1)


def test_lexer_orderby():
    token = get_one_token("orderby")
    assert token.type == TokenType.ORDER_BY
    assert token.position == (1, 1)


def test_lexer_keyword_int():
    token = get_one_token("int")
    assert token.type == TokenType.INT_KEYWORD


def test_lexer_string():
    token = get_one_token('"jakis tam string"')
    assert token.type == TokenType.STRING_VALUE
    assert token.value == "jakis tam string"
    assert token.position == (1, 1)


def test_lexer_int():
    token = get_one_token("10")
    assert token.type == TokenType.INT_VALUE
    assert token.value == 10
    assert token.position == (1, 1)


def test_lexer_float():
    token = get_one_token("3.14")
    assert token.type == TokenType.FLOAT_VALUE
    assert token.value == 3.14
    assert token.position == (1, 1)


def test_lexer_bracket_left():
    token = get_one_token("(")
    assert token.type == TokenType.LEFT_BRACKET


def test_lexer_bracket_right():
    token = get_one_token(")")
    assert token.type == TokenType.RIGHT_BRACKET
    assert token.position == (1, 1)


def test_lexer_curlybracket_left():
    token = get_one_token("{")
    assert token.type == TokenType.LEFT_CURLY_BRACKET
    assert token.position == (1, 1)


def test_lexer_curlybracket_right():
    token = get_one_token("}")
    assert token.type == TokenType.RIGHT_CURLY_BRACKET
    assert token.position == (1, 1)


def test_lexer_add():
    token = get_one_token("+")
    assert token.type == TokenType.ADD_SIGN


def test_lexer_sub():
    token = get_one_token("-")
    assert token.type == TokenType.SUB_SIGN


def test_lexer_mul():
    token = get_one_token("*")
    assert token.type == TokenType.MULTIPLY_SIGN


def test_lexer_div():
    token = get_one_token("/")
    assert token.type == TokenType.DIVIDE_SIGN


def test_lexer_less():
    token = get_one_token("<")
    assert token.type == TokenType.LESS_SIGN


def test_lexer_greater():
    token = get_one_token(">")
    assert token.type == TokenType.GREATER_SIGN


def test_lexer_less_or_equal():
    token = get_one_token("<=")
    assert token.type == TokenType.LESS_OR_EQUAL_SIGN


def test_lexer_greater_or_equal():
    token = get_one_token(">=")
    assert token.type == TokenType.GREATER_OR_EQUAL_SIGN


def test_lexer_equal():
    token = get_one_token("==")
    assert token.type == TokenType.EQUAL_SIGN
    assert token.position == (1, 1)


def test_lexer_assign():
    token = get_one_token("=")
    assert token.type == TokenType.ASSIGN
    assert token.position == (1, 1)


def test_lexer_negation():
    token = get_one_token("!")
    assert token.type == TokenType.NEGATION_SIGN
    assert token.position == (1, 1)


def test_lexer_not_equal():
    token = get_one_token("!=")
    assert token.type == TokenType.NOT_EQUAL_SIGN
    assert token.position == (1, 1)


def test_lexer_and():
    token = get_one_token("&&")
    assert token.type == TokenType.AND_SIGN


def test_lexer_or():
    token = get_one_token("||")
    assert token.type == TokenType.OR_SIGN
