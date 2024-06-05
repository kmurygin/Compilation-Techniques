#!/usr/bin/env python3

import sys

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
        try:
            result = interpreter.visit_program()
            print(result)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    main("program.ks")
