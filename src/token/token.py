from src.token.token_types import TokenType
from typing import Optional


class Token:
    def __init__(self, type: TokenType, value: Optional[str | int | float], position: tuple[int, int]):
        self.type = type
        self.value = value
        self.position = position

    def __str__(self):
        return f'{self.type}: {self.value}'

    def get_type(self) -> TokenType:
        return self.type

    def get_value(self) -> Optional[str | int | float]:
        return self.value

    def get_position(self) -> tuple[int, int]:
        return self.position

    def get_line(self):
        return self.position[0]

    def get_column(self):
        return self.position[1]
