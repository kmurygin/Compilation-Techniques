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
    assert parser.parse_literal() == IntValue(1)


def test_parse_float():
    parser = create_parser("1.5")
    assert parser.parse_literal() == FloatValue(1.5)


def test_parse_string():
    parser = create_parser('"hello"')
    assert parser.parse_literal() == StringValue("hello")


def test_parse_list():
    parser = create_parser('[10, 20, 30]')
    assert parser.parse_list() == List([IntValue(10), IntValue(20), IntValue(30)])


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
    parser = create_parser("for(int i in numbers){print(i);}")
    assert parser.parse_for() == ForStatement(
        "int",
        Identifier("i"),
        Identifier("numbers"),
        Body(
            StatementBlock(
                [
                    FunctionCall(
                        Identifier("print"),
                        Arguments([
                            Identifier("i")
                        ])
                    )
                ]
            )
        )
    )


def test_parse_for_sorted():
    parser = create_parser("for(int i in numbers, key=funkcja_key){ print(i); }")
    assert parser.parse_for() == ForSortedStatement(
        "int",
        Identifier("i"),
        Identifier("numbers"),
        Identifier("funkcja_key"),
        Body(
            StatementBlock(
                [
                    FunctionCall(
                        Identifier("print"),
                        Arguments([
                            Identifier("i")
                        ])
                    )
                ]
            )
        )
    )


def test_parse_program():
    parser = create_parser(
        'function int main() { function int name1(bool a, int b) { int a = 10; return a+26; }; return 0; print("Hello world!");}'
    )

    assert (parser.parse() ==
            Program([
                Function("int", Identifier("main"), [],
                         StatementBlock([
                             Function("int", Identifier("name1"),
                                      [("bool", Identifier("a")), ("int", Identifier("b"))],
                                      StatementBlock([
                                          InitStatement("int", Identifier("a"), 1, 1, IntValue(10)),
                                          ReturnStatement(AddExpression(Identifier("a"), IntValue(26)))])),
                             FunctionCall(Identifier("print"), Arguments([StringValue("Hello world!")])),
                             ReturnStatement("0")
                         ])
                         )]))


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


def test_parse_and_expression():
    parser = create_parser(
        "1 && 10"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(10)

    assert parser.parse_and_expression() == AndExpression(literal_1, literal_2)


def test_parse_or_expression():
    parser = create_parser(
        "1 || Kacper"
    )
    literal_1 = IntValue(1)
    literal_2 = Identifier("Kacper")

    assert parser.parse_expression() == OrExpression(literal_1, literal_2)


def test_parse_expression():
    parser = create_parser(
        "4 + 1 * 2 / trzy"
    )
    literal_1 = IntValue(1)
    literal_2 = IntValue(2)
    literal_3 = Identifier("trzy")
    literal_4 = IntValue(4)

    assert parser.parse_expression() == AddExpression(
        literal_4,
        DivisionExpression(
            MultiplyExpression(literal_1, literal_2), literal_3
        )
    )


def test_assignment():
    parser = create_parser(
        "a = 10"
    )
    identifier = Identifier("a")
    expression = IntValue(10)

    assert parser.parse_assignment() == Assignment(identifier, expression)


def test_assignment_complex():
    parser = create_parser(
        "a = 10 + 20 / 10"
    )
    identifier = Identifier("a")
    expression = AddExpression(IntValue(10), DivisionExpression(IntValue(20), IntValue(10)))
    assert parser.parse_assignment() == Assignment(identifier, expression)


def test_function_call():
    parser = create_parser(
        "funkcja(20, 40.7)"
    )
    identifier = Identifier("funkcja")
    arguments = Arguments([IntValue("20"), FloatValue("40.7")])

    assert parser.parse_function_call() == FunctionCall(identifier, arguments)


def test_function_call_single_statement():
    parser = create_parser(
        "funkcja(20, 40.7)"
    )
    identifier = Identifier("funkcja")
    arguments = Arguments([IntValue("20"), FloatValue("40.7")])

    assert parser.parse_single_statement() == FunctionCall(identifier, arguments)


def test_method_call():
    parser = create_parser(
        "obiekt.metoda(10)"
    )
    expression = Identifier("obiekt")
    method_name = Identifier("metoda")
    arguments = Arguments([IntValue("10")])

    assert parser.parse_method_call() == MethodCall(expression, method_name, arguments)


def test_parse_single_statement_method_call():
    parser = create_parser(
        "nazwa.metoda(10, 20);"
    )
    expression = Identifier("nazwa")
    method_name = Identifier("metoda")
    arguments = Arguments([IntValue("10"), IntValue("20")])

    assert parser.parse_single_statement() == MethodCall(expression, method_name, arguments)


def test_parse_single_statement_function_call():
    parser = create_parser(
        "funkcja(10, 20);"
    )
    function_name = Identifier("fumkcja")
    arguments = Arguments([IntValue("10"), IntValue("20")])

    assert parser.parse_single_statement() == FunctionCall(function_name, arguments)


def test_function_declaration():
    parser = create_parser(
        "function int funkcja_1 (int a, int b) { a = a + 10; return a+b; }"
    )
    function_declaration = Function(
        "int",
        Identifier("funkcja_1"),
        # enum zamiasy "int" oraz argument obuduj w klase
        [("int", Identifier("a")), ("int", Identifier("b"))],
        StatementBlock(
            ReturnStatement(
                AddExpression(Identifier("a"), Identifier("b"))
            )
        )
    )

    assert parser.parse_function_declaration() == function_declaration


def test_function_params():
    pass


def test_var_declaration_with_assignment():
    parser = create_parser(
        "int a = 10;"
    )
    assert parser.parse_init_statement() == InitStatement("int", Identifier("a"), IntValue("10"))


def test_var_declaration():
    parser = create_parser(
        "int a;"
    )
    assert parser.parse_init_statement() == Declaration("int", Identifier("a"))


def test_list_declaration_with_assignment():
    parser = create_parser(
        "List<int> lista_1 = [1, 2, 3];"
    )
    assert parser.parse_init_statement() == InitStatement(
        ListType("int"),
        Identifier("lista_1"),
        List([
            IntValue("1"),
            IntValue("2"),
            IntValue("3")
        ])
    )


def test_pair_declaration_with_assignment():
    parser = create_parser(
        'Pair<int, string> para_1 = (1, "Kacper")'
    )
    assert parser.parse_init_statement() == InitStatement(
        PairType("int", "string"),
        Identifier("para_1"),
        Pair(
            IntValue("1"),
            StringValue("Kacper"),
        )
    )


def test_dict_declaration_with_assignment():
    parser = create_parser(
        'Dict<int, string> slownik_1 = {1: "hello_world"}'
    )
    assert parser.parse_init_statement() == InitStatement(
        DictType("int", "string"),
        Identifier("slownik_1"),
        Dict([
            Pair(IntValue("1"), StringValue("hello_world"))
        ])
    )


def test_parse_add_with_function_call():
    parser = create_parser(
        "a + funkcja(10)"
    )
    assert parser.parse_single_statement() == AddExpression(
        Identifier("a"),
        FunctionCall(
            Identifier("funkcja"),
            Arguments([IntValue("10")])
        )
    )


def test_parse_add_with_method_call():
    parser = create_parser(
        "a + slownik.get(10)"
    )
    assert parser.parse_single_statement() == AddExpression(
        Identifier("a"),
        MethodCall(
            Identifier("slownik_1"),
            Identifier("get"),
            Arguments([IntValue("10")])
        )
    )
