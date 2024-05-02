from src.token.token_types import TokenType
from typing import Optional


class Token:
    def __init__(self, type: TokenType, value: Optional[str | int | float], position: tuple[int, int]):
        self.type = type
        self.value = value
        self.position = position

    def __str__(self):
        return f'{self.type}: {self.value}'
