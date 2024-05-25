import io
import pytest

from src.reader import Reader
from src.lexer.lexer import Lexer

from src.token.token import Token
from src.token.token_types import TokenType

from src.parser.parser import Parser

from src.ast.abstract_node import Node
from src.ast.nodes import *


def create_parser(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return Parser(reader, lexer)


def test_parse_int():
    parser = create_parser("1")
    assert parser.parse_int() == IntValue(1)


def test_parse_float():
    parser = create_parser("1.5")
    assert parser.parse_float() == FloatValue(1.5)


def test_parse_string():
    parser = create_parser('"hello"')
    assert parser.parse_string() == StringValue("hello")


def test_parse_declaration():
    parser = create_parser("int a = 10")
    assert parser.parse_declaration() == Variable("int", Identifier("a"), IntValue(10))


def test_parse_arguments():
    string_arguments = "int a, bool b, float c, string d"
    parser = create_parser(string_arguments)
    arg_1 = Variable("int", Identifier("a"), None)
    arg_2 = Variable("bool", Identifier("b"), None)
    arg_3 = Variable("float", Identifier("c"), None)
    arg_4 = Variable("string", Identifier("d"), None)
    assert parser.parse_arguments() == [arg_1, arg_2, arg_3, arg_4]


def test_parse_list():
    parser = create_parser('[10, 20, 30]')
    assert parser.parse_list() == List([IntValue(10), IntValue(20), IntValue(30)])


def test_parse_length():
    parser = create_parser(".length()")
    tmp_list = [1, 2, 3]
    assert parser.parse_collection_operation(tmp_list) == Length(tmp_list)


def test_parse_type():
    parser = create_parser(".type()")
    tmp_list = [1, 2, 3]
    assert parser.parse_collection_operation(tmp_list) == Type(tmp_list)


def test_parse_at():
    parser = create_parser(".at(0)")
    tmp_list = [1, 2, 3]
    assert parser.parse_collection_operation(tmp_list) == At(tmp_list, IntValue(0))


def test_parse_append():
    parser = create_parser(".append(10)")
    tmp_list = [1, 2, 3]
    assert parser.parse_operation_append(tmp_list) == Append(tmp_list, IntValue(10))


def test_parse_remove():
    parser = create_parser(".remove(123)")
    tmp_list = [1, 2, 3]
    assert parser.parse_operation_remove(tmp_list) == Remove(tmp_list, IntValue(123))


def test_parse_get():
    parser = create_parser('.get("rok")')
    dict = {"rok": 2020}
    assert parser.parse_operation_remove(dict) == Remove(dict, StringValue("rok"))


def test_parse_dict():
    parser = create_parser('{"rok": 2020, "miesiac": 12, "dzien": 1}')
    pair_1 = Pair(StringValue("rok"), IntValue(2020))
    pair_2 = Pair(StringValue("miesiac"), IntValue(12))
    pair_3 = Pair(StringValue("dzien"), IntValue(1))
    pairs = [pair_1, pair_2, pair_3]
    assert parser.parse_dict() == Dict(pairs)


def test_parse_pair():
    parser = create_parser('["rok", 2024]')
    assert parser.parse_pair() == Pair(StringValue("rok"), IntValue(2024))


def test_parse_for():
    parser = create_parser("for(int i in numbers){int a = 10;}")

    body = Body([Variable("int", Identifier("a"), IntValue(10))])

    assert parser.parse_for() == ForStatement("int", Identifier("i"), Identifier("numbers"), body)


def test_parse_program():
    parser = create_parser(
        "function int name1(bool a, int b) { int a = 10; return 0; }"
    )

    arguments = [Variable("bool", Identifier("a")), Variable("int", Identifier("b"))]
    body = FunctionBody([Variable("int", Identifier("a"), IntValue(10))], IntValue(0))
    function = Function("int", Identifier("name1"), arguments, body)

    assert parser.parse() == [function]


def test_parse_add_expression():
    parser = create_parser(
        "1+2"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(2)

    assert parser.parse_sum_expression() == AddExpression(literal_1, literal_2)


def test_parse_subtract_expression():
    parser = create_parser(
        "1-2"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(2)

    assert parser.parse_sum_expression() == SubExpression(literal_1, literal_2, 1, 2)


def test_parse_multiply_expression():
    parser = create_parser(
        "1*2"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(2)

    assert parser.parse_multiply_expression() == MultiplyExpression(literal_1, literal_2)


def test_parse_divide_expression():
    parser = create_parser(
        "1/2"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(2)

    assert parser.parse_multiply_expression() == DivisionExpression(literal_1, literal_2)