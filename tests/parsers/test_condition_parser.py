from unittest.mock import patch

import pytest

from mau.environment.environment import Environment
from mau.message import MauException, MauMessageType
from mau.lexers.condition_lexer import ConditionLexer
from mau.nodes.node import NodeInfo, ValueNode
from mau.nodes.condition import ConditionNode
from mau.parsers.condition_parser import (
    ConditionParser,
    process_arguments_with_variables,
)
from mau.test_helpers import (
    compare_nodes,
    compare_nodes_map,
    compare_nodes_sequence,
    generate_context,
    parser_runner_factory,
)

runner = parser_runner_factory(ConditionLexer, ConditionParser)


def test_condition_parser():
    source = "variable1==value1"

    expected = ConditionNode(
        variable="variable1",
        comparison="==",
        value="value1",
        info=NodeInfo(
            context=generate_context(0, 0, 0, 17),
        ),
        parent=None,
    )

    parser = runner(source)

    assert parser.condition_node.variable == expected.variable
    assert parser.condition_node.comparison == expected.comparison
    assert parser.condition_node.value == expected.value
    assert parser.condition_node.info.asdict() == expected.info.asdict()
    assert parser.condition_node.parent is None


def test_condition_parser_with_spaces():
    source = "variable1   ==    value1"

    expected = ConditionNode(
        variable="variable1",
        comparison="==",
        value="value1",
        info=NodeInfo(
            context=generate_context(0, 0, 0, 24),
        ),
        parent=None,
    )

    parser = runner(source)

    assert parser.condition_node.variable == expected.variable
    assert parser.condition_node.comparison == expected.comparison
    assert parser.condition_node.value == expected.value
    assert parser.condition_node.info.asdict() == expected.info.asdict()
    assert parser.condition_node.parent is None
