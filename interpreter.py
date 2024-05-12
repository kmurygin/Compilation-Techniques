from src.token.token import Token
from src.token.token_types import TokenType
from src.lexer.lexer import Lexer, get_tokens
from src.reader import Reader
import io
import sys


def main(arguments):
    with open(arguments[1], "r") as file_handle:
        reader = Reader(file_handle)
        lexer = Lexer(reader)
        all_tokens = get_tokens(lexer)
    for token in all_tokens:
        print(token)


if __name__ == '__main__':
    main(sys.argv)
