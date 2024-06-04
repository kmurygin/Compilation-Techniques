class ParserException(Exception):
    def __init__(self, position):
        self.line = position[0]
        self.column = position[1]


class SyntaxError(ParserException):
    def __init__(self, message, position):
        super().__init__(position)
        self.message = message

    def __str__(self):
        return f"SyntaxError: Expected {self.message} in line:{self.line} column:{self.column}"


class NoSemicolonError(ParserException):
    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return f"NoSemicolonError: Missing semicolon in line:{self.line} column:{self.column}"


class NoClosingCurlyBracketError(ParserException):
    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return f"NoClosingCurlyBracketError: Missing closing curly bracket in line:{self.line} column:{self.column}"


class NoClosingBracketError(ParserException):
    def __init__(self, position):
        super().__init__(position)

    def __str__(self):
        return f"NoClosingBracketError: Missing closing bracket in line:{self.line} column:{self.column}"