class LexerException(Exception):
    def __init__(self, message, position):
        self.message = message
        self.line = position[0]
        self.column = position[1]

    def __str__(self):
        return f"LexerException: {self.message} in line:{self.line} column:{self.column}"


class CommentTooLongException(LexerException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"CommentTooLongException: {self.message} in line:{self.line} column:{self.column}"


class StringTooLongException(LexerException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"StringTooLongException: {self.message} in line:{self.line} column:{self.column}"


class IdentifierTooLongException(LexerException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"IdentifierTooLongException: {self.message} in line:{self.line} column:{self.column}"


class UnclosedStringException(LexerException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"UnclosedStringException: {self.message} in line:{self.line} column:{self.column}"


class NumberException(LexerException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"TooBigNumberException: {self.message} in line:{self.line} column:{self.column}"