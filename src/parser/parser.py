from google.protobuf.internal.well_known_types import ListValue
from torch._C._jit_tree_views import StringLiteral

from src.lexer.lexer import Lexer
from src.token.token_types import TokenType
from src.token.token import Token

from src.ast.nodes import *

VARIABLE_TYPES = [TokenType.INT_KEYWORD, TokenType.FLOAT_KEYWORD, TokenType.STRING_KEYWORD, TokenType.LIST,
                  TokenType.DICT, TokenType.LIST, TokenType.BOOL_KEYWORD]

LITERAL_TYPES = {
    TokenType.STRING_VALUE: StringValue,
    TokenType.INT_VALUE: IntValue,
    TokenType.FLOAT_VALUE: FloatValue,
    TokenType.BOOL_VALUE: BoolValue,
    TokenType.LIST: List,
    TokenType.DICT: Dict,
    TokenType.PAIR: Pair,
}

RELATION_SIGNS = {
    TokenType.LESS_SIGN: LessThanExpression,
    TokenType.GREATER_SIGN: GreaterThanExpression,
    TokenType.EQUAL_SIGN: EqualExpression,
    TokenType.NOT_EQUAL_SIGN: NotEqualExpression,
    TokenType.LESS_OR_EQUAL_SIGN: LessThanOrEqualExpression,
    TokenType.GREATER_OR_EQUAL_SIGN: GreaterThanOrEqualExpression
}

ADDITIVE_SIGNS = {
    TokenType.ADD_SIGN: AddExpression,
    TokenType.SUB_SIGN: SubExpression
}

MULTIPLICATIVE_SIGNS = {
    TokenType.MULTIPLY_SIGN: MultiplyExpression,
    TokenType.DIVIDE_SIGN: DivisionExpression
}


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
        program = Program()
        while self.current_token.get_type() != TokenType.EOF:
            function = self.parse_function_declaration()
            program.add_function(function)
        return program

    def parse_function_declaration(self) -> Function:
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.FUNCTION)
        function_type = self.parse_type()
        identifier = self.parse_identifier()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        params = self.parse_function_params()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        body = self.parse_statement_block()
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return Function(function_type, identifier, params, body, line, column)

    def parse_function_params(self):
        line, column = self.current_token.get_position()
        params = []
        while self.current_token.get_type() in VARIABLE_TYPES:
            variable_type = self.parse_type()
            variable_name = self.parse_identifier()
            params.append((variable_type, variable_name))
            if self.current_token.get_type() == TokenType.COMMA:
                self.consume()
        return params

    def parse_function_call(self):
        line, column = self.current_token.get_position()
        identifier = self.parse_identifier()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        arguments = self.parse_arguments()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return FunctionCall(identifier, arguments, line, column)

    def parse_arguments(self):
        line, column = self.current_token.get_position()
        arguments = []
        while self.current_token.get_type() != TokenType.LEFT_BRACKET:
            argument = self.parse_expression()
            self.require_and_consume(TokenType.COMMA)
        return arguments

    def parse_statement_block(self):
        statements = []
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        while self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            statements.append(self.parse_single_statement())
            self.require_and_consume(TokenType.SEMICOLON)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return StatementBlock(statements, line, column)

    def parse_single_statement(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() == TokenType.FOR:
            self.parse_for()
        elif self.current_token.get_type() == TokenType.IF:
            self.parse_if()
        elif self.current_token.get_type() == TokenType.WHILE:
            self.parse_while()
        elif self.current_token.get_type() == TokenType.RETURN:
            self.parse_return()
        elif self.current_token.get_type() == TokenType.ID:
            self.parse_function_call()
        elif self.current_token.get_type() == TokenType.RETURN:
            self.parse_return()
            # self.parse_method_call()
            # self.parse_assignment()

    def parse_elements(self, stop_type):
        elements = []
        while self.current_token.get_type() != stop_type:
            elements.append(self.parse_expression())
            if self.check_token_type(TokenType.COMMA):
                self.consume()
        return elements

    def parse_identifier(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.ID:
            return None
        token = self.require_and_consume(TokenType.ID)
        identifier = Identifier(token.get_value(), line, column)
        return identifier

    def parse_return(self):
        self.require_and_consume(TokenType.RETURN)
        return self.parse_expression()

    def parse_content(self):
        end_of_content_token_types = [TokenType.RETURN, TokenType.RIGHT_CURLY_BRACKET]
        lines = []

        while self.current_token.get_type() not in end_of_content_token_types:
            line = self.parse_line()
            lines.append(line)

        return lines

    def parse_expression(self):
        result = self.parse_and_expression()
        if not result:
            return None
        while self.current_token.get_type() == TokenType.OR_SIGN:
            self.require_and_consume(TokenType.OR_SIGN)
            result = OrExpression(result, self.parse_expression())
        return result

    def parse_and_expression(self):
        result = self.parse_relation_expression()
        if not result:
            return None
        while self.current_token.get_type() == TokenType.AND_SIGN:
            self.require_and_consume(TokenType.AND_SIGN)
            result = AndExpression(result, self.parse_and_expression())
        return result

    def parse_relation_expression(self):
        result = self.parse_sum_expression()
        if not result:
            return None
        if self.current_token.get_type() in RELATION_SIGNS.keys():
            constructor = RELATION_SIGNS[self.current_token.get_type()]
            line, column = self.current_token.get_position()
            result = constructor(result, self.parse_sum_expression(), line, column)
        return result

    def parse_sum_expression(self):
        result = self.parse_multiply_expression()
        if not result:
            return None
        while self.current_token.get_type() in ADDITIVE_SIGNS.keys():
            constructor = ADDITIVE_SIGNS[self.current_token.get_type()]
            line, column = self.current_token.get_position()
            self.consume()
            result = constructor(result, self.parse_multiply_expression(), line, column)
        return result

    def parse_multiply_expression(self):
        result = self.parse_factor()
        if not result:
            return None
        while self.current_token.get_type() in MULTIPLICATIVE_SIGNS.keys():
            constructor = MULTIPLICATIVE_SIGNS[self.current_token.get_type()]
            line, column = self.current_token.get_position()
            self.consume()
            result = constructor(result, self.parse_factor(), line, column)
        return result

    def parse_factor(self):
        return (
            self.parse_identifier() or
            # self.parse_function_call() or
            self.parse_literal()
        )

    def parse_literal(self):
        if self.current_token.get_type() not in LITERAL_TYPES.keys():
            return None
        constructor = LITERAL_TYPES[self.current_token.get_type()]
        line, column = self.current_token.get_position()
        result = constructor(self.current_token.get_value(), line, column)
        self.consume()
        return result
    #
    # def multiply_expression(self):
    #     result = self.factor()
    #     while self.current_token.type in ('MUL', 'DIV'):
    #         operator = self.current_token.type
    #         self.eat(operator)
    #         result = (operator, result, self.multiply_expression())
    #     return result
    #
    # def factor(self):
    #     token = self.current_token
    #     if token.type == 'NUMBER':
    #         self.eat('NUMBER')
    #         return ('NUM', token.value)
    #     elif token.type == 'LPAREN':
    #         self.eat('LPAREN')
    #         result = self.expression()
    #         self.eat('RPAREN')
    #         return result
    #     else:
    #         raise Exception(f'Unexpected token: {token.type}')
    # def parse_bool(self):
    #     token = self.require_and_consume(TokenType.BOOL_VALUE)
    #     return BoolValue(token.get_value(), token.get_line(), token.get_column())
    #
    # def parse_string(self):
    #     token = self.require_and_consume(TokenType.STRING_VALUE)
    #     return StringValue(token.get_value(), token.get_line(), token.get_column())
    #
    # def parse_int(self):
    #     token = self.require_and_consume(TokenType.INT_VALUE)
    #     return IntValue(token.get_value(), token.get_line(), token.get_column())
    #
    # def parse_float(self):
    #     token = self.require_and_consume(TokenType.FLOAT_VALUE)
    #     return FloatValue(token.get_value(), token.get_line(), token.get_column())

    # def parse_declaration(self):
    #     line, column = self.current_token.get_position()
    #     variable_type = self.parse_type()
    #     variable_identifier = self.parse_identifier()
    #     value = None
    #
    #     if self.check_token_type(TokenType.ASSIGN):
    #         self.require_and_consume(TokenType.ASSIGN)
    #         value = self.parse_expression()
    #
    #     declaration = Variable(variable_type, variable_identifier, value, line, column)
    #
    #     return declaration

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
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.WHILE)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        condition = self.parse_expression()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        body = self.parse_content() # ??????????
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return WhileStatement(condition, body, line, column)
