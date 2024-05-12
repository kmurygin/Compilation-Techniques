class ParserException(Exception):
    def __init__(self, message, position):
        self.message = message
        self.line = position[0]
        self.column = position[1]

    def __str__(self):
        return f"LexerException: {self.message} in line:{self.line} column:{self.column}"


class SyntaxError(ParserException):
    def __init__(self, message, position):
        super().__init__(message, position)

    def __str__(self):
        return f"SyntaxError: Expected {self.message} in line:{self.line} column:{self.column}"
