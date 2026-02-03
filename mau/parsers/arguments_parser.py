from __future__ import annotations

from mau.environment.environment import Environment
from mau.lexers.arguments_lexer import ArgumentsLexer
from mau.nodes.node import NodeInfo, ValueNode
from mau.nodes.node_arguments import NodeArguments, set_names
from mau.parsers.base_parser import BaseParser, create_parser_exception
from mau.token import Token, TokenType


class ArgumentsParser(BaseParser):
    lexer_class = ArgumentsLexer

    def __init__(
        self,
        tokens: list[Token],
        environment: Environment | None = None,
        parent_node=None,
    ):
        super().__init__(tokens, environment, parent_node)

        # Save the context of the first token
        # to make exceptions more useful.
        self.context = None
        if tokens:
            self.context = tokens[0].context

        # This flag is turned on as soon as
        # a named argument is parsed
        self._named_arguments_on = False

        # This is the list of unnamed argument nodes.
        self.unnamed_argument_nodes: list[ValueNode] = []

        # This is the list of named argument nodes.
        self.named_argument_nodes: dict[str, ValueNode] = {}

        # This is the list of tag nodes.
        self.tag_nodes: list[ValueNode] = []

        # This is the subtype node.
        self.subtype: ValueNode | None = None

    def _process_functions(self):
        return [
            self._process_named_argument,
            self._process_unnamed_argument,
        ]

    def _process_named_argument(self):
        # This parses a named argument in the form
        # key=value
        # or
        # key="value"

        # Get the token with the key.
        key_token = self.tm.get_token(TokenType.TEXT)

        # After a key there should be an equal.
        # If not, this function fails.
        self.tm.get_token(TokenType.LITERAL, "=")

        # Values can be surrounded by quotes.
        # If there are quotes we skip them.
        if self.tm.peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self.tm.get_token(TokenType.LITERAL, '"')

            # Get everything before the next double quotes.
            token = self.tm.collect_join([Token.generate(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self.tm.get_token(TokenType.LITERAL, '"')
        else:
            # Get everything before the comma or EOF.
            token = self.tm.collect_join([Token.generate(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self.tm:
            self.tm.get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self.tm:
            self.tm.get_token(TokenType.WHITESPACE)

        # Save the node.
        node = ValueNode(
            token.value.strip(),
            info=NodeInfo(context=token.context),
            # Remove leading and trailing spaces from the value.
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
            raise create_parser_exception(
                message="Unnamed arguments after named arguments are forbidden",
                context=self.context,
            )

        # Values can be surrounded by quotes
        # If there are quotes we skip them.
        if self.tm.peek_token_is(TokenType.LITERAL, '"'):
            # Read and discard the opening quotes
            self.tm.get_token(TokenType.LITERAL, '"')

            # Get everything before the next double quotes.
            token = self.tm.collect_join([Token.generate(TokenType.LITERAL, '"')])

            # Read and discard the closing quotes
            self.tm.get_token(TokenType.LITERAL, '"')
        else:
            # Get everything before the comma or EOF.
            token = self.tm.collect_join([Token.generate(TokenType.LITERAL, ",")])

        # The comma is not there after the last argument,
        # so this is in a context manager as it might fail.
        with self.tm:
            self.tm.get_token(TokenType.LITERAL, ",")

        # Ignore whitespace after the comma.
        with self.tm:
            self.tm.get_token(TokenType.WHITESPACE)

        # Save the node.
        node = ValueNode(
            token.value,
            info=NodeInfo(context=token.context),
            parent=self.parent_node,
        )

        self.unnamed_argument_nodes.append(node)

        return True

    def _isolate_tags_and_subtype(self):
        # Isolate tags.
        self.tag_nodes = []
        for i in self.unnamed_argument_nodes:
            # Discard arguments that do not start with `#`.
            if not i.value.startswith("#"):  # type: ignore[attr-defined]
                continue

            # Remove the initial `#`.
            i.value = i.value[1:]  # type: ignore[attr-defined]

            # Append the node to the list of tags.
            self.tag_nodes.append(i)

        # Isolate subtypes.
        subtypes = []
        for i in self.unnamed_argument_nodes:
            # Discard arguments that do not start with `*`.
            if not i.value.startswith("*"):  # type: ignore[attr-defined]
                continue

            # Remove the initial `*`.
            i.value = i.value[1:]  # type: ignore[attr-defined]

            # Append the node to the list of subtypes.
            subtypes.append(i)

        # There can be only one subtype.
        if len(subtypes) > 1:
            raise create_parser_exception(
                message="Multiple subtypes detected",
                context=self.context,
            )

        # Extract the subtype if present.
        if len(subtypes) == 1:
            # Get the only subtype and remove the leading "*"
            self.subtype = subtypes[0]

        # Remove tags and subtype from unnamed arguments.
        self.unnamed_argument_nodes = [
            i for i in self.unnamed_argument_nodes if i not in self.tag_nodes + subtypes
        ]

        if self.subtype:
            # Check if the subtype contains
            # additional named_arguments.
            subtype_replacements = self.environment.get(
                "mau.parser.subtypes", Environment()
            ).asdict()
            subtype_replacement = subtype_replacements.get(
                self.subtype.value,  # type:ignore[attr-defined]
                {},
            )
            subtype_args = subtype_replacement.get("args", {})
            subtype_names = subtype_replacement.get("names", [])

            # We need to add those arguments as nodes
            # with the same context as the subtype.
            # However, if the arguments are already there
            # we must not overwrite them.

            # These are the keys added by the subtype
            # that are not already in the processed arguments.
            missing_keys = set(subtype_args.keys()) - set(
                self.named_argument_nodes.keys()
            )

            for key in missing_keys:
                context = self.subtype.info.context
                value = subtype_args[key]

                self.named_argument_nodes[key] = ValueNode(
                    value,
                    info=NodeInfo(context=context),
                    parent=self.parent_node,
                )

            self.set_names(subtype_names)

    def set_names(self, positional_names: list[str]):
        self.unnamed_argument_nodes, self.named_argument_nodes = set_names(
            self.unnamed_argument_nodes, self.named_argument_nodes, positional_names
        )

    @property
    def arguments(self):
        return NodeArguments(
            unnamed_args=[node.value for node in self.unnamed_argument_nodes],  # type: ignore[attr-defined]
            named_args={
                key: node.value  # type: ignore[attr-defined]
                for key, node in self.named_argument_nodes.items()
            },
            tags=[node.value for node in self.tag_nodes],  # type: ignore[attr-defined]
            subtype=self.subtype.value if self.subtype else None,  # type: ignore[attr-defined]
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
