from abc import ABC, abstractmethod

from mau.token import Token


class BaseFormatter(ABC):
    type = "base"

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        for token in tokens:
            print(token)
