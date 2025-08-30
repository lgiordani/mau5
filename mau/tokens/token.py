from enum import Enum

from mau.text_buffer.context import Context


class TokenType(Enum):
    ARGUMENTS = "ARGUMENTS"
    BLOCK = "BLOCK"
    COMMAND = "COMMAND"
    COMMENT = "COMMENT"
    CONTENT = "CONTENT"
    CONTROL = "CONTROL"
    EMPTY = "EMPTY"
    EOF = "EOF"
    EOL = "EOL"
    HEADER = "HEADER"
    HORIZONTAL_RULE = "HORIZONTAL_RULE"
    LIST = "LIST"
    # Characters with specific syntax value like
    # commas to separate between arguments, colons,
    # double quotes, etc.
    LITERAL = "LITERAL"
    MULTILINE_COMMENT = "MULTILINE_COMMENT"
    # Free text without a specific value in
    # the language
    TEXT = "TEXT"
    TITLE = "TITLE"
    VARIABLE = "VARIABLE"
    WHITESPACE = "WHITESPACE"


class Token:
    """
    This represents a token.
    Tokens have a type, a value (the actual characters), and a context
    """

    def __init__(
        self,
        _type: TokenType,
        value: str | None = None,
        context: Context | None = None,
    ):
        self.type = _type
        self.context = context
        self.value = value or ""

    def __repr__(self):
        return f'Token({self.type}, "{self.value}", {self.context})'

    def __eq__(self, other):
        if not isinstance(other, Token):
            return False

        return (self.type, self.value) == (
            other.type,
            other.value,
        )

    def __hash__(self):
        return hash((self.type, self.value))

    def __len__(self):
        if self.value:
            return len(self.value)

        return 0

    def __bool__(self):
        return True
