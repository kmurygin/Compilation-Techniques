from enum import Enum, auto


class TokenType(Enum):
    ID = auto()

    FUNCTION = auto()

    INT_KEYWORD = auto()
    FLOAT_KEYWORD = auto()
    STRING_KEYWORD = auto()
    BOOL_KEYWORD = auto()

    INT_VALUE = auto()
    FLOAT_VALUE = auto()
    STRING_VALUE = auto()
    BOOL_VALUE = auto()

    PAIR = auto()
    LIST = auto()
    DICT = auto()

    OR_SIGN = auto()
    AND_SIGN = auto()
    LESS_SIGN = auto()
    LESS_OR_EQUAL_SIGN = auto()
    GREATER_SIGN = auto()
    GREATER_OR_EQUAL_SIGN = auto()
    EQUAL_SIGN = auto()
    NOT_EQUAL_SIGN = auto()
    NEGATION_SIGN = auto()

    ASSIGN = auto()

    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    LEFT_CURLY_BRACKET = auto()
    RIGHT_CURLY_BRACKET = auto()

    ADD_SIGN = auto()
    SUB_SIGN = auto()
    MULTIPLY_SIGN = auto()
    DIVIDE_SIGN = auto()

    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELSE = auto()
    RETURN = auto()

    FROM = auto()
    IN = auto()
    WHERE = auto()
    SELECT = auto()
    ORDER_BY = auto()

    TRUE_VALUE = auto()
    FALSE_VALUE = auto()

    SEMICOLON = auto()
    COMMA = auto()

    COMMENT = auto()
    EOF = auto()
