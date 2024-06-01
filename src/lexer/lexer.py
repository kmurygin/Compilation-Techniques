from src.token.token_types import TokenType
from src.token.token import Token
from src.exceptions import lexer_exception
import math

STRING_LIMIT_CHARS = 10_000
NUMBER_LIMIT_DIGITS = 1_000

ID_LIMIT_CHARS = 100

MAX_NUMBER = 10_000_000
MIN_NUMBER = -MAX_NUMBER


class Lexer:
    def __init__(self, reader):
        self.reader = reader
        self.current_token = None
        self.current_position = (0, 0)
        self.previous_position = (0, 0)

        self.token_dictionary = {
            "Pair": TokenType.PAIR,
            "Dict": TokenType.DICT,
            "List": TokenType.LIST,
            "int": TokenType.INT_KEYWORD,
            "float": TokenType.FLOAT_KEYWORD,
            "string": TokenType.STRING_KEYWORD,
            "bool": TokenType.BOOL_KEYWORD,

            # "SELECT": TokenType.SELECT,
            # "WHERE": TokenType.WHERE,
            # "FROM": TokenType.FROM,
            # "at": TokenType.AT,
            # "append": TokenType.APPEND,
            # "remove": TokenType.REMOVE,
            # "first": TokenType.FIRST,
            # "second": TokenType.SECOND,

            "function": TokenType.FUNCTION,
            "for": TokenType.FOR,
            "while": TokenType.WHILE,
            "return": TokenType.RETURN,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "from": TokenType.FROM,
            "in": TokenType.IN,
            "where": TokenType.WHERE,
            "select": TokenType.SELECT,
            "orderby": TokenType.ORDER_BY,
            "EOF": TokenType.EOF,

            "key": TokenType.KEY,
        }

        self.token_dictionary_sign = {
            "(": TokenType.LEFT_BRACKET,
            ")": TokenType.RIGHT_BRACKET,
            "{": TokenType.LEFT_CURLY_BRACKET,
            "}": TokenType.RIGHT_CURLY_BRACKET,
            "[": TokenType.LEFT_SQUARE_BRACKET,
            "]": TokenType.RIGHT_SQUARE_BRACKET,
            ",": TokenType.COMMA,
            ".": TokenType.DOT,
            ";": TokenType.SEMICOLON,
            ":": TokenType.COLON
        }

        self.token_dictionary_operators = {
            "||": TokenType.OR_SIGN,
            "&&": TokenType.AND_SIGN,
            "<": TokenType.LESS_SIGN,
            "<=": TokenType.LESS_OR_EQUAL_SIGN,
            ">": TokenType.GREATER_SIGN,
            ">=": TokenType.GREATER_OR_EQUAL_SIGN,
            "=": TokenType.ASSIGN,
            "==": TokenType.EQUAL_SIGN,
            "!=": TokenType.NOT_EQUAL_SIGN,
            "!": TokenType.NEGATION_SIGN,
        }

        self.token_dictionary_operators_one_char = {
            "+": TokenType.ADD_SIGN,
            "-": TokenType.SUB_SIGN,
            "*": TokenType.MULTIPLY_SIGN,
            "/": TokenType.DIVIDE_SIGN,
        }

    def get_next_token(self):
        self.current_token = self.try_build_token()
        return self.current_token

    def get_current_token(self):
        return self.current_token

    def get_current_position(self):
        return self.current_position

    def try_build_token(self):
        self.skip_whitespace()
        self.current_position = self.reader.get_current_position()

        token = (
            self.try_build_sign() or
            self.try_build_comment() or
            self.try_build_eof() or
            self.try_build_operator() or
            self.try_build_number() or
            self.try_build_string() or
            self.try_build_keyword_or_identifier()
        )

        if token:
            return token

    def try_build_sign(self):
        character = self.get_char()
        if character in self.token_dictionary_sign.keys():
            self.get_next_char()
            return Token(self.token_dictionary_sign[character], None, self.current_position)
        else:
            return None

    def try_build_eof(self):
        if self.get_char() == 'EOF':
            return Token(TokenType.EOF, None, self.current_position)
        return None

    def try_build_comment(self):
        text_comment = str()
        character = self.get_char()

        if not character == '#':
            return None

        self.get_next_char()
        character = self.get_char()

        while not character == '\n' or character == 'EOF':
            text_comment = text_comment + character
            self.get_next_char()
            character = self.get_char()
            if len(text_comment) > STRING_LIMIT_CHARS:
                raise lexer_exception.CommentTooLongException("Comment too long", self.current_position)
        self.get_next_char()
        token = Token(TokenType.COMMENT, text_comment, self.current_position)
        return token

    def try_build_operator(self):
        operator = ""
        character = self.get_char()
        if character in self.token_dictionary_operators_one_char.keys():
            self.get_next_char()
            return Token(self.token_dictionary_operators_one_char[character], operator, self.current_position)
        if character in ['<', '>', '=', '!']:
            operator += character
            self.get_next_char()
            character = self.get_char()
            if not character == "=":
                return Token(self.token_dictionary_operators[operator], operator, self.current_position)
            elif character == "=":
                operator += character
                return Token(self.token_dictionary_operators[operator], operator, self.current_position)
        if character in ['|','&']:
            token = self.build_logical_operator(character)
            self.get_next_char()
            if token:
                return token
        return None

    def build_logical_operator(self, character):
        operator = str()
        operator += character
        self.get_next_char()
        character = self.get_char()
        if character == operator:
            operator += character
            return Token(self.token_dictionary_operators[operator], None, self.current_position)
        return None

    def try_build_number(self):
        if not self.get_char().isdigit():
            return None

        int_number = self.build_integer_number()

        if not self.get_char() == ".":
            if int_number > MAX_NUMBER:
                raise lexer_exception.NumberException("Number above max", self.current_position)
            elif int_number < MIN_NUMBER:
                raise lexer_exception.NumberException("Number below min", self.current_position)

            return Token(TokenType.INT_VALUE, int_number, self.current_position)

        self.get_next_char()
        float_part = self.build_integer_number()

        digits = int(math.log10(float_part)) + 1
        number = float(int_number) + float_part * 10 ** -digits

        if number > MAX_NUMBER:
            raise lexer_exception.NumberException("Number above max", self.current_position)
        elif number < MIN_NUMBER:
            raise lexer_exception.NumberException("Number below min", self.current_position)

        return Token(TokenType.FLOAT_VALUE, number, self.current_position)

    def build_integer_number(self):
        character = self.get_char()
        built_number = 0
        while character.isdigit():
            built_number = built_number * 10 + int(character)
            self.get_next_char()
            character = self.get_char()
        return built_number

    def try_build_string(self):
        text = str()
        character = self.get_char()

        if not character == '"':
            return None

        self.get_next_char()
        character = self.get_char()

        while not character == '"':
            text = text + character
            self.get_next_char()
            character = self.get_char()
            if len(text) > STRING_LIMIT_CHARS:
                raise lexer_exception.StringTooLongException("String too long", self.current_position)
            if character == '\n' or character == 'EOF':
                raise lexer_exception.UnclosedStringException("Unclosed string", self.current_position)

        token = Token(TokenType.STRING_VALUE, text, self.current_position)
        self.get_next_char()
        return token

    def try_build_keyword_or_identifier(self):
        text = str()
        character = self.get_char()
        while (character.isalpha() or character == "_" or character.isdigit()) and character != 'EOF':
            text += character
            self.get_next_char()
            character = self.get_char()
            if len(text) > ID_LIMIT_CHARS:
                raise lexer_exception.IdentifierTooLongException("Identifier too long", self.current_position)
        if text == "":
            return None
        elif text in ("true", "false"):
            return Token(TokenType.BOOL_VALUE, text, self.current_position)
        elif text in self.token_dictionary.keys():
            return Token(self.token_dictionary[text], text, self.current_position)
        return Token(TokenType.ID, text, self.current_position)

    def skip_whitespace(self):
        char = self.get_char()
        while char.isspace():
            self.get_next_char()
            char = self.get_char()

    def get_char(self):
        return self.reader.get_current_char()

    def get_next_char(self):
        self.previous_position = self.reader.get_current_position()
        return self.reader.next()


def get_tokens(lexer):
    tokens = list()
    while (next_token := lexer.get_next_token()).type != TokenType.EOF:
        tokens.append(next_token)
    tokens.append(next_token)
    return tokens
