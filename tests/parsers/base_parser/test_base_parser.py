from unittest.mock import Mock, mock_open, patch

import pytest

from mau.environment.environment import Environment
from mau.lexers.base_lexer.lexer import BaseLexer
from mau.parsers.base_parser.parser import (
    BaseParser,
    MauParserException,
    format_parser_error,
)
from mau.test_helpers import (
    compare_text_lines,
    dedent,
    generate_context,
    init_parser_factory,
)
from mau.tokens.token import Token, TokenType

init_parser = init_parser_factory(BaseLexer, BaseParser)


def test_save():
    parent_node = Mock()
    node = Mock()
    parser = BaseParser([], Environment(), parent_node=parent_node)

    parser._save(node)

    assert parser.nodes == [node]
    node.set_parent.assert_called_with(parent_node)


def test_format_parser_error():
    test_message = "A test message"

    exception = MauParserException(test_message)

    expected = dedent(
        """
        ######################################
        ## Parser error

        Message: A test message
        """
    )

    assert format_parser_error(exception) == expected


@patch("builtins.open", new_callable=mock_open, read_data="just some data")
def test_format_parser_error_with_context(mock_open):
    test_message = "A test message"
    test_context = generate_context(0, 5, 0, 9)

    exception = MauParserException(test_message, test_context)

    expected = dedent(
        """
        ######################################
        ## Parser error

        Message: A test message

        test.py:0,5-0,9

        just some data
             ^^^^
        """
    )

    compare_text_lines(format_parser_error(exception), expected)


def test_unknown_token():
    test_context = generate_context(42, 24)
    test_token = Token(TokenType.EOL, "", test_context)

    parser = BaseParser([test_token], Environment())

    with pytest.raises(MauParserException) as exc:
        parser.parse()

    assert exc.value.message == "Cannot parse token"
    assert exc.value.context is test_context
