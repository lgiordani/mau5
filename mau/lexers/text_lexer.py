from mau.helpers import rematch
from mau.lexers.base_lexer import BaseLexer, TokenType


class TextLexer(BaseLexer):
    """
    This class provides a lexer for text paragraphs.

    It can identify whitespace, special characters, or text.
    """

    def _process_whitespace(self):
        match = rematch(r"\ +", self._tail)

        if not match:
            return None

        return [self._create_token_and_skip(TokenType.TEXT, " ")]

    def _process_literal(self):
        if self._current_char not in '~^_*`{}()[]\\"$%':
            return None

        return [self._create_token_and_skip(TokenType.LITERAL, self._current_char)]

    def _process_text(self):
        match = rematch(r'[^~\^_*`{}()[\]"\\ \$%]+', self._tail)

        if not match:  # pragma: no cover
            return None

        return [self._create_token_and_skip(TokenType.TEXT, match.group())]

    def _process_functions(self):
        return [
            self._process_whitespace,
            self._process_literal,
            self._process_text,
        ]
