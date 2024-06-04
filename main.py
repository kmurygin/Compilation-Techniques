from src.interpreter.interpreter import Interpreter
from src.reader import Reader
from src.lexer.lexer import Lexer
from src.parser.parser import Parser


def main(file):
    with open(file, "r") as file_handle:
        reader = Reader(file_handle)
        lexer = Lexer(reader)
        parser = Parser(reader, lexer)
        program = parser.parse()
        interpreter = Interpreter(program)
        result = interpreter.run_main_function()
        print(result)


if __name__ == '__main__':
    main("program.ks")
