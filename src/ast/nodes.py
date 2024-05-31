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


class Function(Node):
    def __init__(self, type, identifier, arguments, body, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier
        self.arguments = arguments
        self.body = body

    def __eq__(self, other):
        return (
                isinstance(other, Function) and
                self.type == other.type and
                self.identifier == other.identifier and
                self.arguments == other.arguments and
                self.body == other.body
        )

    def __repr__(self):
        return f"[Function: {self.type} {self.identifier} {self.arguments} {self.body}]"


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


class WhileStatement(Node):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


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


class RelationExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[RelationExpression {self.line} {self.column} ({self.left}, {self.right})"

    def __eq__(self, other):
        return (
                isinstance(other, RelationExpression) and
                other.left == self.left and
                other.right == self.right
        )


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


class LessThanExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[LessThanExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, LessThanExpression) and
            other.left == self.left and
            other.right == self.right
        )


class LessThanOrEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[LessThanOrEqualExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, LessThanOrEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )


class GreaterThanExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, GreaterThanExpression) and
            other.left == self.left and
            other.right == self.right
        )


class GreaterThanOrEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[GreaterThanOrEqualExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, GreaterThanOrEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )


class EqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[EqualExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, EqualExpression) and
            other.left == self.left and
            other.right == self.right
        )


class NotEqualExpression(Node):
    def __init__(self, left_term, right_term, line=None, column=None):
        super().__init__(line, column)
        self.left = left_term
        self.right = right_term

    def __repr__(self):
        return f"[NotEqualExpression {self.line} {self.column}]"

    def __eq__(self, other):
        return (
            isinstance(other, NotEqualExpression) and
            other.left == self.left and
            other.right == self.right
        )


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


class Declaration(Node):
    def __init__(self, type, identifier, line=None, column=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier

    def __repr__(self):
        return f"[Declaration {self.type} {self.identifier} ]"

    def __eq__(self, other):
        return (
            isinstance(other, InitStatement) and
            other.type == self.type and
            other.identifier == self.identifier
        )


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
