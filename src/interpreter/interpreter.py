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
    list.remove(arguments[0])
    return list


def at(list, arguments=None):
    return list[arguments[0]]


def get_type(list, arguments=None):
    return type(list[0])


def get_print(arguments):
    print(f"Arguments::::::{arguments}")
    print(argument[1] for argument in arguments)


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
}


class Interpreter:
    def __init__(self, program):
        self.global_variables = {}
        self.function_definitions = {}
        self.scopes_stack = []
        self.current_scope = None
        self.program = program
        self.visit_program()
        self.last_value = None

    def visit_program(self):
        for declaration in self.program.program_body:
            declaration.accept(self)

        self.current_scope = Scope(
            self.function_definitions['main'],
            (0, 0),
            []
        )
# visit program uruchamia maina
    def run_main_function(self):
        main_function = self.function_definitions['main']
        main_function_call = FunctionCall(Identifier('main'), Arguments([]), 0, 0)
        return main_function_call.accept(self)

    def visit_declaration(self, declaration, global_declaration):
        if global_declaration:
            scope = self.global_variables
        else:
            scope = self.current_scope.local_variables

        scope[declaration.identifier] = None

    def visit_identifier(self, identifier):
        return identifier.value

    def visit_init_statement(self, init_statement, global_declaration):
        if global_declaration:
            scope = self.global_variables
        else:
            scope = self.current_scope.local_variables

        value = init_statement.expression.accept(self)
        type = init_statement.type.accept(self) #tutaj
        self.check_type(type, value, (init_statement.line, init_statement.column))

        scope[init_statement.identifier.accept(self)] = (type, value)

    def visit_function_definition(self, function_definition):
        function_identifier = function_definition.identifier.accept(self)
        if function_identifier in self.function_definitions:
            raise FunctionAlreadyDefinedError(function_identifier)
        self.function_definitions[function_identifier] = function_definition

    def visit_bool_value(self, bool_value):
        return bool_value.value

    def visit_int_value(self, int_value):
        return int_value.value

    def visit_float_value(self, float_value):
        return float_value.value

    def visit_string_value(self, string_value):
        return string_value.value

    def visit_boolean_value(self, boolean_value):
        return boolean_value.value

    def visit_variable(self, variable):
        value = self.get_variable(variable.name.accept(self), (variable.line, variable.column))
        return value

    def visit_function_call(self, function_call):
        function_id = function_call.identifier.accept(self)
        # if function_id in BUILTIN_FUNCTIONS.keys:
        #     function = BUILTIN_FUNCTIONS[function_id]
        #     function(function_call.arguments)
        # slownika zawiera funckje uzytkownikani wbudowane
        # drugi slownik z lambda dla funkcji wbudowanych
        if function_id == "print":
            # print(*function_call.arguments.accept(self))
            lista = [argument for argument in function_call.arguments.accept(self)]
            print(*lista)
        elif function_id == "int":
            pass
        elif function_id == "string":
            pass
        else:
            function_definition = self.get_function_definition(function_id, function_call.position)
            new_scope = Scope(
                function_definition,
                function_call.position,
                function_call.arguments.accept(self)
            )
            self.scopes_stack.append(self.current_scope)
            if len(self.scopes_stack) == 10:
                raise ValueError()
            self.current_scope = new_scope
            return function_definition.body.accept(self)
#czy typy w metodzie sie zgadzaja
    def visit_method_call(self, method_call):
        method_expression = method_call.expression.accept(self)
        method_id = method_call.method_identifier.accept(self)
        method_arguments = method_call.arguments.accept(self)
        method_body = BUILTIN_METHODS[method_id]

        variable_name = self.get_variable(method_expression)
        if variable_name is not None:
            method_expression = variable_name
        return method_body(method_expression, method_arguments)
# self.last_value = ..
# jezeli return przerwij wywolanie bloku
    def visit_statement_block(self, statement_block):
        for statement in statement_block.statements:
            return_value = statement.accept(self)
            if return_value is not None:
                return return_value
        return None

    def visit_arguments(self, arguments):
        if len(arguments.arguments) > 0:
            return [exp.accept(self) for exp in arguments.arguments]
        else:
            return []

    def visit_linq(self, linq):
        result = []
        from_statement = linq.from_statement
        # from_type = from_statement[0]
        from_id = from_statement[1].accept(self)
        data = self.get_variable(from_statement[2].accept(self))
        all_pairs = list(data[1].items())
        for pair in all_pairs:
            new_scope = Scope()
            new_scope.local_variables[from_id] = (None, pair)
            self.scopes_stack.append(self.current_scope)
            self.current_scope = new_scope
            # where

            if linq.where_statement.accept(self):
                # select
                result.append(linq.select_statement.accept(self))

            frame = self.scopes_stack.pop()
            self.current_scope = frame
        # select

        # orderby

        # orderby_statement = linq.orderby_statement.accept(self)
        return result

    def visit_assignment(self, assignment):

        variable_id = assignment.identifier.accept(self)
        type, variable = self.get_variable(variable_id, assignment.position)
        value = assignment.expression.accept(self)

        self.check_type(type, value[1], assignment.position)
        self.current_scope.local_variables[variable_id] = value

    def visit_if_statement(self, if_statement):
        condition = if_statement.condition.accept(self)
        self.check_type(bool, condition, if_statement.position)
        if condition:
            return if_statement.true_statement.accept(self)
        else:
            return if_statement.false_statement.accept(self)

    def visit_while_statement(self, while_statement):
        condition = while_statement.condition.accept(self)
        self.check_type(bool, condition, while_statement.position)
        i = 0

        while condition:
            # scope dla bloku
            return_value = while_statement.body.accept(self)
            if return_value:
                return return_value
            if i == 100:
                raise ValueError()

            condition = while_statement.condition.accept(self)
            i += 1

# nie rob osobnych scopw, ale przypisz nowe a w kolejnej iteracji
    def visit_for_statement(self, for_statement):
        # type = for_statement.type.accept(self)
        identifier = for_statement.identifier.accept(self)
        collection = for_statement.collection.accept(self)
        collection = self.get_variable(collection)
        for element in collection:
            new_frame = Scope()
            new_frame.local_variables[identifier] = element
            self.scopes_stack.append(self.current_scope)
            self.current_scope = new_frame
            # where
            for_statement.body.accept(self)

            frame = self.scopes_stack.pop()
            self.current_scope = frame


    def visit_return_statement(self, return_statement):
        return_value = return_statement.expression.accept(self)
        if self.current_scope.return_value_type in (IntType, BoolType, StringType, FloatType):
            if self.current_scope.return_value_type.accept(self, self) == type(return_value):
                scope = self.scopes_stack.pop()
                self.current_scope = scope
                return return_value
        elif self.current_scope.return_value_type.accept(self) == return_value[0]:
            scope = self.scopes_stack.pop()
            self.current_scope = scope
            return return_value
        try:
            raise WrongTypeReturnError(self.current_scope.return_value_type.accept(self)[1].__name__, type(return_value[1][0]).__name__, return_statement.position)
        except Exception:
            raise WrongTypeReturnError(self.current_scope.return_value_type, type(return_value), return_statement.position)

    def visit_expression(self, expression):
        pass

# czy prawa i lew bool
    def visit_and_expression(self, and_expression):
        left_result = and_expression.left.accept(self)
        right_result = and_expression.right.accept(self)
        return left_result and right_result

    def visit_or_expression(self, or_expression):
        left_result = or_expression.left.accept(self)
        right_result = or_expression.right.accept(self)
        return left_result or right_result

    def visit_add_expression(self, add_expression):
        left_result = add_expression.left.accept(self)
        right_result = add_expression.right.accept(self)
        return left_result + right_result

    def visit_sub_expression(self, sub_expression):
        left_result = sub_expression.left.accept(self)
        right_result = sub_expression.right.accept(self)
        return left_result - right_result

    def visit_multiply_expression(self, multiply_expression):
        left_result = multiply_expression.left.accept(self)
        right_result = multiply_expression.right.accept(self)
        return left_result * right_result

# dzilenie przez 0
    def visit_division_expression(self, division_expression):
        left_result = division_expression.left.accept(self)
        right_result = division_expression.right.accept(self)
        return left_result / right_result

    def visit_less_than_expression(self, less_than_expression):
        left_result = less_than_expression.left.accept(self)
        right_result = less_than_expression.right.accept(self)
        return left_result < right_result

    def visit_greater_than_expression(self, greater_than_expression):
        left_result = greater_than_expression.left.accept(self)
        right_result = greater_than_expression.right.accept(self)
        return left_result > right_result

    def visit_less_than_or_equal_expression(self, less_than_equal_expression):
        left_result = less_than_equal_expression.left.accept(self)
        right_result = less_than_equal_expression.right.accept(self)
        return left_result <= right_result

    def visit_greater_than_equal_expression(self, greater_than_equal_expression):
        left_result = greater_than_equal_expression.left.accept(self)
        right_result = greater_than_equal_expression.right.accept(self)
        return left_result >= right_result

    def visit_list(self, list):
        result = []
        prev_element = list.elements[0].accept(self)
        for element in list.elements:
            next_element = element.accept(self)
            if type(next_element) != type(prev_element):
                raise DifferentTypesListError((element.line, element.column))
            result.append(element.accept(self))
            prev_element = next_element
        return result

    def visit_pair(self, pair):
        return tuple((pair.left.accept(self), pair.right.accept(self)))

    def visit_dict(self, dict):
        result = {}
        for pair in dict.pairs:
            key = pair.left.accept(self)
            value = pair.right.accept(self)
            result[key] = value
        return result

    def visit_list_type(self, list_type):
        return ("list", list_type.type)

    def visit_pair_type(self, pair_type):
        left_type = pair_type.type_1
        right_type = pair_type.type_2
        return ("pair", left_type, right_type)

    def visit_dict_type(self, dict_type):
        left_type = dict_type.key_type
        right_type = dict_type.value_type
        return ("dict", left_type, right_type)

    def visit_int_type(self, int_type):
        return int

    def visit_float_type(self, float_type):
        return float

    def visit_bool_type(self, bool_type):
        return bool

    def visit_string_type(self, string_type):
        return str

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
                if type(value[0]) == expected_type[1].accept(self, self):
                    return True
            elif expected_type[0] == "pair":
                if type(value[0]) == expected_type[1].accept(self, self) and type(value[1]) == expected_type[2].accept(self, self):
                    return True
            elif expected_type[0] == "dict":
                for pair in value.items():
                    if type(pair[0]) != expected_type[1].accept(self, self):
                        raise WrongTypeError(expected_type[1].accept(self, self).__name__, type(pair[0]).__name__, position)
                    if type(pair[1]) != expected_type[2].accept(self, self):
                        raise WrongTypeError(expected_type[2].accept(self, self).__name__, type(pair[1]).__name__, position)
                return True
        except TypeError:
            raise WrongTypeError(expected_type, value, position)
        raise WrongTypeError(expected_type, value, position)
