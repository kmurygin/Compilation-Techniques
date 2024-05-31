from src.lexer.lexer import Lexer
from src.token.token_types import TokenType
from src.token.token import Token

from src.ast.nodes import *
from src.exceptions.parser_exception import *

VARIABLE_TYPES = [
    TokenType.INT_KEYWORD,
    TokenType.FLOAT_KEYWORD,
    TokenType.STRING_KEYWORD,
    TokenType.BOOL_KEYWORD
]

CONTAINER_TYPES = [
    TokenType.PAIR,
    TokenType.DICT,
    TokenType.LIST,
]

LITERAL_TYPES = {
    TokenType.STRING_VALUE: StringValue,
    TokenType.INT_VALUE: IntValue,
    TokenType.FLOAT_VALUE: FloatValue,
    TokenType.BOOL_VALUE: BoolValue,
    # TokenType.LIST: List,
    # TokenType.DICT: Dict,
    # TokenType.PAIR: Pair,
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
        elif token_type == TokenType.RIGHT_BRACKET:
            raise NoClosingBracketError(self.current_token.get_position())
        elif token_type == TokenType.RIGHT_CURLY_BRACKET:
            raise NoClosingCurlyBracketError(self.current_token.get_position())
        elif token_type == TokenType.SEMICOLON:
            raise NoSemicolonError(self.current_token.get_position())
        raise SyntaxError(f"We have {self.current_token.get_type()} but we want  {token_type}")

    def parse(self):
        program = Program()
        while self.current_token.get_type() != TokenType.EOF:
            function = self.parse_function_declaration()
            program.add_function(function)
        return program

    def parse_function_declaration(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.FUNCTION:
            return None
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
        while self.current_token.get_type() in VARIABLE_TYPES or self.current_token.get_type() in CONTAINER_TYPES:
            variable_type = self.parse_type()
            variable_name = self.parse_identifier()
            params.append((variable_type, variable_name))
            if self.current_token.get_type() == TokenType.COMMA:
                self.consume()
        return params

    def parse_function_call(self, identifier=None):
        line, column = self.current_token.get_position()
        if not identifier:
            identifier = self.parse_identifier()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        arguments = self.parse_arguments()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return FunctionCall(identifier, arguments, line, column)

    def parse_method_call(self):
        line, column = self.current_token.get_position()
        # if not identifier:
        #     identifier = self.parse_identifier()
        expression = self.parse_expression()
        self.require_and_consume(TokenType.DOT)
        method_name = self.parse_identifier()
        self.require_and_consume(TokenType.LEFT_BRACKET)
        arguments = self.parse_arguments()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return MethodCall(expression, method_name, arguments, line, column)

    def parse_arguments(self):
        line, column = self.current_token.get_position()
        arguments = [self.parse_expression()]
        while self.current_token.get_type() != TokenType.RIGHT_BRACKET:
            self.require_and_consume(TokenType.COMMA)
            argument = self.parse_expression()
            # self.consume()
            arguments.append(argument)
        return Arguments(arguments, line, column)

    def parse_statement_block(self):
        statements = []
        line, column = self.current_token.get_position()
        while self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            statements.append(self.parse_single_statement())
            self.require_and_consume(TokenType.SEMICOLON)
        return StatementBlock(statements, line, column)

    # def parse_statement_block(self):
    #     statements = []
    #     line, column = self.current_token.get_position()
    #     while self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
    #         next_statement = self.parse_single_statement()
    #         if next_statement is None:
    #             if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
    #                 raise NoClosingCurlyBracketError((line, column))
    #         statements.append(next_statement)
    #         if self.current_token.get_type() != TokenType.SEMICOLON:
    #             raise NoSemicolonError((line, column))
    #         self.require_and_consume(TokenType.SEMICOLON)
    #     return StatementBlock(statements, line, column)

    def parse_single_statement(self):
        line, column = self.current_token.get_position()
        result = (
                self.parse_for() or
                self.parse_if() or
                self.parse_while() or
                self.parse_return() or
                self.parse_function_declaration() or
                self.parse_init_statement() or
                self.parse_expression()
        )
        return result

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
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.IF:
            return None
        self.require_and_consume(TokenType.RETURN)
        expression = self.parse_expression()
        return ReturnStatement(expression, line, column)

    def parse_assignment(self):
        line, column = self.current_token.get_position()
        identifier = self.parse_identifier()
        self.require_and_consume(TokenType.ASSIGN)
        expression = self.parse_expression()
        return Assignment(identifier, expression, line, column)

    def parse_init_statement(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() not in VARIABLE_TYPES and self.current_token.get_type() not in CONTAINER_TYPES:
            return None
        type = self.parse_type()
        identifier = self.parse_identifier()
        if self.current_token.get_type() == TokenType.ASSIGN:
            self.require_and_consume(TokenType.ASSIGN)
            expression = self.parse_expression()
            return InitStatement(type, identifier, expression, line, column)
        return Declaration(type, identifier, line, column)

    def parse_expression(self):
        result = self.parse_and_expression()
        line, column = self.current_token.get_position()
        if not result:
            return None
        while self.current_token.get_type() == TokenType.OR_SIGN:
            self.require_and_consume(TokenType.OR_SIGN)
            result = OrExpression(result, self.parse_expression())
        if self.current_token.get_type() == TokenType.DOT:
            self.require_and_consume(TokenType.DOT)
            method_name = self.parse_identifier()
            self.require_and_consume(TokenType.LEFT_BRACKET)
            arguments = self.parse_arguments()
            self.require_and_consume(TokenType.RIGHT_BRACKET)
            return MethodCall(result, method_name, arguments, line, column)
        if isinstance(result, Identifier):
            if self.current_token.get_type() == TokenType.LEFT_BRACKET:
                self.require_and_consume(TokenType.LEFT_BRACKET)
                arguments = self.parse_arguments()
                self.require_and_consume(TokenType.RIGHT_BRACKET)
                return FunctionCall(result, arguments, line, column)

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
                # self.parse_method_call() or
                self.parse_literal() or
                self.parse_list() or
                self.parse_pair() or
                self.parse_dict()
        )

    # def parse_identifier_or_function_method_call(self):
    #     line, column = self.current_token.get_position()
    #     identifier = self.parse_identifier()
    #     if self.current_token.get_type() == TokenType.DOT:
    #         self.parse

    def parse_literal(self):
        if self.current_token.get_type() not in LITERAL_TYPES.keys():
            return None
        constructor = LITERAL_TYPES[self.current_token.get_type()]
        line, column = self.current_token.get_position()
        result = constructor(self.current_token.get_value(), line, column)
        self.consume()
        return result

    def parse_type(self):
        for token_type in VARIABLE_TYPES:
            if token_type == self.current_token.get_type():
                token = self.current_token
                self.consume()
                return token.get_value()
        for token_type in CONTAINER_TYPES:
            if token_type == self.current_token.get_type():
                return self.parse_container_type()
        # required_types = []
        # for single_type in VARIABLE_TYPES:
        #     required_types.append(single_type.name)

        # raise TypeNotSupportedError(self.current_token.get_type())

    def parse_container_type(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() == TokenType.DICT:
            type_container = self.parse_dict_type()
        elif self.current_token.get_type() == TokenType.LIST:
            type_container = self.parse_list_type()
        elif self.current_token.get_type() == TokenType.PAIR:
            type_container = self.parse_pair_type()
        else:
            return None
        # type_container = self.current_token.get_value()
        # self.require_and_consume(TokenType.LESS_SIGN)
        # type = self.parse_type()
        # self.require_and_consume(TokenType.GREATER_SIGN)
        return type_container

    def parse_list_type(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.LIST)
        self.require_and_consume(TokenType.LESS_SIGN)
        list_type = self.parse_type()
        self.require_and_consume(TokenType.GREATER_SIGN)
        return ListType(list_type, line, column)

    def parse_pair_type(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.PAIR)
        self.require_and_consume(TokenType.LESS_SIGN)
        first_type = self.parse_type()
        self.require_and_consume(TokenType.COMMA)
        second_type = self.parse_type()
        self.require_and_consume(TokenType.GREATER_SIGN)
        return PairType(first_type, second_type, line, column)

    def parse_dict_type(self):
        line, column = self.current_token.get_position()
        self.require_and_consume(TokenType.DICT)
        self.require_and_consume(TokenType.LESS_SIGN)
        key_type = self.parse_type()
        self.require_and_consume(TokenType.COMMA)
        value_type = self.parse_type()
        self.require_and_consume(TokenType.GREATER_SIGN)
        return DictType(key_type, value_type, line, column)

    def parse_list(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.LEFT_SQUARE_BRACKET:
            return None
        self.require_and_consume(TokenType.LEFT_SQUARE_BRACKET)
        elements = self.parse_elements(TokenType.RIGHT_SQUARE_BRACKET)
        self.require_and_consume(TokenType.RIGHT_SQUARE_BRACKET)
        return List(elements, line, column)

    def parse_pair(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.LEFT_BRACKET:
            return None
        self.require_and_consume(TokenType.LEFT_BRACKET)
        elements = list()
        for _ in range(2):
            elements.append(self.parse_expression())
            if self.check_token_type(TokenType.COMMA):
                self.consume()

        self.require_and_consume(TokenType.RIGHT_BRACKET)
        return Pair(elements[0], elements[1], line, column)

    def parse_dict(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.LEFT_CURLY_BRACKET:
            return None
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
        if self.current_token.get_type() != TokenType.IF:
            return None
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
        key_function = None
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.FOR:
            return None
        self.require_and_consume(TokenType.FOR)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        type = self.parse_type()
        var = self.parse_identifier()
        self.require_and_consume(TokenType.IN)
        collection = self.parse_identifier()
        if self.current_token.get_type() == TokenType.COMMA:
            self.require_and_consume(TokenType.COMMA)
            self.require_and_consume(TokenType.KEY)
            self.require_and_consume(TokenType.ASSIGN)
            key_function = self.parse_identifier()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            content = self.parse_statement_block()
        else:
            content = []
        content = Body(content)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)

        if key_function is None:
            return ForStatement(type, var, collection, content, line, column)
        else:
            return ForSortedStatement(type, var, collection, key_function, content, line, column)

    def parse_while(self):
        line, column = self.current_token.get_position()
        if self.current_token.get_type() != TokenType.WHILE:
            return None
        self.require_and_consume(TokenType.WHILE)
        self.require_and_consume(TokenType.LEFT_BRACKET)
        condition = self.parse_expression()
        self.require_and_consume(TokenType.RIGHT_BRACKET)
        self.require_and_consume(TokenType.LEFT_CURLY_BRACKET)
        if self.current_token.get_type() != TokenType.RIGHT_CURLY_BRACKET:
            content = self.parse_statement_block()
        else:
            content = []
        content = Body(content)
        self.require_and_consume(TokenType.RIGHT_CURLY_BRACKET)
        return WhileStatement(condition, content, line, column)
