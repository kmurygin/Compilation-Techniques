class WrongTypeError(Exception):
    def __init__(self, expected_type, actual_type, position):
        self.expected = expected_type
        self.actual = actual_type
        self.position = position

    def __str__(self):
        return f"WrongTypeError: Expected type {self.expected}, but got {self.actual} at position {self.position}"


class DifferentTypesListError(Exception):
    def __init__(self, position):
        self.position = position

    def __str__(self):
        return f"DifferentTypesListError: Different types of elements at position {self.position}"


class UndefinedVariableError(Exception):
    def __init__(self, variable_name, position):
        self.variable_name = variable_name
        self.position = position

    def __str__(self):
        return f"UndefinedVariableError: Undefined variable {self.variable_name} at line: {self.position[0]} column: {self.position[1]}"


class WrongTypeReturnError(Exception):
    def __init__(self, expected_type, actual_type, position):
        self.expected = expected_type
        self.actual = actual_type
        self.position = position

    def __str__(self):
        return f"WrongTypeReturnError: Expected return type {self.expected}, but got {self.actual} at line: {self.position[0]} column: {self.position[1]}"


class FunctionAlreadyDefinedError(Exception):
    def __init__(self, function_name):
        self.function_name = function_name

    def __str__(self):
        return f"FunctionAlreadyDefinedError: Function {self.function_name} is already defined"


class FunctionNotDefinedError(Exception):
    def __init__(self, function_name, position):
        self.function_name = function_name
        self.position = position

    def __str__(self):
        return f"FunctionNotDefinedError: Function {self.function_name} is not defined, line: {self.position[0]} at column: {self.position[1]}"