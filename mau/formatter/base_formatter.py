from abc import ABC

from mau.token import Token
from mau.text_buffer import Context, Position


class BaseFormatter(ABC):
    type = "base"

    @classmethod
    def _adjust_context(cls, context: Context):
        return context.move_to(1, 1)

    @classmethod
    def _adjust_position(cls, position: Position):
        return (position[0] + 1, position[1] + 1)

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        for token in tokens:
            print(token)
