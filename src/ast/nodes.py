from .abstract_node import Node


class Variable(Node):
    def __init__(self, variable_type, variable_identifier, value=None, line=None, column=None):
        super().__init__(line, column)
        self.type = variable_type
        self.identifier = variable_identifier
        self.value = value
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return (
                isinstance(other, Variable) and
                self.type == other.type and
                self.identifier == other.identifier and
                self.value == other.value
        )

    def __repr__(self):
        return f"[Variable: {self.type} {self.identifier} {self.value}]"


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


class List(Node):
    def __init__(self, elements, line=None, column=None):
        super().__init__(line, column)
        # self.type = type
        self.elements = elements

    def __eq__(self, other):
        return (
                isinstance(other, List) and
                self.elements == other.elements
        )

    def __repr__(self):
        buff = f"[LIST:"
        for element in self.elements:
            buff += f" {element}"
        buff += "]"
        return buff


class Pair(Node):
    def __init__(self, value_1, value_2, line=None, column=None):
        super().__init__(line, column)
        # self.type_1 = type_1
        # self.type_2 = type_2
        self.value_1 = value_1
        self.value_2 = value_2

    def __eq__(self, other):
        return (
            isinstance(other, Pair) and
            self.value_1 == other.value_1 and
            self.value_2 == other.value_2
        )

    def __repr__(self):
        return f"[Pair: {self.value_1}, {self.value_2}]"


class Dict(Node):
    def __init__(self, pairs, line=None, column=None):
        super().__init__(line, column)
        self.pairs = pairs

    def __eq__(self, other):
        return (
            isinstance(other, Dict) and
            other.pairs == self.pairs
        )

    def __repr__(self):
        return f"[Dict: {self.pairs}]"


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
    def __init__(self, identifier, arguments, line, column):
        super().__init__(line, column)
        self.identifier = identifier
        self.arguments = arguments

    def __eq__(self, other):
        return (
                isinstance(other,
                           FunctionCall) and self.identifier == other.identifier and self.arguments == other.arguments
        )


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
    def __init__(self, type, identifier, collection, body, line=None, column=None, key_identifier=None):
        super().__init__(line, column)
        self.type = type
        self.identifier = identifier
        self.collection = collection
        self.body = body
        self.key_identifier = key_identifier

    def __eq__(self, other):
        return (
                isinstance(other, ForStatement) and
                self.type == other.type and
                self.identifier == other.identifier and
                self.collection == other.collection and
                self.body == other.body and
                self.key_identifier == other.key_identifier
        )

    def __repr__(self):
        return f"[For: {self.type} {self.identifier} {self.collection} {self.body} {self.key_identifier}]"


class WhileStatement(Node):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class PrintFunction(Node):
    def __init__(self, value, line=None, column=None):
        super().__init__(line, column)
        self.value = value

    def __eq__(self, other):
        return (
                isinstance(other, PrintFunction) and
                self.value == other.value
        )


class CollectionOperation(Node):
    def __init__(self, source_list, line=None, column=None):
        super().__init__(line, column)
        self.source_list = source_list
        # self.line = line
        # self.column = column

    def __repr__(self):
        pass


class At(CollectionOperation):
    def __init__(self, source_list, idx, line=None, column=None):
        super().__init__(source_list, line, column)
        self.source_list = source_list
        self.idx = idx
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return isinstance(other, At) and self.source_list == other.source_list and self.idx == other.idx

    def __repr__(self):
        return f"[Get: {self.source_list}, {self.idx}]"


class Length(CollectionOperation):
    def __init__(self, source_list, line=None, column=None):
        super().__init__(source_list, line, column)
        self.source_list = source_list
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return isinstance(other, Length) and self.source_list == other.source_list

    def __repr__(self):
        return f"[Length: {self.source_list}]"


class Remove(CollectionOperation):
    def __init__(self, source_list, idx, line=None, column=None):
        super().__init__(source_list, line, column)
        self.source_list = source_list
        self.idx = idx
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return isinstance(other, Remove) and self.source_list == other.source_list and self.idx == other.idx

    def __repr__(self):
        return f"[Delete: {self.source_list}, {self.idx}]"


class Type(CollectionOperation):
    def __init__(self, source_list, line=None, column=None):
        super().__init__(source_list, line, column)
        self.source_list = source_list
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return isinstance(other, Type) and self.source_list == other.source_list

    def __repr__(self):
        return f"[Type: {self.source_list}]"


class Append(CollectionOperation):
    def __init__(self, source_list, idx, line=None, column=None):
        super().__init__(source_list, line, column)
        self.source_list = source_list
        self.idx = idx
        # self.line = line
        # self.column = column

    def __eq__(self, other):
        return (isinstance(other, Append) and
                self.source_list == other.source_list and
                self.idx == other.idx
                )

    def __repr__(self):
        return f"[Append: {self.source_list}, {self.idx}]"


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