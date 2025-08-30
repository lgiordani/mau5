from mau.environment.environment import Environment
from mau.lexers.arguments_lexer import ArgumentsLexer
from mau.nodes.arguments import NamedArgumentNodeContent, UnnamedArgumentNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import BaseParser
from mau.tokens.token import Token, TokenType


def set_names_and_defaults(
    args: list[str],
    kwargs: dict[str, str],
    positional_names: list[str],
    default_values: dict[str, str | None] | None = None,
):
    """
    Give names to positional arguments and assign
    default values to the ones that have not been
    initialised.

    This function uses the given `positional_names`
    to convert unnamed args to named ones. Each
    value in `args` is assigned to a key from
    `positional_names` in order.

    The values in the final dictionary are
    set according to the following hierarchy:

    args + positional > kwargs > default

    So, the following input

    args: [3],
    kwargs: {"price": 42},
    positional_names: ["price"],
    default_values: {"price": 0}

    results in

    {"price": 3}

    because the default value 0 is overridden by
    the kwargs value 42, which in turn is overridden
    by the poritional value 3.
    """

    # Copy default values so that we can update
    # it without affecting the original dictionary.
    results = default_values.copy() if default_values else {}

    # Filter the given positional names.
    # If a named argument provides the value for a
    # positional name we consider it already set and ignore it.
    positional_names = [i for i in positional_names if i not in kwargs]

    # If we pass more positional values than names,
    # some of them won't be converted and become flags
    remaining_args = args[len(positional_names) :]

    # Merge positional names and args into a dictionary.
    positional_arguments = dict(zip(positional_names, args))

    # Update the default values with the given
    # named arguments.
    results.update(kwargs)

    # Update the default values with the given
    # positional arguments.
    results.update(positional_arguments)

    # Positional names identify mandatory keys,
    # so all of them have to be present in the
    # final dictionary.
    # This might not be true if we pass less
    # positional values (args) than names
    # and there are no kwargs or defaults to
    # provide values.

    available_keys = set(results.keys())
    mandatory_keys = set(positional_names)

    if not mandatory_keys.issubset(available_keys):
        missing_keys = mandatory_keys - available_keys

        raise ValueError(
            f"The following attributes need to be specified: {missing_keys}"
        )

    return remaining_args, results


class ArgumentsParser(BaseParser):
    lexer_class = ArgumentsLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
        parent_position=None,
    ):
        super().__init__(tokens, environment, parent_node, parent_position)

        # This flag is turned on as soon as
        # a named argument is parsed
        self._named_arguments = False

    def _process_functions(self):
        return [
            self._process_eol,
            self._process_named_argument,
            self._process_unnamed_argument,
        ]

    def _process_eol(self):
        # This simply ignores the end of line.

        self._get_token(TokenType.EOL)

        return True

    def _process_named_argument(self):
        # This parses a named argument in the form
        # key=value
        # or
        # key="value"

        # Get the token with the key.
        key_token = self._get_token(TokenType.TEXT)

        # The context of the argument is the
        # context of the key.
        context = key_token.context

        # After a key there should be an equal.
        # If not, this function fails.
        self._get_token(TokenType.LITERAL, "=")

        # Values can be surrounded by quotes.
        # If there are quotes we skip them.
        if self._peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self._get_token(TokenType.LITERAL, '"')

            # Get everything until the next double quotes.
            value = self._collect_join([Token(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self._get_token(TokenType.LITERAL, '"')
        else:
            # Get everything until the comma or EOF.
            value = self._collect_join([Token(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self:
            self._get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self:
            self._get_token(TokenType.WHITESPACE)

        # Save the node.
        # Remove leading and trailing spaces from the value.
        self._save(
            Node(
                info=NodeInfo(context=context),
                content=NamedArgumentNodeContent(key_token.value, value.strip()),
            ),
        )

        # Mark the beginning of named arguments
        self._named_arguments = True

        return True

    def _process_unnamed_argument(self):
        # This parses an unnamed argument in the form
        # value
        # or
        # "value"

        # Unnamed arguments can't appear after named ones.
        if self._named_arguments:
            self._error("Unnamed arguments after named arguments are forbidden")

        # Values can be surrounded by quotes
        # If there are quotes we skip them.
        if self._peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self._get_token(TokenType.LITERAL, '"')

            # The context of the argument is the
            # context of the first token.
            context = self._peek_token().context

            # Get everything until the next double quotes.
            value = self._collect_join([Token(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self._get_token(TokenType.LITERAL, '"')
        else:
            # The context of the argument is the
            # context of the first token.
            context = self._peek_token().context

            # Get everything until the comma or EOF.
            value = self._collect_join([Token(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self:
            self._get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self:
            self._get_token(TokenType.WHITESPACE)

        # Save the node.
        self._save(
            Node(
                info=NodeInfo(context=context),
                content=UnnamedArgumentNodeContent(value),
            ),
        )

        return True

    def process_arguments(self):
        """
        Process the extracted nodes and converts them into Python structures.
        Unnamed arguments become a list of values (similar to *args).
        Named arguments become a dictionary (similar to *kwargs).
        Tags are all the unnamed arguments whose value starts with `#`.
        Subtype is the unnamed argument whose value starts with `*`.
        There can't be more than one subtype.
        """

        # Filter the nodes and extract all the unnamed arguments.
        unnamed_arguments = [
            node.content.value
            for node in self.nodes
            if node.content.type == "unnamed_argument"
        ]

        # Filter the nodes and extract all the named arguments.
        named_arguments = {
            node.content.key: node.content.value
            for node in self.nodes
            if node.content.type == "named_argument"
        }

        # Isolate tags.
        tags = [i for i in unnamed_arguments if i.startswith("#")]

        # Isolate subtypes.
        subtypes = [i for i in unnamed_arguments if i.startswith("*")]

        # There can be only one subtype.
        if len(subtypes) > 1:
            self._error("Multiple subtypes detected")

        # The default subtype is None.
        # Extract the subtype if present.
        subtype = None
        if len(subtypes) == 1:
            # Get the first subtype and remove the leading "*"
            subtype = subtypes[0][1:]

        # Remove tags and subtype from unnamed arguments.
        unnamed_arguments = [i for i in unnamed_arguments if i not in tags + subtypes]

        # Remove the leading "#" from tags.
        tags = [i[1:] for i in tags]

        return unnamed_arguments, named_arguments, tags, subtype
