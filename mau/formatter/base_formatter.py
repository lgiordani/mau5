from abc import ABC

from mau.nodes.node import Node
from mau.text_buffer import Context, Position
from mau.token import Token


class BaseFormatter(ABC):
    type = "base"

    @classmethod
    def _adjust_context(cls, context: Context):
        return context.move_to(1, 1)

    @classmethod
    def _adjust_position(cls, position: Position):
        return (position[0] + 1, position[1] + 1)

    @classmethod
    def print_tokens(cls, tokens: list[Token]): ...

    @classmethod
    def print_nodes(cls, nodes: list[Node], indent: int = 0): ...
