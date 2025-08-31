import logging
from collections.abc import Callable

from mau.environment.environment import Environment

# from mau.errors import MauError, MauErrorException
# from mau.parsers.arguments import set_names_and_defaults
# from mau.text_buffer.context import print_context
from mau.lexers.base_lexer import BaseLexer
from mau.nodes.node import Node
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer
from mau.tokens.token import Token, TokenType

logger = logging.getLogger(__name__)


class MauParserException(ValueError):
    def __init__(self, message: str, context: Context | None = None):
        self.message = message
        self.context = context


def format_parser_error(exception: MauParserException) -> str:
    # This is a function used to print an error occurred
    # during processing.

    output = []

    output.append("######################################")
    output.append("## Parser error")
    output.append("")
    output.append(f"Message: {exception.message}")

    if c := exception.context:
        output.append("")
        output.append(f"Line: {c.line}")
        output.append(f"Column: {c.column}")
        output.append(f"Source: {c.source}")

    return "\n".join(output)


def format_node(node: Node) -> str:  # pragma: no cover
    return node.asdict()


# This is a generic function that processes text with a
# lexer and a parser.
def lex_and_parse(
    lexer_class,
    parser_class,
    text: str,
    context: Context,
    environment: Environment,
    *args,
    **kwargs,
):  # pragma: no cover
    text_buffer = TextBuffer(text, context)

    # Initialise the lexer.
    lexer = lexer_class(text_buffer, environment)

    # Process the text and retrieve tokens.
    lexer.process()

    # Initialise the parser.
    parser = parser_class(lexer.tokens, environment, *args, **kwargs)

    # Process the tokens and retrieve nodes.
    parser.parse()

    return parser


class TokenError(ValueError):
    """
    This is an exception that parsers can use to signal
    that the current function cannot process the upcoming
    tokens.
    This means that the parser as a context manager
    must reset the index, but also that the exception
    must not be propagated.
    """

    def __init__(self, message: str | None = None, context: Context | None = None):
        self.message = message
        self.context = context


class BaseParser:
    text_buffer_class = TextBuffer
    lexer_class = BaseLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
        parent_position=None,
    ):
        # This is the index of the current token.
        self.index: int = -1

        # These are the tokens parsed by the parser.
        self.tokens: list[Token] = tokens

        # A stack for the parser's state.
        # Currently the state is represented only
        # by the current index in the input tokens.
        self._stack: list[int] = []

        # These are the nodes created by the parsing.
        self.nodes: list[Node] = []

        # The last processed token. Used to detect loops.
        self.last_processed_token: Token = Token(TokenType.EOF)

        # The configuration environment
        self.environment: Environment = environment or Environment()

        # This is the parent node of all the nodes
        # created by this parser
        self.parent_node = parent_node

        # This is the position of all the nodes
        # in the parent
        self.parent_position = parent_position

    @property
    def _current_token(self) -> Token:
        """
        Returns the token being parsed.
        We often need to know which token we are currently
        parsing, but we might already have parsed all
        of them, so this convenience method wraps the
        possible index error.
        """

        if not self.tokens:
            raise TokenError("No tokens")

        if self.index < 0:
            return self.tokens[-1]

        try:
            return self.tokens[self.index]
        except IndexError:
            return self.tokens[-1]

    def _advance(self):
        if self.index < len(self.tokens):
            self.index += 1

    def _push(self):
        # Push the current state on the stack.
        self._stack.append(self.index)

    def _pop(self) -> int:
        # Get the state from the stack.
        return self._stack.pop()

    def __enter__(self):
        # The parser can be used as a context manager.
        # When we enter a new context we just need to
        # push the current state.
        self._push()

    def __exit__(self, etype, evalue, etrace) -> bool:
        # This is automatically run when we leave the context.
        # The execution of a parser function can either return
        # None or raise an exception.
        # In the first case everything went well, and we can exit
        # the context manager after we restored the stack.
        # In the second case we need to check if the exception
        # is an expected one or not. If the exception is
        # a signal that the function failed we can suppress it.

        # First make sure we leave the stack as it was before
        # we entered the context.
        stacked_index = self._pop()

        # If there was no exception we can exit the
        # context manager and continue execution
        if etype is None:
            return True

        # If there was an exception we need to
        # actually backtrace and pretend we didn't
        # do anything. Be cautious and don't get caught.

        # Restore the original position
        self.index = stacked_index

        # If the exception is not among the managed
        # ones we need to signal that it has to
        # be propagated
        if etype not in [TokenError]:
            return False

        # At this point we know that there was
        # an exception but we can ignore it as
        # it is one of the expected ones
        return True

    def _save(self, node):
        # Store the node.
        node.set_parent(self.parent_node)

        self.nodes.append(node)

    # def save(self, node):
    #     # Store the node.
    #     self.nodes.append(node)

    def _check_token(
        self,
        token: Token,
        ttype: TokenType | None = None,
        tvalue: str | None = None,
        value_check_function: Callable[[str], bool] | None = None,
    ) -> Token:
        # This method performs a test on the current token,
        # figuring out if type and value correspond to those passed
        # as arguments. If type or value are not given they are not
        # tested.
        # If the test is successful the token is returned, otherwise
        # the TokenError exception is raised.
        # The argument value_check_function is a function that
        # can be passed to test the token value and shall return a boolean.

        check_type = ttype or token.type
        if token.type != check_type:
            expected_token = Token(check_type, tvalue)

            raise TokenError(
                message=f"Found token {token}, Expected token: {expected_token}",
                context=token.context,
            )

        if tvalue is not None and token.value != tvalue:
            raise TokenError(
                message=f"Value of token {token} is not {tvalue}", context=token.context
            )

        if (
            value_check_function is not None
            and value_check_function(token.value) is False
        ):
            raise TokenError(
                message=f"Value of token {token} didn't pass check with {value_check_function}",
                context=token.context,
            )

        return token

    def _process_functions(self):
        # The parse functions available in this parser
        return []

    def _error(self, message: str, context: Context | None = None):
        context = context or self._current_token.context

        return MauParserException(message=message, context=context)

    def _put_token(self, token: Token):
        self.tokens.insert(self.index + 1, token)

    def _check_current_token(
        self,
        ttype: TokenType,
        tvalue: str | None = None,
        value_check_function: Callable[[str], bool] | None = None,
    ) -> Token:
        """
        Just check the type and value of the current token without
        advancing the index.
        """

        return self._check_token(
            self._current_token, ttype, tvalue, value_check_function
        )

    def _peek_token(
        self,
        ttype: TokenType | None = None,
        tvalue: str | None = None,
        value_check_function: Callable[[str], bool] | None = None,
    ) -> Token:
        """
        Return the next token without advancing the index.

        If the next token doesn't match the given type or value
        the function raises TokenError, that can be intercepted
        by the method parse. This means that the current processing
        function failed, and that the parser should try to
        use the next one.
        """

        try:
            token = self.tokens[self.index + 1]
        except IndexError:
            token = self.tokens[-1]

        return self._check_token(token, ttype, tvalue, value_check_function)

    def _get_token(
        self,
        ttype: TokenType | None = None,
        tvalue: str | None = None,
        value_check_function: Callable[[str], bool] | None = None,
    ) -> Token:
        """
        Return the next token and advances the index.
        This function returns the next token and then advances the index,
        and can optionally check its type or value.
        If the check fails the index is not advanced.
        """

        self._peek_token(ttype, tvalue, value_check_function)

        self._advance()

        return self._current_token

    def _peek_token_is(
        self,
        ttype: TokenType,
        tvalue: str | None = None,
        value_check_function: Callable[[str], bool] | None = None,
    ) -> bool:
        """
        Peek a token and check it.
        This works like peek_token, but returns a boolean
        instead of raising an exception.
        """

        try:
            self._peek_token(ttype, tvalue, value_check_function)
            return True
        except TokenError:
            return False

    def _force_token(
        self,
        ttype: TokenType,
        tvalue: str | None = None,
    ) -> Token:
        """
        This function is equivalent to _get_token but
        raises a parser exception when the processed token
        doesn't match the given type or value.

        The function should be used when we expect a
        given token and there is no other possible outcome.
        """
        try:
            token = self._get_token(ttype, tvalue)
        except TokenError:
            # This is the token that the parser finds
            # instead of the expected one.
            token = self._peek_token()

            error_message = f"Expected token of type {ttype}"

            if tvalue is not None:
                error_message = f"{error_message} with value '{tvalue}'"

            raise self._error(error_message, token.context)

        return token

    def _collect(
        self, stop_tokens: list[Token], preserve_escaped_stop_tokens: bool = False
    ):
        """
        Collect all tokens until one of the stop_tokens pops up.

        The stop token that terminates the collection is added to
        the joined list.

        An escape token (a literal "\\") is processed according
        to the following rules:

        * In front of a normal token it is kept.
        * In front of an escape token it is removed.
        * In front of an escape token with preserve_escaped_stop_tokens on it is kept.
        """
        tokens = []

        # After all, at EOF the world ends.
        stop_tokens.append(Token(TokenType.EOF))

        # This keeps looking at the next token and
        # stops when it is one of the stop ones.
        while self._peek_token() not in stop_tokens:
            # Stop tokens might be escaped, but we
            # consider the escape only if
            # preserve_escaped_stop_tokens is True.
            if self._peek_token() == Token(TokenType.LITERAL, "\\"):
                # Store the literal escape.
                escape = self._get_token()

                # We keep the escaped token if it is not
                # a stop one, or if the preserve flag is on.
                if (
                    self._peek_token() not in stop_tokens
                    or preserve_escaped_stop_tokens
                ):
                    tokens.append(escape)

            # Append the next token.
            # This might be a normal token or the escaped
            # one if the logic above added the escape.
            tokens.append(self._get_token())

        return tokens

    def _collect_join(
        self,
        stop_tokens: list[Token],
        join_with: str = "",
        preserve_escaped_stop_tokens: bool = False,
    ):
        """
        Collect tokens and join them.

        Collect all tokens until one of the stop_tokens
        pops up and join them in a single string.
        This works exactly like collect but returns
        a string of tokens joined with the given characters.
        """

        # Some tokens have value None, so this removes them
        token_values = [
            t.value
            for t in self._collect(stop_tokens, preserve_escaped_stop_tokens)
            if t.value != ""
        ]

        return join_with.join(token_values)

    def parse(self):
        """
        Run the parser on the lexed tokens.
        """

        # Loop on all lexed tokens until we reach EOF.

        while not self._peek_token_is(TokenType.EOF):
            # This detects infinite loops created by incomplete
            # parsing functions. Those functions keep trying
            # to parse the same token, so if we spot that
            # we are doing it we should raise an error.
            next_token = self._peek_token()

            if (
                next_token == self.last_processed_token
                and next_token.context == self.last_processed_token.context
            ):
                raise self._error(
                    "Loop detected, cannot parse token"
                )  # pragma: no cover
            else:
                self.last_processed_token = next_token

            # Here we run all parsing functions provided by
            # the parser until one returns a sensible result.
            result = False
            for process_function in self._process_functions():
                # The context manager wraps the function so that
                # any exception leaves the parsed tokens as they
                # were at the beginning of the function execution.
                #
                # If the parse function is successful it returns
                # True. If the function raises an exception the
                # variable result is not set and the value is False.
                # Any other result returned by the function
                # is ignored.
                with self:
                    result = process_function()

                if result is True:
                    # True means the function was successful
                    # and we can stop the loop.
                    break

            # If we get here and result is still False
            # we didn't find any function to parse the
            # current token.
            if result is False:
                raise self._error("Cannot parse token")

    @classmethod
    def lex_and_parse(cls, text, context, environment, *args, **kwargs):
        text_buffer = cls.text_buffer_class(text, context)

        lexer = cls.lexer_class(text_buffer, environment)
        lexer.process()

        parser = cls(lexer.tokens, environment, *args, **kwargs)
        parser.parse()

        return parser

    def finalise(self):
        pass
