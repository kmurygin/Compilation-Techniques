from src.lexer.lexer import Lexer
from src.token.token_types import TokenType
from src.token.token import Token

from src.ast.nodes import *

VARIABLE_TYPES = [TokenType.INT_KEYWORD, TokenType.FLOAT_KEYWORD, TokenType.STRING_KEYWORD, TokenType.LIST,
                  TokenType.DICT, TokenType.LIST, TokenType.BOOL_KEYWORD]

RELATIONSHIP_TYPES = [TokenType.LESS_SIGN, TokenType.LESS_OR_EQUAL_SIGN, TokenType.GREATER_SIGN, TokenType.GREATER_OR_EQUAL_SIGN, TokenType.EQUAL_SIGN, TokenType.NOT_EQUAL_SIGN]


class Parser:
    def __init__(self, reader, lexer: Lexer):
        self.reader = reader
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def check_token_type(self, token_type):
        return self.current_token.get_type() == token_type

    def consume(self):
        old_token = self.current_token
        new_token = self.lexer.get_next_token()
        self.current_token = new_token
        return old_token

    def require_and_consume(self, token_type):
        self.require_token(token_type)
        return self.consume()

    def require_token(self, token_type):
        if self.current_token.get_type() == token_type:
            return self.current_token
        # raise SyntaxError(token_type)

    def parse(self):
        program = []
        while self.current_token.get_type() != TokenType.EOF:
            function = self.parse_function()
            program.append(function)
        return program

    def parse_function(self) -> Function:
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.FUNCTION)
        type = self.parse_type()
        identifier = self.parse_identifier()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        arguments = self.parse_arguments()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        body = self.parse_function_body()
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return Function(type, identifier, arguments, body, line, column)

    def parse_function_body(self) -> FunctionBody:
        line, column = self.current_token.get_position()
        content = self.parse_function_body_content()
        return_statement = self.parse_function_body_return()
        return FunctionBody(content, return_statement, line, column)

    def parse_function_body_content(self):
        if self.current_token.get_type() not in [TokenType.RETURN, TokenType.RIGHT_CURLY_BRACKET]:
            return self.parse_content()
        return []

    def parse_function_body_return(self):
        if self.current_token.get_type() == TokenType.RETURN:
            return_statement = self.parse_return()
            self.require_and_consume(TokenType.SEMICOLON)
            return return_statement

    def parse_function_call(self, function_identifier):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        arguments = self.parse_elements(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return FunctionCall(function_identifier, arguments, line, column)

    def parse_elements(self, stop_type):
        elements = []
        while self.current_token.get_type() != stop_type:
            elements.append(self.parse_expression())
            if self.check_token_type(TokenType.COMMA):
                self.consume()
        return elements

    def parse_identifier(self):
        line, column = self.current_token.get_position()
        token = self.require_and_consume(TokenType.ID)
        identifier = Identifier(token.get_value(), line, column)
        return identifier

    def parse_return(self):
        self.require_and_consume(TokenType.RETURN)
        return self.parse_expression()

    def parse_arguments(self):
        line, column = self.current_token.get_position()
        arguments = []
        if self.current_token.get_type() != TokenType.RIGHT_BRACKET:
            while self.current_token.get_type() in VARIABLE_TYPES:
                variable_type = self.parse_type()
                variable_name = self.parse_identifier()
                arguments.append(Variable(variable_type, variable_name, None, line, column))
                if self.current_token.get_type() == TokenType.COMMA:
                    self.consume()
        return arguments

    def parse_content(self):
        end_of_content_token_types = [TokenType.RETURN, TokenType.RIGHT_CURLY_BRACKET]
        lines = []

        while self.current_token.get_type() not in end_of_content_token_types:
            line = self.parse_line()
            lines.append(line)

        return lines

    def parse_expression(self):
        line, column = self.current_token.get_position()
        factor = self.parse_multiplication()

        if type(factor) == Identifier:
            if self.check_token_type(TokenType.ASSIGN):
                operator = self.consume().get_value()
                new_factor = self.parse_expression()
                return Expression(factor, operator, new_factor, line, column)

        for sign in RELATIONSHIP_TYPES:
            if self.check_token_type(sign):
                operator = self.consume().get_value()
                new_factor = self.parse_expression()
                return Expression(factor, operator, new_factor, line, column)

        while self.check_token_type(TokenType.ADD_SIGN) or self.check_token_type(TokenType.SUB_SIGN):
            operator = self.consume()
            new_factor = self.parse_multiplication()
            factor = Expression(factor, operator.get_value(), new_factor, line, column)
        return factor

    def parse_multiplication(self):
        line, column = self.current_token.get_position()
        factor = self.parse_factor()
        while self.check_token_type(TokenType.MULTIPLY_SIGN) or self.check_token_type(TokenType.DIVIDE_SIGN):
            operator = self.consume().get_value()
            new_factor = self.parse_factor()
            factor = Expression(factor, operator, new_factor, line, column)
        return factor

    def parse_factor(self):
        if self.check_token_type(TokenType.LEFT_BRACKET):
            self.require_and_consume(TokenType.LEFT_BRACKET)
            factor = self.parse_expression()
            self.require_and_consume(TokenType.LEFT_BRACKET)
        else:
            factor = self.parse_component()
        return factor

    def parse_component(self):
        if self.current_token.get_value() == "-":
            line, column = self.current_token.get_position()
            self.consume()
            return_statement = self.parse_component_without_minus()
            return Expression(IntValue(0), "-", return_statement, line, column)
        else:
            return self.parse_component_without_minus()

    def parse_component_without_minus(self):
        if self.check_token_type(TokenType.BOOL_VALUE):
            return self.parse_bool()
        elif self.check_token_type(TokenType.INT_VALUE):
            return self.parse_int()
        elif self.check_token_type(TokenType.FLOAT_VALUE):
            return self.parse_float()
        elif self.check_token_type(TokenType.STRING_VALUE):
            return self.parse_string()
        elif self.check_token_type(TokenType.ID):
            identifier = self.parse_identifier()
            if self.check_token_type(TokenType.LEFT_BRACKET):
                return self.parse_function_call(identifier)
            else:
                return identifier

    def parse_bool(self):
        token = self.require_and_consume(TokenType.BOOL_VALUE)
        return BoolValue(token.get_value(), token.get_line(), token.get_column())

    def parse_string(self):
        token = self.require_and_consume(TokenType.STRING_VALUE)
        return StringValue(token.get_value(), token.get_line(), token.get_column())

    def parse_int(self):
        token = self.require_and_consume(TokenType.INT_VALUE)
        return IntValue(token.get_value(), token.get_line(), token.get_column())

    def parse_float(self):
        token = self.require_and_consume(TokenType.FLOAT_VALUE)
        return FloatValue(token.get_value(), token.get_line(), token.get_column())

    def parse_line(self):
        if self.current_token.get_type() == TokenType.PRINT:
            line = self.parse_print()
        elif self.current_token.get_type() in VARIABLE_TYPES:
            line = self.parse_declaration()
        else:
            line = self.parse_expression()
        self.require_and_consume(TokenType.SEMICOLON)
        return line

    def parse_print(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.PRINT)
        value = self.parse_expression()
        return PrintFunction(value, line, column)

    def parse_declaration(self):
        line, column = self.current_token.get_position()
        variable_type = self.parse_type()
        variable_identifier = self.parse_identifier()
        value = None

        if self.check_token_type(TokenType.ASSIGN):
            self.require_and_consume(TokenType.ASSIGN)
            value = self.parse_expression()

        declaration = Variable(variable_type, variable_identifier, value, line, column)

        return declaration

    def parse_type(self):
        for token_type in VARIABLE_TYPES:
            if token_type == self.current_token.get_type():
                token = self.current_token
                self.consume()
                return token.get_value()

        required_types = []
        for single_type in VARIABLE_TYPES:
            required_types.append(single_type.name)

        raise SyntaxError(VARIABLE_TYPES)

    def parse_list(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LEFT_SQUARE_BRACKET)
        elements = self.parse_elements(TokenType.RIGHT_SQUARE_BRACKET)
        self.require_and_consume(TokenType.RIGHT_SQUARE_BRACKET)
        return List(elements, line, column)

    def parse_pair(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LEFT_SQUARE_BRACKET)

        elements = list()
        for _ in range(2):
            elements.append(self.parse_expression())
            if self.check_token_type(TokenType.COMMA):
                self.consume()

        self.require_and_consume(TokenType.RIGHT_SQUARE_BRACKET)
        return Pair(elements[0], elements[1], line, column)

    def parse_dict(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        pairs = []
        while self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            pair = list()
            pair.append(self.parse_expression())
            if self.check_token_type(TokenType.COLON):
                self.consume()
            pair.append(self.parse_expression())

            if self.check_token_type(TokenType.COMMA):
                self.consume()
            pairs.append(Pair(pair[0], pair[1], line, column))
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return Dict(pairs, line, column)

    def parse_collection_operation(self, tmp_list):
        self.require_and_consume(TokenType.DOT)
        if self.check_token_type(TokenType.REMOVE):
            return self.parse_operation_remove(tmp_list)
        elif self.check_token_type(TokenType.AT):
            return self.parse_operation_at(tmp_list)
        elif self.check_token_type(TokenType.GET):
            return self.parse_operation_get(tmp_list)
        elif self.check_token_type(TokenType.LENGTH):
            return self.parse_operation_length(tmp_list)
        elif self.check_token_type(TokenType.APPEND):
            return self.parse_operation_append(tmp_list)
        elif self.check_token_type(TokenType.TYPE):
            return self.parse_operation_type(tmp_list)

    def parse_operation_remove(self, tmp_list):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.DELETE)
        self.require_and_consume(TokenType.LEFT_BRACKET)

        argument = self.parse_expression()

        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Remove(tmp_list, argument, line, column)

    def parse_operation_length(self, tmp_list):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LENGTH)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Length(tmp_list, line, column)

    def parse_operation_type(self, tmp_list):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.TYPE)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Type(tmp_list, line, column)

    def parse_operation_append(self, tmp_list):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.DELETE)
        self.require_and_consume(TokenType.LEFT_BRACKET)

        argument = self.parse_expression()

        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Append(tmp_list, argument, line, column)

    def parse_operation_at(self, tmp_list):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.DELETE)
        self.require_and_consume(TokenType.LEFT_BRACKET)

        argument = self.parse_expression()

        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return At(tmp_list, argument, line, column)

    def parse_operation_get(self, dict):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.DELETE)
        self.require_and_consume(TokenType.LEFT_BRACKET)

        argument = self.parse_expression()

        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Append(dict, argument, line, column)

    def parse_linq(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.FROM)
        from_type = self.parse_type()
        from_id = self.parse_identifier()
        self.require_and_consume(TokenType.IN)
        from_in = self.parse_identifier()
        self.require_and_consume(TokenType.WHERE)
        where = self.parse_expression()
        self.require_and_consume(TokenType.SELECT)
        select = self.parse_expression()
        self.require_and_consume(TokenType.ORDER_BY)
        orderby = self.parse_expression()
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)

        from_statement = [from_type, from_id, from_in]

        return LINQ(from_statement, where, select, orderby, line, column)

    def parse_if(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.IF)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        condition = self.parse_expression()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            content = self.parse_content()
        else:
            content = []
        true_statement = Body(content)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        self.require_and_consume(TokenType.ELSE)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            content = self.parse_content()
        else:
            content = []
        false_statement = Body(content)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return IfStatement(condition, true_statement, false_statement, line, column)

    def parse_for(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.FOR)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        type = self.parse_type()
        var = self.parse_identifier()
        self.require_and_consume(TokenType.IN)
        collection = self.parse_identifier()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            content = self.parse_content()
        else:
            content = []
        content = Body(content)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return ForStatement(type, var, collection, content, line, column)

    def parse_while(self):
        pass
