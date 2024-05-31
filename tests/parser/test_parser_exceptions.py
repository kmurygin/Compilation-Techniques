import io
import pytest

from src.reader import Reader
from src.lexer.lexer import Lexer

from src.token.token import Token
from src.token.token_types import TokenType

from src.parser.parser import Parser
from src.ast.nodes import *
from src.exceptions.parser_exception import *


def create_parser(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return Parser(reader, lexer)


def test_single_statement_no_semicolon():
    with pytest.raises(NoSemicolonError) as e:
        parser = create_parser("function int main(){int a \n int b}")
        parser.parse()


def test_single_statement_no_closing_curly_bracket():
    with pytest.raises(NoClosingCurlyBracketError) as e:
        parser = create_parser("function int main(){int a; \n int b;")
        parser.parse()


def test_single_statement_no_closing_curly_bracket():
    with pytest.raises(NoClosingBracketError) as e:
        parser = create_parser("function int main({int a; \n int b;")
        parser.parse()


