from .abstract_node import Node


class Program(Node):
    def __init__(self, program_body=None):
        super().__init__()
        if not program_body:
            self.program_body = list()
        else:
            self.program_body = program_body

    def add_function(self, function):
        self.program_body.append(function)

    def __eq__(self, other):
        return (
                isinstance(other, Program)
                and self.program_body == other.program_body
        )

    def __repr__(self):
        return f"[Program: {self.program_body}]"

    def accept(self, visitor):
        return visitor.visit_program(self)


class Variable(Node):
    def __init__(self, name, line=None, column=None):
        super().__init__(line, column)
        self.name = name

    def __eq__(self, other):
        return (
            isinstance(other, Variable)
            and self.name == other.name
        )

    def __repr__(self):
        return f"[Variable: {self.name} {self.line} {self.column}]"

    def accept(self, visitor):
        return visitor.visit_variable(self)


class StatementBlock(Node):
    def __init__(self, statements, line=None, column=None):
        super().__init__()
        self.statements = statements

    def __eq__(self, other):
        return (
                isinstance(other, StatementBlock) and
                self.statements == other.statements
        )

    def __repr__(self):
        return f"[StatementBlock: {self.statements}]"

    def accept(self, visitor):
        return visitor.visit_statement_block(self)


class SingleStatement(Node):
    def __init__(self, statement, line=None, column=None):
        super().__init__()
        self.statement = statement

    def __eq__(self, other):
        return (
                isinstance(other, SingleStatement) and
                self.statement == other.statement
        )

    def __repr__(self):
        return f"[SingleStatement: {self.statement}]"


class BoolValue(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, BoolValue) and
                self.value == other.value
        )

    def __repr__(self):
        return f"[Bool {self.value}]"

    def accept(self, visitor):
        return visitor.visit_bool_value(self)


class IntValue(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, IntValue) and
                self.value == other.value
        )

    def __repr__(self):
        return f"[IntValue: {self.value}]"

    def accept(self, visitor):
        return visitor.visit_int_value(self)


class FloatValue(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, FloatValue) and
                self.value == other.value
        )

    def __repr__(self):
        return f"[FloatValue: {self.value}]"

    def accept(self, visitor):
        return visitor.visit_float_value(self)


class StringValue(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, StringValue) and
                self.value == other.value
        )

    def __repr__(self):
        return f"[StringValue: {self.value}]"

    def accept(self, visitor):
        return visitor.visit_string_value(self)


class Identifier(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, Identifier) and
                self.value == other.value
        )

    def __repr__(self):
        return f"[ID: {self.value}]"

    def accept(self, visitor):
        return visitor.visit_identifier(self)


class Expression(Node):
    def __init__(self, left_operand, operation, right_operand, line=None, column=None):
        super().__init__(line, column)
        self.left_operand = left_operand
        self.operation = operation
        self.right_operand = right_operand

    def __eq__(self, other):
        return (
                isinstance(other, Expression) and
                self.left_operand == other.left_operand and
                self.operation == other.operation and
                self.right_operand == other.right_operand
        )

    def __repr__(self):
        return f"[Expression: {self.left_operand} {self.operation} {self.right_operand}]"

    def accept(self, visitor):
        return visitor.visit_expression(self)


class FunctionBody(Node):
    def __init__(self, content, return_statement, line=None, column=None):
        super().__init__(line, column)
        self.content = content
        self.return_statement = return_statement

    def __eq__(self, other):
        return (
                isinstance(other, FunctionBody) and
                other.content == self.content and
                other.return_statement == self.return_statement
        )

    def __repr__(self):
        return f"[FunctionBody: {self.content} {self.return_statement}]"

    def accept(self, visitor):
        return visitor.visit_function_body(self)


class FunctionCall(Node):
    def __init__(self, identifier, arguments, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.arguments = arguments

    def __eq__(self, other):
        return (
            isinstance(other, FunctionCall) and
            self.identifier == other.identifier and
            self.arguments == other.arguments
        )

    def __repr__(self):
        return f"[FunctionCall: {self.identifier} {self.arguments}]"

    def accept(self, visitor):
        return visitor.visit_function_call(self)


class MethodCall(Node):
    def __init__(self, expression, method_identifier, arguments, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression
        self.method_identifier = method_identifier
        self.arguments = arguments

    def __eq__(self, other):
        return (
            isinstance(other, MethodCall) and
            self.expression == other.expression and
            self.method_identifier == other.method_identifier and
            self.arguments == other.arguments
        )

    def __repr__(self):
        return f"[MethodCall: {self.expression} {self.method_identifier} {self.arguments}]"

    def accept(self, visitor):
        return visitor.visit_method_call(self)


class FunctionDefinition(Node):
    def __init__(self, type, identifier, arguments, body, line=None, column=None):
        super().__init__(line, column)
        self.return_type = type
        self.identifier = identifier
        self.arguments = arguments
        self.body = body

    def __eq__(self, other):
        return (
                isinstance(other, FunctionDefinition) and
                self.return_type == other.return_type and
                self.identifier == other.identifier and
                self.arguments == other.arguments and
                self.body == other.body
        )

    def __repr__(self):
        return f"[Function: {self.return_type} {self.identifier} {self.arguments} {self.body}]"

    def accept(self, visitor):
        return visitor.visit_function_definition(self)


class IfStatement(Node):
    def __init__(self, condition, true_statement, false_statement, line=None, column=None):
        super().__init__(line, column)
        self.condition = condition
        self.true_statement = true_statement
        self.false_statement = false_statement

    def __eq__(self, other):
        return (
                isinstance(other, IfStatement) and
                self.condition == other.condition and
                self.true_statement == other.true_statement and
                self.false_statement == other.false_statement
        )

    def __repr__(self):
        return f"[IF: {self.condition} {self.true_statement} {self.false_statement}]"

    def accept(self, visitor):
        return visitor.visit_if_statement(self)


class Body(Node):
    def __init__(self, content, line=None, column=None):
        super().__init__(line, column)
        self.content = content

    def __eq__(self, other):
        return (
                isinstance(other, Body) and
                other.content == self.content
        )

    def __repr__(self):
        return f"[Body: {self.content}]"

    def accept(self, visitor):
        return visitor.visit_body(self)


class ForStatement(Node):
    def __init__(self, type, identifier, collection, body, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier
        self.collection = collection
        self.body = body

    def __eq__(self, other):
        return (
                isinstance(other, ForStatement) and
                self.type == other.type and
                self.identifier == other.identifier and
                self.collection == other.collection and
                self.body == other.body
        )

    def __repr__(self):
        return f"[For: {self.type} {self.identifier} {self.collection} {self.body}]"

    def accept(self, visitor):
        return visitor.visit_for_statement(self)


class ForSortedStatement(Node):
    def __init__(self, type, identifier, collection, key_identifier, body, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier
        self.collection = collection
        self.body = body
        self.key_identifier = key_identifier

    def __eq__(self, other):
        return (
                isinstance(other, ForSortedStatement) and
                self.type == other.type and
                self.identifier == other.identifier and
                self.collection == other.collection and
                self.body == other.body and
                self.key_identifier == other.key_identifier
        )

    def __repr__(self):
        return f"[ForSorted: {self.type} {self.identifier} {self.collection} {self.key_identifier} {self.body}]"

    def accept(self, visitor):
        return visitor.visit_for_sorted_statement(self)


class WhileStatement(Node):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body

    def __eq__(self, other):
        return (
            isinstance(other, WhileStatement) and
            self.condition == other.condition and
            self.body == other.body
        )

    def __repr__(self):
        return f"[While: {self.condition} {self.body}]"

    def accept(self, visitor):
        return visitor.visit_while_statement(self)


class LINQ(Node):
    def __init__(self, from_statement, where_statement, select_statement, orderby_statement, line=None, column=None):
        super().__init__(line, column)
        self.from_statement = from_statement
        self.where_statement = where_statement
        self.select_statement = select_statement
        self.orderby_statement = orderby_statement

    def __eq__(self, other):
        return (
                isinstance(other, LINQ) and
                other.from_statement == self.from_statement and
                other.where_statement == self.where_statement and
                other.select_statement == self.select_statement and
                other.orderby_statement == self.orderby_statement
        )

    def __repr__(self):
        return f"[LINQ: {self.from_statement} {self.where_statement} {self.select_statement} {self.orderby_statement}]"

    def accept(self, visitor):
        return visitor.visit_linq(self)


class AndExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[AndExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
                isinstance(other, AndExpression) and
                other.left == self.left and
                other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_and_expression(self)


# class RelationExpression(Node):
#     def __init__(self, left_term, right_term, line=None, column=None):
#         super().__init__(line, column)
#         self.left = left_term
#         self.right = right_term
#
#     def __repr__(self):
#         return f"[RelationExpression {self.line} {self.column} ({self.left}, {self.right})"
#
#     def __eq__(self, other):
#         return (
#                 isinstance(other, RelationExpression) and
#                 other.left == self.left and
#                 other.right == self.right
#         )


class OrExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[OrExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, OrExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_or_expression(self)


class AddExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[AddExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, AddExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_add_expression(self)


class SubExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[SubExpression ({self.left}, {self.right}) {self.line} {self.column} "

    def __eq__(self, other):
        return (
            isinstance(other, SubExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_sub_expression(self)


class MultiplyExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[MultiplicationExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, MultiplyExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_multiply_expression(self)


class DivisionExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[DivisionExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, DivisionExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_division_expression(self)


class LessThanExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, LessThanExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_less_than_expression(self)


class LessThanOrEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, LessThanOrEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_less_than_or_equal_expression(self)


class GreaterThanExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, GreaterThanExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_greater_than_expression(self)


class GreaterThanOrEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, GreaterThanOrEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_greater_than_or_equal_expression(self)


class EqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, EqualExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_equal_expression(self)


class NotEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, NotEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_not_equal_expression(self)


class Assignment(Node):
    def __init__(self, identifier, expression, line=None, column=None):
        super().__init__(line, column)
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"[Assignment {self.identifier} {self.expression}]"

    def __eq__(self, other):
        return (
            isinstance(other, Assignment) and
            other.identifier == self.identifier and
            other.expression == self.expression
        )

    def accept(self, visitor):
        return visitor.visit_assignment(self)


class Arguments(Node):
    def __init__(self, arguments, line=None, column=None):
        super().__init__(line, column)
        self.arguments = arguments

    def __repr__(self):
        return f"[Arguments {self.arguments}]"

    def __eq__(self, other):
        return (
            isinstance(other, Arguments) and
            other.arguments == self.arguments
        )

    def accept(self, visitor):
        return visitor.visit_arguments(self)


class ReturnStatement(Node):
    def __init__(self, expression, line=None, column=None):
        super().__init__(line, column)
        self.expression = expression

    def __repr__(self):
        return f"[ReturnStatement {self.expression}]"

    def __eq__(self, other):
        return (
            isinstance(other, ReturnStatement) and
            other.expression == self.expression
        )

    def accept(self, visitor):
        return visitor.visit_return_statement(self)


class InitStatement(Node):
    def __init__(self, type, identifier, expression, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier
        self.expression = expression

    def __repr__(self):
        return f"[InitStatement {self.type} {self.identifier} {self.expression}]"

    def __eq__(self, other):
        return (
            isinstance(other, InitStatement) and
            other.type == self.type and
            other.identifier == self.identifier and
            other.expression == self.expression
        )

    def accept(self, visitor):
        return visitor.visit_init_statement(self, global_declaration=False)


class Declaration(Node):
    def __init__(self, type, identifier, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier

    def __repr__(self):
        return f"[Declaration {self.type} {self.identifier} ]"

    def __eq__(self, other):
        return (
            isinstance(other, Declaration) and
            other.type == self.type and
            other.identifier == self.identifier
        )

    def accept(self, visitor):
        return visitor.visit_declaration(self, global_declaration=False)


class ListType(Node):
    def __init__(self, type, line=None, column=None):
        super().__init__(line, column)
        self.type = type

    def __repr__(self):
        return f"[ListType {self.type}]"

    def __eq__(self, other):
        return (
            isinstance(other, ListType) and
            other.type == self.type
        )

    def accept(self, visitor):
        return visitor.visit_list_type(self)


class PairType(Node):
    def __init__(self, type_1, type_2, line=None, column=None):
        super().__init__(line, column)
        self.type_1 = type_1
        self.type_2 = type_2

    def __repr__(self):
        return f"[PairType {self.type_1} {self.type_2}]"

    def __eq__(self, other):
        return (
            isinstance(other, PairType) and
            other.type_1 == self.type_1 and
            other.type_2 == self.type_2
        )

    def accept(self, visitor):
        return visitor.visit_pair_type(self)


class DictType(Node):
    def __init__(self, key_type, value_type, line=None, column=None):
        super().__init__(line, column)
        self.key_type = key_type
        self.value_type = value_type

    def __repr__(self):
        return f"[DictType {self.key_type} {self.value_type}]"

    def __eq__(self, other):
        return (
            isinstance(other, DictType) and
            other.key_type == self.key_type and
            other.value_type == self.value_type
        )

    def accept(self, visitor):
        return visitor.visit_dict_type(self)


class IntType(Node):
    def __init__(self, line=None, column=None):
        self.value = int

    def __repr__(self):
        return f"[IntType]"

    def __eq__(self, other):
        return (
            isinstance(other, IntType)
        )

    def accept(self, visitor):
        return visitor.visit_int_type(self)


class StringType(Node):
    def __init__(self, line=None, column=None):
        self.value = str

    def __repr__(self):
        return f"[StringType]"

    def __eq__(self, other):
        return (
            isinstance(other, StringType)
        )

    def accept(self, visitor):
        return visitor.visit_string_type(self)


class FloatType(Node):
    def __init__(self, line=None, column=None):
        self.value = float

    def __repr__(self):
        return f"[FloatType]"

    def __eq__(self, other):
        return (
            isinstance(other, FloatType)
        )

    def accept(self, visitor):
        return visitor.visit_float_type(self)


class BoolType(Node):
    def __init__(self, line=None, column=None):
        self.value = bool

    def __repr__(self):
        return f"[BoolType]"

    def __eq__(self, other):
        return (
            isinstance(other, BoolType)
        )

    def accept(self, visitor):
        return visitor.visit_bool_type(self)


class List(Node):
    def __init__(self, elements, line=None, column=None):
        super().__init__(line, column)
        self.elements = elements

    def __repr__(self):
        return f"[List {self.elements}]"

    def __eq__(self, other):
        return (
            isinstance(other, List) and
            other.elements == self.elements
        )

    def accept(self, visitor):
        return visitor.visit_list(self)


class Pair(Node):
    def __init__(self, left, right, line=None, column=None):
        super().__init__(line, column)
        self.left = left
        self.right = right

    def __repr__(self):
        return f"[Pair {self.left} {self.right}]"

    def __eq__(self, other):
        return (
            isinstance(other, Pair) and
            other.left == self.left and
            other.right == self.right
        )

    def accept(self, visitor):
        return visitor.visit_pair(self)


class Dict(Node):
    def __init__(self, pairs, line=None, column=None):
        super().__init__(line, column)
        self.pairs = pairs

    def __repr__(self):
        return f"[Dict {self.pairs}]"

    def __eq__(self, other):
        return (
            isinstance(other, Dict) and
            other.pairs == self.pairs
        )

    def accept(self, visitor):
        return visitor.visit_dict(self)
