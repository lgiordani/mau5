from __future__ import annotations

from collections.abc import Sequence

from mau.parsers.preprocess_variables_parser import PreprocessVariablesParser
from mau.environment.environment import Environment
from mau.lexers.condition_lexer import ConditionLexer
from mau.text_buffer import Context
from mau.nodes.node import NodeInfo, ValueNode
from mau.nodes.node_arguments import NodeArguments, set_names
from mau.nodes.condition import ConditionNode
from mau.parsers.base_parser import BaseParser, create_parser_exception
from mau.token import Token, TokenType
from mau.message import BaseMessageHandler

INTERNAL_TAG_PREFIX = "mau:"


class ConditionParser(BaseParser):
    lexer_class = ConditionLexer

    def __init__(
        self,
        tokens: list[Token],
        message_handler: BaseMessageHandler,
        environment: Environment | None = None,
        parent_node=None,
    ):
        super().__init__(tokens, message_handler, environment, parent_node)

        # This is the list of condition nodes.
        self.condition_node: ConditionNode = None

    def _process_functions(self):
        return [
            self._process_condition,
        ]

    def _process_condition(self):
        # This parses a named argument in the form
        # key=value
        # or
        # key="value"

        # Get the variable
        variable_token = self.tm.get_token(TokenType.TEXT)

        # Get the comparison
        comparison_token = self.tm.get_token(TokenType.TEXT)

        # Get the value
        value_token = self.tm.get_token(TokenType.TEXT)

        # Find the final context.
        context = Context.merge_contexts(variable_token.context, value_token.context)

        # Save the node.
        node = ConditionNode(
            variable=variable_token.value,
            comparison=comparison_token.value,
            value=value_token.value,
            info=NodeInfo(context=context),
            parent=self.parent_node,
        )

        self.condition_node = node

        return True
