from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from mau.environment.environment import Environment
from mau.lexers.arguments_lexer.lexer import ArgumentsLexer
from mau.nodes.node import Node, NodeInfo, ValueNodeContent
from mau.parsers.base_parser.parser import BaseParser
from mau.tokens.token import Token, TokenType


def set_names(
    unnamed_args: list[Any],
    named_args: dict[str, Any],
    positional_names: list[str],
) -> tuple[list[Any], dict[str, Any]]:
    """
    Give names to positional arguments.

    This function uses the given `positional_names`
    to convert unnamed args to named ones. Each node
    in `self.unnamed_argument_nodes` is assigned a
    key from `positional_names` in order.

    If a positional name is used that is already
    present in `self.named_argument_nodes`, the
    key is ignored and the corresponding unnamed
    node remains unassigned.
    """

    # Filter the given positional names.
    # If a named argument provides the value for a
    # positional name we consider it already set and ignore it.
    positional_names = [i for i in positional_names if i not in named_args]

    # Merge positional names and args into a dictionary.
    # Then create a named argument out of each value.
    # The zip() will ignore arguments that don't have a
    # corresponding value.
    positional_arguments = dict(zip(positional_names, unnamed_args))

    # If we pass more positional values than names,
    # some of them won't be converted and become flags
    unnamed_args = unnamed_args[len(positional_names) :]

    # Update the named dictionary with the
    named_args.update(positional_arguments)

    return unnamed_args, named_args


@dataclass
class Arguments:
    unnamed_args: list[str] = field(default_factory=list)
    named_args: dict[str, str] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    subtype: str | None = None

    def asdict(self):
        return asdict(self)

    def set_names(self, positional_names: list[str]) -> Arguments:
        self.unnamed_args, self.named_args = set_names(
            self.unnamed_args, self.named_args, positional_names
        )

        return self


class ArgumentsParser(BaseParser):
    lexer_class = ArgumentsLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
    ):
        super().__init__(tokens, environment, parent_node)

        # This flag is turned on as soon as
        # a named argument is parsed
        self._named_arguments_on = False

        # This is the list of unnamed argument nodes.
        self.unnamed_argument_nodes: list[Node[ValueNodeContent]] = []

        # This is the list of named argument nodes.
        self.named_argument_nodes: dict[str, Node[ValueNodeContent]] = {}

        # This is the list of tag nodes.
        self.tag_nodes: list[Node[ValueNodeContent]] = []

        # This is the subtype node.
        self.subtype: Node[ValueNodeContent] | None = None

    def _process_functions(self):
        return [
            self._process_eol,
            self._process_named_argument,
            self._process_unnamed_argument,
        ]

    def _process_eol(self):
        # This simply ignores the end of line.

        self.tm.get_token(TokenType.EOL)

        return True

    def _process_named_argument(self):
        # This parses a named argument in the form
        # key=value
        # or
        # key="value"

        # Get the token with the key.
        key_token = self.tm.get_token(TokenType.TEXT)

        # The context of the argument is the
        # context of the key.
        context = key_token.context

        # After a key there should be an equal.
        # If not, this function fails.
        self.tm.get_token(TokenType.LITERAL, "=")

        # Values can be surrounded by quotes.
        # If there are quotes we skip them.
        if self.tm.peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self.tm.get_token(TokenType.LITERAL, '"')

            # Get everything before the next double quotes.
            value = self.tm.collect_join([Token(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self.tm.get_token(TokenType.LITERAL, '"')
        else:
            # Get everything before the comma or EOF.
            value = self.tm.collect_join([Token(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self.tm:
            self.tm.get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self.tm:
            self.tm.get_token(TokenType.WHITESPACE)

        # Save the node.
        node = Node(
            info=NodeInfo(context=context),
            # Remove leading and trailing spaces from the value.
            content=ValueNodeContent(value.strip()),
            parent=self.parent_node,
        )

        self.named_argument_nodes[key_token.value] = node

        # Mark the beginning of named arguments
        self._named_arguments_on = True

        return True

    def _process_unnamed_argument(self):
        # This parses an unnamed argument in the form
        # value
        # or
        # "value"

        # Unnamed arguments can't appear after named ones.
        if self._named_arguments_on:
            raise self._error("Unnamed arguments after named arguments are forbidden")

        # Values can be surrounded by quotes
        # If there are quotes we skip them.
        if self.tm.peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self.tm.get_token(TokenType.LITERAL, '"')

            # The context of the argument is the
            # context of the first token.
            context = self.tm.peek_token().context

            # Get everything before the next double quotes.
            value = self.tm.collect_join([Token(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self.tm.get_token(TokenType.LITERAL, '"')
        else:
            # The context of the argument is the
            # context of the first token.
            context = self.tm.peek_token().context

            # Get everything before the comma or EOF.
            value = self.tm.collect_join([Token(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self.tm:
            self.tm.get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self.tm:
            self.tm.get_token(TokenType.WHITESPACE)

        # Save the node.
        node = Node(
            info=NodeInfo(context=context),
            content=ValueNodeContent(value),
            parent=self.parent_node,
        )

        self.unnamed_argument_nodes.append(node)

        return True

    def _isolate_tags_and_subtype(self):
        # Isolate tags.
        self.tag_nodes = []
        for i in self.unnamed_argument_nodes:
            # Discard arguments that do not start with `#`.
            if not i.content.value.startswith("#"):  # type: ignore[attr-defined]
                continue

            # Remove the initial `#`.
            i.content.value = i.content.value[1:]  # type: ignore[attr-defined]

            # Append the node to the list of tags.
            self.tag_nodes.append(i)

        # Isolate subtypes.
        subtypes = []
        for i in self.unnamed_argument_nodes:
            # Discard arguments that do not start with `*`.
            if not i.content.value.startswith("*"):  # type: ignore[attr-defined]
                continue

            # Remove the initial `*`.
            i.content.value = i.content.value[1:]  # type: ignore[attr-defined]

            # Append the node to the list of subtypes.
            subtypes.append(i)

        # There can be only one subtype.
        if len(subtypes) > 1:
            raise self._error("Multiple subtypes detected")

        # Extract the subtype if present.
        if len(subtypes) == 1:
            # Get the only subtype and remove the leading "*"
            self.subtype = subtypes[0]

        if self.subtype:
            # Check if the subtype contains
            # additional named_arguments.
            subtype_replacements = self.environment.getvar(
                "mau.parser.subtype_replacements", Environment()
            ).asdict()
            subtype_named_arguments = subtype_replacements.get(
                self.subtype.content.value, {}
            )

            # We need to add those arguments as nodes
            # with the same context as the subtype.
            # However, if the arguments are already there
            # we must not overwrite them.

            # These are the keys added by the subtype
            # that are not already in the processed arguments.
            missing_keys = set(subtype_named_arguments.keys()) - set(
                self.named_argument_nodes.keys()
            )

            for key in missing_keys:
                context = self.subtype.info.context
                value = subtype_named_arguments[key]

                self.named_argument_nodes[key] = Node(
                    info=NodeInfo(context=context),
                    content=ValueNodeContent(value),
                    parent=self.parent_node,
                )

        # Remove tags and subtype from unnamed arguments.
        self.unnamed_argument_nodes = [
            i for i in self.unnamed_argument_nodes if i not in self.tag_nodes + subtypes
        ]

    def set_names(self, positional_names: list[str]):
        self.unnamed_argument_nodes, self.named_argument_nodes = set_names(
            self.unnamed_argument_nodes, self.named_argument_nodes, positional_names
        )

    @property
    def arguments(self):
        return Arguments(
            unnamed_args=[node.content.value for node in self.unnamed_argument_nodes],  # type: ignore[attr-defined]
            named_args={
                key: node.content.value  # type: ignore[attr-defined]
                for key, node in self.named_argument_nodes.items()
            },
            tags=[node.content.value for node in self.tag_nodes],  # type: ignore[attr-defined]
            subtype=self.subtype.content.value if self.subtype else None,  # type: ignore[attr-defined]
        )

    def parse(self):
        """
        Process the extracted nodes and converts them into Python structures.
        Unnamed arguments become a list of values (similar to *args).
        Named arguments become a dictionary (similar to *kwargs).
        Tags are all the unnamed arguments whose value starts with `#`.
        Subtype is the unnamed argument whose value starts with `*`.
        There can't be more than one subtype.
        """

        super().parse()

        self._isolate_tags_and_subtype()
