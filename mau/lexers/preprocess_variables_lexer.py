from mau.lexers.base_lexer import BaseLexer, TokenType, rematch
from mau.token import Token
from mau.text_buffer.context import Context


class PreprocessVariablesLexer(BaseLexer):
    r"""This lexer has been designed to work on
    strings of text (single lines). It detects
    the characters {} that might surround a
    variable, the escape \, or the backtick `.
    """

    def _process_literal(self):
        # Spot if the current character is one
        # among \`{}. These wil be useful to the
        # parser as they might contain
        # variables or escaped variables.

        # If the current char is not special
        # just return.
        if self._current_char not in r"\`{}":
            return None

        return [self._create_token_and_skip(TokenType.LITERAL, self._current_char)]

    def _process_text(self):
        # Anything that is not a special character
        # can be collected under the generic name
        # of "text".
        match = rematch(r"[^\\`{}]+", self._tail)

        if not match:  # pragma: no cover
            return None

        return [self._create_token_and_skip(TokenType.TEXT, match.group())]

    def _process_functions(self):
        return [
            self._process_literal,
            self._process_text,
        ]
