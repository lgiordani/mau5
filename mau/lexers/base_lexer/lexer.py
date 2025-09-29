import logging

from mau.environment.environment import Environment
from mau.helpers import rematch
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer
from mau.tokens.token import Token, TokenType

logger = logging.getLogger(__name__)


class MauLexerException(ValueError):
    def __init__(self, message: str, context: Context | None = None):
        self.message = message
        self.context = context


def format_lexer_error(exception: MauLexerException) -> str:
    # This is a function used to print an error occurred
    # during processing.

    output = []

    output.append("######################################")
    output.append("## Lexer error")
    output.append("")
    output.append(f"Message: {exception.message}")

    if c := exception.context:
        output.append("")
        output.append(str(c))

    return "\n".join(output)


class BaseLexer:
    """
    The base class for lexers.
    The lexer decomposes the input text into a list of tokens
    and provides basic navigation functions in the
    output results.

    This class provides the base machinery for a lexer,
    running a sequence of functions until one of them
    successfully identifies a token.
    """

    def __init__(self, text_buffer: TextBuffer, environment: Environment | None = None):
        self.text_buffer: TextBuffer = text_buffer

        # This is the list of the tokens that
        # the lexer extracts.
        self.tokens: list[Token] = []

        # The last visited context. Used to detect loops.
        self.last_visited_context: Context | None = None

        # The configuration environment.
        self.environment: Environment = environment or Environment()

    def process(self):
        # Process tokens until we reach the end of file
        self._process()
        while True:
            # Check if the last thing we processed is an EOF
            if len(self.tokens) > 0 and self.tokens[-1].type is TokenType.EOF:
                break

            self._process()

    @property
    def _current_char(self) -> str:
        # Return the current character
        return self.text_buffer.current_char

    @property
    def _current_line(self) -> str:
        # Return the current line
        return self.text_buffer.current_line

    @property
    def _context(self) -> Context:
        # Return the context
        return self.text_buffer.context

    @property
    def _tail(self) -> str:
        # A wrapper to return the rest of the line
        return self.text_buffer.tail

    def _nextline(self):
        # Skip the whole line including the EOL
        self.text_buffer.nextline()

    def _skip(self, value):
        # Skip only the given amount of characters
        # This is very useful with regexp groups
        # that can be None.
        if value is not None:
            self.text_buffer.skip(len(value))

    def _error(self, message=None):
        raise MauLexerException(message=message, context=self._context)

    def _process(self):
        # This should not be touched by child classes
        # as it is the core of the lexer. It tries
        # each function in the list returned by
        # _process_functions and stores all the resulting
        # tokens.
        # All lexers process first EOF and EOL, and last
        # an error. This is mandatory as the underlying
        # text buffer doesn't flinch when we are past
        # EOL or EOF, and returns an empty string.
        # However, this means the parse can't skip the
        # token (it's empty) and end up in an infinite
        # loop, so we have to actively check that.
        # A lexer function must return None
        # when characters do not match the rule.

        process_functions = [
            self._process_eof,
            self._process_newline,
            self._process_trailing_spaces,
        ]
        process_functions.extend(self._process_functions())
        process_functions.append(self._process_error)

        # This detects infinite loops created by incomplete
        # lexing functions. Those functions keep trying
        # to parse the same context, so if we spot that
        # we are doing it we should raise an error.
        if (
            self.last_visited_context is not None
            and self.last_visited_context == self._context
        ):
            self._error("Loop detected, cannot process context.")  # pragma: no cover

        self.last_visited_context = self._context

        for process_func in process_functions:
            # This ensures result is always either None or a list
            result = process_func()

            if result is None:
                continue

            self.tokens.extend(result)

            return

    def _process_functions(self):
        return [
            self._process_text_line,
        ]

    def _process_error(self):
        self._error("No function found to process context.")

    def _create_token_and_skip(
        self, token_type, token_value: str | None = None
    ) -> Token:
        # Create the token and advance the position
        # in the text buffer to skip the characters
        # that are part of the token.

        # Clone the current context.
        context = self._context.clone()

        # Set the end line and column of the
        # token context. The line doesn't change
        # as all tokens are singl-line, but the
        # column should take into account the
        # length of the token.
        context.end_line = context.start_line

        columns = len(token_value) if token_value else 0
        context.end_column = context.start_column + columns

        token = Token(token_type, token_value, context)

        if token_value:
            self._skip(token_value)

        return token

    def _process_eof(self):
        if not self.text_buffer.eof:
            return None

        tokens = [self._create_token_and_skip(TokenType.EOF)]

        return tokens

    def _process_newline(self):
        # This detects an fully empty line,
        # that we want to preserve.

        match = rematch(r"^\ *$", self._current_line)

        if not match:
            return None

        tokens = [self._create_token_and_skip(TokenType.EOL, self._current_line)]

        self._nextline()

        # if self.text_buffer.eof:
        #     tokens.append(self._create_token_and_skip(TokenType.EOF))

        return tokens

    def _process_trailing_spaces(self):
        # This detects and skips any trailing spaces,
        # reaches the end of line and proceeds to the next line.
        match = rematch(r"\ *$", self._tail)

        if not match:
            return None

        self._skip(self._tail)

        self._nextline()

        return []

    def _process_text_line(self):
        tokens = [
            self._create_token_and_skip(TokenType.TEXT, self._tail),
        ]

        self._nextline()

        # if self.text_buffer.eof:
        #     return self._create_token_and_skip(TokenType.EOF)

        return tokens
