from mau.lexers.base_lexer.lexer import BaseLexer, TokenType
from mau.token import Token
from mau.text_buffer.context import Context


class PreprocessVariablesLexer(BaseLexer):
    def _process_literal(self):
        if self._current_char not in r"\`{}":
            return None

        return [self._create_token_and_skip(TokenType.LITERAL, self._current_char)]

    def _process_text(self):
        characters = []

        initial_position = self._position

        while (c := self._current_char) not in r"\`{}":
            characters.append(c)
            self._skip(c)

        final_position = self._position

        context = Context(
            *initial_position, *final_position, self.text_buffer.source_filename
        )

        return [Token(TokenType.TEXT, "".join(characters), context)]

    def _process_functions(self):
        return [
            self._process_literal,
            self._process_text,
        ]
