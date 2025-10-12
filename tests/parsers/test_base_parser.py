from functools import partial
from unittest.mock import Mock, patch

import pytest

from mau.environment.environment import Environment
from mau.lexers.base_lexer import BaseLexer
from mau.parsers.base_parser import (
    BaseParser,
    MauParserException,
    recursive_check_nodes,
)
from mau.parsers.managers.tokens_manager import TokenError
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
)
from mau.token import Token, TokenType

init_parser = init_parser_factory(BaseLexer, BaseParser)


def test_save():
    parent_node = Mock()
    node = Mock()
    parser = BaseParser([], Environment(), parent_node=parent_node)

    parser._save(node)

    assert parser.nodes == [node]
    node.set_parent.assert_called_with(parent_node)


def test_unknown_token():
    test_context = generate_context(0, 0, 0, 0)
    test_token = Token(TokenType.EOL, "", test_context)

    parser = BaseParser([test_token], Environment())

    with pytest.raises(MauParserException) as exc:
        parser.parse()

    assert exc.value.message == "Cannot parse token"
    assert exc.value.context is test_context


def test_process_functions_token_error():
    process_test = Mock()
    process_test.side_effect = TokenError

    def process_functions():
        return [process_test]

    test_context = generate_context(0, 0, 0, 0)
    test_token = Token(TokenType.EOL, "", test_context)

    parser = BaseParser([test_token], Environment())
    parser._process_functions = process_functions

    with pytest.raises(MauParserException):
        parser.parse()

    process_test.assert_called()


def test_process_functions_success():
    process_test = Mock()
    process_test.return_value = True

    def process_functions():
        return [process_test]

    test_context = generate_context(0, 0, 0, 0)
    test_token = Token(TokenType.EOL, "", test_context)

    parser = BaseParser([test_token], Environment())
    parser._process_functions = process_functions

    with pytest.raises(MauParserException):
        parser.parse()

    process_test.assert_called()


@patch("mau.parsers.base_parser.recursive_check_nodes")
def test_recursive_check_nodes_is_called(mock_recursive_check_nodes):
    test_context = generate_context(0, 0, 0, 0)
    test_token1 = Token(TokenType.TEXT, "sometext", test_context)
    test_token2 = Token(TokenType.EOF, "", test_context)

    def process_test(parser: BaseParser):
        parser.tm.get_token(TokenType.TEXT)
        return True

    parser = BaseParser([test_token1, test_token2], Environment())

    def process_functions():
        return [partial(process_test, parser)]

    parser._process_functions = process_functions

    parser.parse()

    mock_recursive_check_nodes.assert_called_with(parser.nodes)


def test_recursive_check_nodes_empty():
    assert recursive_check_nodes([]) is None


def test_recursive_check_nodes_good_nodes():
    node1 = Mock()
    node1.check_children.return_value = set()
    node1.children = {}

    node2 = Mock()
    node2.check_children.return_value = set()
    node2.children = {}

    assert recursive_check_nodes([node1, node2]) is None
    node1.check_children.assert_called_once()
    node2.check_children.assert_called_once()


def test_recursive_check_nodes_bad_nodes():
    node1 = Mock()
    node1.check_children.return_value = set()
    node1.children = {}

    node2 = Mock()
    node2.check_children.return_value = set([node1])

    with pytest.raises(ValueError):
        recursive_check_nodes([node2])
    node1.check_children.assert_not_called()
    node2.check_children.assert_called_once()


def test_recursive_check_nodes_checks_children():
    node1 = Mock()
    node1.check_children.return_value = set()
    node1.children = {}

    node2 = Mock()
    node2.check_children.return_value = set()
    node2.children = {"somelabel": [node1]}

    assert recursive_check_nodes([node2]) is None
    node1.check_children.assert_called_once()
    node2.check_children.assert_called_once()
