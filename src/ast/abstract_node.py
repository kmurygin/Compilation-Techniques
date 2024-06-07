from abc import ABC, abstractmethod


class Node(ABC):
    @abstractmethod
    def __init__(self, line: int = None, column: int = None):
        self.line = line
        self.column = column
        self.position = line, column