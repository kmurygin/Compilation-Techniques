import io
import pytest
from src.interpreter.interpreter import Interpreter
from src.exceptions.interpreter_exception import *
from src.lexer.lexer import Lexer
from src.parser.parser import Parser
from src.reader import Reader


def create_parser(string):
    reader = Reader(io.StringIO(string))
    lexer = Lexer(reader)
    return Parser(reader, lexer)


def interpret(string):
    parser = create_parser(string)
    program = parser.parse()
    interpreter = Interpreter(program)
    return interpreter.run_main_function()


def test_double_function_declaration():
    with pytest.raises(FunctionAlreadyDefinedError):
        string = 'function int main(){return 3+1;} function int main(){return 3+1;}'
        result = interpret(string)
        assert result == 4


def test_undefined_variable():
    with pytest.raises(UndefinedVariableError):
        string = 'function int main(){return a;}'
        result = interpret(string)
        assert result == 4


def test_undefined_function():
    with pytest.raises(FunctionNotDefinedError):
        string = 'function int main(){return a();}'
        result = interpret(string)
        assert result == 4


def test_wrong_return_type():
    with pytest.raises(WrongTypeReturnError):
        string = 'function bool main(){return 4;}'
        result = interpret(string)
        assert result == 4


def test_different_types():
    with pytest.raises(WrongTypeError):
        string = 'function bool main(){float a = 10; return 4;}'
        result = interpret(string)
        assert result == 4
                                                               