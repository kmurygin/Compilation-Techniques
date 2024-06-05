from src.exceptions.interpreter_exception import *
from src.interpreter.scope import Scope
from src.ast.nodes import *


def length(object, arguments=None):
    return len(object)


def add(dictionary, arguments):
    if type(dictionary) is dict:
        dictionary[arguments[0]] = arguments[1]
        return dictionary
    else:
        dictionary[1][arguments[0]] = arguments[1]
        return dictionary


def delete(dictionary, arguments):
    del dictionary[arguments[0]]
    return dictionary


def get(dictionary, arguments):
    return dictionary[arguments[0]]


def contains(dictionary, arguments):
    return dictionary.__contains__(arguments[0])


def first(pair, arguments=None):
    return pair[1][0]


def second(pair, arguments=None):
    return pair[1][1]


def append(list, arguments=None):
    list.append(arguments[0])
    return list


def remove(list, arguments=None):
    list[1].remove(arguments[0])
    return list


def at(list, arguments=None):
    return list[arguments[0]]


def get_type(list, arguments=None):
    return type(list[0])


def get_print(arguments):
    lista = [argument for argument in arguments]
    print(*lista)


def get_int(value):
    return int(value[0])


def get_string():
    pass


BUILTIN_METHODS = {
    'length': length,
    'add': add,
    'delete': delete,
    'get': get,
    'contains': contains,
    "first": first,
    "second": second,
    "type": get_type,
    "at": at,
    "append": append,
    "remove": remove,
}

BUILTIN_FUNCTIONS = {
    'print': get_print,
    'get_int': get_int,
    'get_string': get_string
}


class Interpreter:
    def __init__(self, program):
        self.global_variables = {}
        self.function_definitions = {}
        self.scopes_stack = []
        self.current_scope = None
        self.program = program
        self.last_value = None

        self.builtin_functions = {
            'print': lambda arguments: print(*arguments),
            'get_int': lambda value: setattr(self, 'last_value', int(value[0])),
            'get_float': lambda value: setattr(self, 'last_value', float(value[0])),
            'get_string': lambda value: setattr(self, 'last_value', str(value[0]))
        }

    def visit_program(self):
        for declaration in self.program.program_body:
            declaration.accept(self)

        self.current_scope = Scope(
            self.function_definitions['main'],
            (0, 0),
            []
        )
        return self.run_main_function()

    def run_main_function(self):
        main_function = self.function_definitions['main']
        main_function_call = FunctionCall(Identifier('main'), Arguments([]), 0, 0)
        main_function_call.accept(self)
        return self.last_value

    def visit_declaration(self, declaration, global_declaration):
        if global_declaration:
            scope = self.global_variables
        else:
            scope = self.current_scope.local_variables

        scope[declaration.identifier] = None

    def visit_identifier(self, identifier):
        self.last_value = identifier.value

    def visit_init_statement(self, init_statement, global_declaration):
        if global_declaration:
            scope = self.global_variables
        else:
            scope = self.current_scope.local_variables

        init_statement.expression.accept(self)
        value = self.last_value
        try:
            init_statement.type.accept(self)
        except TypeError:
            init_statement.type.accept(self, self)
        type = self.last_value
        self.check_type(type, value, (init_statement.line, init_statement.column))

        init_statement.identifier.accept(self)

        scope[self.last_value] = (type, value)

    def visit_function_definition(self, function_definition):
        function_definition.identifier.accept(self)
        function_identifier = self.last_value
        if function_identifier in self.function_definitions:
            raise FunctionAlreadyDefinedError(function_identifier)
        self.function_definitions[function_identifier] = function_definition

    def visit_bool_value(self, bool_value):
        self.last_value = bool_value.value

    def visit_int_value(self, int_value):
        self.last_value = int_value.value

    def visit_float_value(self, float_value):
        self.last_value = float_value.value

    def visit_string_value(self, string_value):
        self.last_value = string_value.value

    def visit_boolean_value(self, boolean_value):
        self.last_value = boolean_value.value

    def visit_variable(self, variable):
        variable.name.accept(self)
        variable_name = self.last_value
        value = self.get_variable(variable_name, (variable.line, variable.column))
        self.last_value = value

    def visit_function_call(self, function_call):
        function_call.identifier.accept(self)
        function_id = self.last_value

        if function_id in self.builtin_functions:
            function = self.builtin_functions[function_id]
            function_call.arguments.accept(self)
            function(self.last_value)
        else:
            function_definition = self.get_function_definition(function_id, function_call.position)
            function_call.arguments.accept(self)
            new_scope = Scope(
                function_definition,
                function_call.position,
                self.last_value
            )
            self.scopes_stack.append(self.current_scope)
            if len(self.scopes_stack) == 10:
                raise MaximumRecursionExceededError(function_call.position)
            self.current_scope = new_scope
            function_definition.body.accept(self)

    def visit_method_call(self, method_call):
        method_call.expression.accept(self)
        method_expression = self.last_value
        method_call.method_identifier.accept(self)
        method_id = self.last_value
        method_call.arguments.accept(self)
        method_arguments = self.last_value
        method_body = BUILTIN_METHODS[method_id]

        variable_name = self.get_variable(method_expression)
        if variable_name is not None:
            method_expression = variable_name
        self.last_value = method_body(method_expression, method_arguments)

    def visit_statement_block(self, statement_block):
        for statement in statement_block.statements:
            statement.accept(self)
            if self.last_value is not None:
                pass

    def visit_arguments(self, arguments):
        if len(arguments.arguments) > 0:
            return_value = []
            for exp in arguments.arguments:
                exp.accept(self)
                return_value.append(self.last_value)

            self.last_value = return_value
        else:
            self.last_value = []

    def visit_linq(self, linq):
        result = []
        from_statement = linq.from_statement
        # from_type = from_statement[0]
        from_statement[1].accept(self)
        from_id = self.last_value

        from_statement[2].accept(self)
        data = self.get_variable(self.last_value)

        all_pairs = list(data[1].items())
        for pair in all_pairs:
            new_scope = Scope()
            new_scope.local_variables[from_id] = (None, pair)
            self.scopes_stack.append(self.current_scope)
            self.current_scope = new_scope
            # where
            linq.where_statement.accept(self)
            if self.last_value:
                # select
                linq.select_statement.accept(self)
                result.append(self.last_value)

            frame = self.scopes_stack.pop()
            self.current_scope = frame
        # select

        # orderby

        # orderby_statement = linq.orderby_statement.accept(self)
        self.last_value = result

    def visit_assignment(self, assignment):

        assignment.identifier.accept(self)
        variable_id = self.last_value

        type, variable = self.get_variable(variable_id, assignment.position)

        assignment.expression.accept(self)
        value = self.last_value

        self.check_type(type, value[1], assignment.position)
        self.current_scope.local_variables[variable_id] = value

    def visit_if_statement(self, if_statement):
        if_statement.condition.accept(self)
        condition = self.last_value
        self.check_type(bool, condition, if_statement.position)
        if condition:
            if_statement.true_statement.accept(self)
        else:
            if_statement.false_statement.accept(self)

    def visit_while_statement(self, while_statement):
        while_statement.condition.accept(self)
        condition = self.last_value
        self.check_type(bool, condition, while_statement.position)
        i = 0

        while condition:
            # scope dla bloku
            while_statement.body.accept(self)
            return_value = self.last_value
            if return_value:
                pass
            if i == 100:
                raise MaximumIterationsExceededError(while_statement.position)

            while_statement.condition.accept(self)
            condition = self.last_value
            i += 1

# nie rob osobnych scopw, ale przypisz nowe a w kolejnej iteracji
    def visit_for_statement(self, for_statement):
        # type = for_statement.type.accept(self)
        for_statement.identifier.accept(self)
        identifier = self.last_value
        for_statement.collection.accept(self)
        collection = self.last_value
        collection = self.get_variable(collection)
        for element in collection[1]:
            new_frame = Scope()
            new_frame.local_variables[identifier] = element
            self.scopes_stack.append(self.current_scope)
            self.current_scope = new_frame
            # where
            for_statement.body.accept(self)

            frame = self.scopes_stack.pop()
            self.current_scope = frame

    def visit_return_statement(self, return_statement):
        return_statement.expression.accept(self)
        return_value = self.last_value
        if self.current_scope.return_value_type in (IntType, BoolType, StringType, FloatType):
            self.current_scope.return_value_type.accept(self, self)
            if self.last_value == type(return_value):
                scope = self.scopes_stack.pop()
                self.current_scope = scope
                self.last_value = return_value
            else:
                raise WrongTypeReturnError(self.current_scope.return_value_type, type(return_value),
                                           return_statement.position)
        else:
            self.current_scope.return_value_type.accept(self)
            if self.last_value == return_value[0]:
                scope = self.scopes_stack.pop()
                self.current_scope = scope
                self.last_value = return_value
            else:
                raise WrongTypeReturnError(self.last_value[1].__name__, type(return_value[1][0]).__name__,
                                           return_statement.position)

    def visit_expression(self, expression):
        pass

    def visit_and_expression(self, and_expression):
        and_expression.left.accept(self)
        left_result = self.last_value
        if type(left_result) is not bool:
            raise WrongTypeError(bool, type(left_result), and_expression.position)
        if not left_result:
            self.last_value = False
        and_expression.right.accept(self)
        right_result = self.last_value
        if type(left_result) is not bool:
            raise WrongTypeError(bool, type(right_result), and_expression.position)
        self.last_value = left_result and right_result

    def visit_or_expression(self, or_expression):
        or_expression.left.accept(self)
        left_result = self.last_value
        if type(left_result) is not bool:
            raise WrongTypeError(bool, type(left_result), or_expression.position)
        if left_result:
            self.last_value = True
        or_expression.right.accept(self)
        right_result = self.last_value
        if type(left_result) is not bool:
            raise WrongTypeError(bool, type(right_result), or_expression.position)
        self.last_value = left_result or right_result

    def visit_add_expression(self, add_expression):
        add_expression.left.accept(self)
        left_result = self.last_value
        add_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result + right_result

    def visit_sub_expression(self, sub_expression):
        sub_expression.left.accept(self)
        left_result = self.last_value
        sub_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result - right_result

    def visit_multiply_expression(self, multiply_expression):
        multiply_expression.left.accept(self)
        left_result = self.last_value
        multiply_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result * right_result

    def visit_division_expression(self, division_expression):
        division_expression.left.accept(self)
        left_result = self.last_value
        division_expression.right.accept(self)
        right_result = self.last_value
        if right_result == 0:
            raise ZeroDivisionError(division_expression.position)
        self.last_value = left_result / right_result

    def visit_less_than_expression(self, less_than_expression):
        less_than_expression.left.accept(self)
        left_result = self.last_value
        less_than_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result < right_result

    def visit_greater_than_expression(self, greater_than_expression):
        greater_than_expression.left.accept(self)
        left_result = self.last_value
        greater_than_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result > right_result

    def visit_less_than_or_equal_expression(self, less_than_equal_expression):
        less_than_equal_expression.left.accept(self)
        left_result = self.last_value
        less_than_equal_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result <= right_result

    def visit_greater_than_equal_expression(self, greater_than_equal_expression):
        greater_than_equal_expression.left.accept(self)
        left_result = self.last_value
        greater_than_equal_expression.right.accept(self)
        right_result = self.last_value
        self.last_value = left_result >= right_result

    def visit_list(self, list):
        result = []
        list.elements[0].accept(self)
        prev_element = self.last_value
        for element in list.elements:
            element.accept(self)
            next_element = self.last_value
            if type(next_element) != type(prev_element):
                raise DifferentTypesListError((element.line, element.column))
            result.append(next_element)
            prev_element = next_element
        self.last_value = result

    def visit_pair(self, pair):
        pair.left.accept(self)
        left = self.last_value

        pair.right.accept(self)
        right = self.last_value

        self.last_value = tuple((left, right))

    def visit_dict(self, dict):
        result = {}
        for pair in dict.pairs:
            pair.left.accept(self)
            key = self.last_value
            pair.right.accept(self)
            value = self.last_value
            result[key] = value
        self.last_value = result

    def visit_list_type(self, list_type):
        self.last_value = ("list", list_type.type)

    def visit_pair_type(self, pair_type):
        left_type = pair_type.type_1
        right_type = pair_type.type_2
        self.last_value = ("pair", left_type, right_type)

    def visit_dict_type(self, dict_type):
        left_type = dict_type.key_type
        right_type = dict_type.value_type
        self.last_value = ("dict", left_type, right_type)

    def visit_int_type(self, int_type):
        self.last_value = int

    def visit_float_type(self, float_type):
        self.last_value = float

    def visit_bool_type(self, bool_type):
        self.last_value = bool

    def visit_string_type(self, string_type):
        self.last_value = str

    def get_function_definition(self, name, position):
        if name in self.function_definitions:
            return self.function_definitions[name]
        raise FunctionNotDefinedError(name, position)

    def get_variable(self, name, position=None):
        if name in self.current_scope.local_variables:
            return self.current_scope.local_variables[name]
        elif name in self.global_variables:
            return self.global_variables[name]
        raise UndefinedVariableError(name, position)

    def check_type(self, expected_type, value, position):
        if type(value) == expected_type:
            return True
        try:
            if expected_type[0] == 'list':
                expected_type[1].accept(self, self)
                if type(value[0]) == self.last_value:
                    return True
            elif expected_type[0] == "pair":
                expected_type[1].accept(self, self)
                type_1 = self.last_value
                expected_type[2].accept(self, self)
                type_2 = self.last_value
                if type(value[0]) == type_1 and type(value[1]) == type_2:
                    return True
            elif expected_type[0] == "dict":
                for pair in value.items():
                    expected_type[1].accept(self, self)
                    type_1 = self.last_value
                    if type(pair[0]) != type_1:
                        raise WrongTypeError(type_1.__name__, type(pair[0]).__name__, position)
                    expected_type[2].accept(self, self)
                    type_2 = self.last_value
                    if type(pair[1]) != type_2:
                        raise WrongTypeError(type_2.__name__, type(pair[1]).__name__, position)
                return True
        except TypeError:
            raise WrongTypeError(expected_type, type(value), position)
        raise WrongTypeError(expected_type, value, position)
