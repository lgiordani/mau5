from .base_formatter import BaseFormatter
from mau.token import Token


class RawFormatter(BaseFormatter):
    type = "raw"

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        for token in tokens:
            print(f"{token.type} {repr(token.value)} {token.context}")
