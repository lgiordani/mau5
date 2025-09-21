import logging

from mau.environment.environment import Environment

# from mau.errors import MauError, MauErrorException
# from mau.parsers.arguments import set_names_and_defaults
# from mau.text_buffer.context import print_context
from mau.lexers.base_lexer.lexer import BaseLexer
from mau.nodes.node import Node
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer
from mau.tokens.token import Token, TokenType

from .managers.tokens_manager import TokensManager

logger = logging.getLogger(__name__)


class MauParserException(ValueError):
    def __init__(
        self, message: str, context: Context | None = None, long_help: str | None = None
    ):
        self.message = message
        self.context = context
        self.long_help = long_help


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

        with open(c.source) as f:
            lines = f.readlines()

            output.append("")
            output.append(lines[c.line].replace("\n", ""))
            output.append(" " * c.column + "^")

    if lh := exception.long_help:
        output.append("")
        output.append(lh)

    return "\n".join(output)


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
        self.tm = TokensManager(tokens)

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

    def _save(self, node):
        # Store the node.
        node.set_parent(self.parent_node)

        self.nodes.append(node)

    def _process_functions(self):
        # The parse functions available in this parser
        return []

    def _error(self, message: str, context: Context | None = None):
        context = context or self.tm.current_token.context

        return MauParserException(message=message, context=context)

    def parse(self):
        """
        Run the parser on the lexed tokens.
        """

        # Loop on all lexed tokens until we reach EOF.

        while not self.tm.peek_token_is(TokenType.EOF):
            # This detects infinite loops created by incomplete
            # parsing functions. Those functions keep trying
            # to parse the same token, so if we spot that
            # we are doing it we should raise an error.
            next_token = self.tm.peek_token()

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
                with self.tm:
                    result = process_function()

                if result is True:
                    # True means the function was successful
                    # and we can stop the loop.
                    break

            # If we get here and result is still False
            # we didn't find any function to parse the
            # current token.
            if result is False:
                raise self._error(
                    "Cannot parse token",
                    self.tm.peek_token().context,
                )

        # Check the produced nodes.
        # This is going to scan each node and each child
        # looking for inconsistencies between the allowed
        # keys and the actual children keys.
        recursive_check_nodes(self.nodes)

    @classmethod
    def lex_and_parse(
        cls,
        text: str,
        context: Context | None,
        environment: Environment | None,
        *args,
        **kwargs,
    ):
        text_buffer = cls.text_buffer_class(text, context)

        lexer = cls.lexer_class(text_buffer, environment)
        lexer.process()

        parser = cls(lexer.tokens, environment, *args, **kwargs)
        parser.parse()
        parser.finalise()

        return parser

    def finalise(self):
        pass


def recursive_check_nodes(nodes: list[Node]):
    if not nodes:
        return

    for node in nodes:
        if node.check_children():
            raise ValueError(
                f"{node.content.__class__} accepts {node.content.allowed_keys} - found {node.children.keys()} - Full node dump: {node}"
            )

        for key, value in node.children.items():
            recursive_check_nodes(value)
