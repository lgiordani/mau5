from mau.token import Token

from .base_formatter import BaseFormatter


class RawFormatter(BaseFormatter):
    type = "raw"

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        for token in tokens:
            print(f"{token.type} {repr(token.value)} {token.context}")
