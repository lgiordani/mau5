from unittest.mock import Mock

import pytest

from mau.environment.environment import Environment
from mau.lexers.base_lexer import BaseLexer
from mau.parsers.base_parser import (
    BaseParser,
    MauParserException,
    TokenError,
    format_parser_error,
)
from mau.test_helpers import dedent, init_parser_factory
from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType

init_parser = init_parser_factory(BaseLexer, BaseParser)


def test_save():
    parent_node = Mock()
    node = Mock()
    parser = BaseParser(Environment(), parent_node=parent_node)

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


def test_format_parser_error_with_token():
    test_message = "A test message"
    test_token = Token(TokenType.TEXT, "Some token", Context(42, 24, "source.py"))

    exception = MauParserException(test_message, test_token)

    expected = dedent(
        """
        ######################################
        ## Parser error

        Message: A test message

        Token: TEXT
        Line: 42
        Column: 24
        Source: source.py

        Some token
        """
    )

    assert format_parser_error(exception) == expected


def test_initial_state():
    parser = init_parser("", Environment())

    assert parser.index == -1
    assert parser._current_token == Token(TokenType.EOF)


def test_current_token_if_no_tokens():
    parser = init_parser("", Environment())
    parser.tokens = []

    with pytest.raises(TokenError):
        parser._current_token  # pylint: disable=pointless-statement


def test_advance_past_end():
    parser = init_parser("", Environment())

    # Advance to index 0 (EOF)
    parser._advance()

    # Advance to index 1 (past the end)
    parser._advance()

    # Advance again
    parser._advance()

    assert parser.index == 1


def test_put_token():
    parser = init_parser("", Environment())

    parser._put_token(Token(TokenType.LITERAL, "*"))
    assert parser.tokens == [
        Token(TokenType.LITERAL, "*"),
        Token(TokenType.EOF),
    ]


def test_get_token():
    mock_check_token = Mock()
    parser = init_parser("", Environment())

    parser._check_token = mock_check_token

    parser._get_token()

    assert parser.index == 0
    mock_check_token.assert_called_once()


def test_get_token_sets_current_token():
    parser = init_parser("Some text", Environment())

    assert parser._get_token() == Token(TokenType.TEXT, "Some text")
    assert parser._current_token == Token(TokenType.TEXT, "Some text")


def test_get_token_can_check_value_with_function():
    parser = init_parser("Some text", Environment())

    # Next token is Token(TokenType.TEXT, "Some text")
    parser._get_token(value_check_function=lambda x: x == "Some text")

    # Failed attempts don't increase the index
    assert parser.index == 0

    # Next token is Token(TokenType.EOL, "")
    with pytest.raises(TokenError):
        parser._get_token(value_check_function=lambda x: x == "foobar")

    # Failed attempts don't increase the index
    assert parser.index == 0


def test_check_token_checks_type():
    parser = init_parser("", Environment())

    parser._check_token(Token(TokenType.TEXT), TokenType.TEXT)

    with pytest.raises(TokenError):
        parser._check_token(Token(TokenType.TEXT), TokenType.EOL)


def test_check_token_checks_type_and_value():
    parser = init_parser("", Environment())

    parser._check_token(
        Token(TokenType.TEXT, "Some text"),
        TokenType.TEXT,
        "Some text",
    )

    with pytest.raises(TokenError):
        parser._check_token(
            Token(TokenType.TEXT, "Some text"),
            TokenType.TEXT,
            "Some other text",
        )


def test_check_token_accepts_check_function():
    parser = init_parser("", Environment())

    parser._check_token(
        Token(TokenType.TEXT, "foobar"),
        TokenType.TEXT,
        value_check_function=lambda x: x == "foobar",
    )

    with pytest.raises(TokenError):
        parser._check_token(
            Token(TokenType.TEXT, "Some text"),
            TokenType.TEXT,
            value_check_function=lambda x: x == "foobar",
        )


def test_check_current_token():
    parser = init_parser("Some text", Environment())
    parser._check_token = Mock()

    parser._get_token()
    parser._check_current_token(TokenType.TEXT)

    parser._check_token.assert_called_with(
        Token(TokenType.TEXT, "Some text"), TokenType.TEXT, None, None
    )


def test_check_current_token_if_no_tokens():
    parser = init_parser("Some text", Environment())
    parser.tokens = []

    with pytest.raises(TokenError):
        parser._check_current_token(TokenType.TEXT)


def test_peek_token():
    parser = init_parser("Some text", Environment())

    assert parser._peek_token() == Token(TokenType.TEXT, "Some text")

    # Peeking doesn't advance the index.
    assert parser.index == -1

    parser._get_token()
    assert parser._peek_token() == Token(TokenType.EOL)

    parser._get_token()
    assert parser._peek_token() == Token(TokenType.EOF)


def test_base_lexer_can_peek_after_eof():
    parser = init_parser("Some text", Environment())

    # Get "Some text".
    parser._get_token()

    # Get "EOL".
    parser._get_token()

    # Get "EOF".
    parser._get_token()

    assert parser._peek_token() == Token(TokenType.EOF)


def test_peek_token_checks_type():
    parser = init_parser("Some text", Environment())

    assert parser._peek_token(TokenType.TEXT) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        parser._peek_token(TokenType.EOL)


def test_peek_token_checks_type_and_value():
    parser = init_parser("Some text", Environment())

    assert parser._peek_token(
        TokenType.TEXT,
        "Some text",
    ) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        parser._peek_token(
            TokenType.EOL,
            "",
        )


def test_peek_token_accepts_check_function():
    parser = init_parser("Some text", Environment())

    assert parser._peek_token(
        TokenType.TEXT,
        value_check_function=lambda x: x.startswith("Some"),
    ) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        parser._peek_token(
            TokenType.TEXT,
            value_check_function=lambda x: x.startswith("Other"),
        )


def test_parser_as_context_manager():
    parser = init_parser("Some text", Environment())

    with parser:
        assert parser._get_token() == Token(TokenType.TEXT, "Some text")


def test_context_manager_does_not_restore_status_if_no_error():
    parser = init_parser("Some text\nSome other text", Environment())

    with parser:
        assert parser._get_token(TokenType.TEXT, "Some text")
        assert parser._get_token(TokenType.EOL)
        assert parser._get_token(TokenType.TEXT, "Some other text")
        assert parser._get_token(TokenType.EOL)

    assert parser._get_token(TokenType.EOF)


def test_context_manager_restores_status_if_error():
    parser = init_parser("Some text\nSome other text", Environment())

    with parser:
        assert parser._get_token(TokenType.TEXT, "Some text")
        assert parser._get_token(TokenType.TEXT, "Some other text")
        # This is an error, so the context manager
        # should restore the status, basically undoing
        # all the previous actions.
        assert parser._get_token(TokenType.TEXT, "Some final text")

    assert parser._get_token(TokenType.TEXT, "Some text")


def test_context_manager_leaves_exceptions_untouched():
    parser = init_parser("Some text\nSome other text", Environment())

    with pytest.raises(ValueError):
        with parser:
            raise ValueError


def test_context_manager_token_error_exception_is_stopped():
    parser = init_parser("Some text\nSome other text", Environment())

    with parser:
        assert parser._get_token(TokenType.TEXT, "Some text")
        raise TokenError

    assert parser._get_token(TokenType.TEXT, "Some text")


def test_context_manager_nested_success():
    parser = init_parser("Some text\nSome other text", Environment())

    with parser:
        parser._get_token(TokenType.TEXT, "Some text")
        parser._get_token(TokenType.EOL)
        with parser:
            parser._get_token(TokenType.TEXT, "Some other text")
            parser._get_token(TokenType.EOL)

        parser._get_token(TokenType.EOF)

    assert parser._get_token(TokenType.EOF)


def test_context_manager_nested_failure():
    parser = init_parser("Some text\nSome other text", Environment())

    with parser:
        parser._get_token(TokenType.TEXT, "Some text")
        parser._get_token(TokenType.EOL)
        with parser:
            parser._get_token(TokenType.TEXT, "Some text")

        parser._get_token(TokenType.TEXT, "Some other text")
        parser._get_token(TokenType.EOL)

    assert parser._get_token(TokenType.EOF)


def test_peek_token_is():
    parser = init_parser("Some text\nSome other text", Environment())

    assert parser._peek_token_is(TokenType.EOL) is False
    assert parser._peek_token_is(TokenType.TEXT) is True


def test_force_token():
    parser = init_parser("Some text\nSome other text", Environment())

    # Force the token type only
    assert parser._force_token(TokenType.TEXT) == Token(TokenType.TEXT, "Some text")

    # Get the EOL
    parser._get_token()

    # Force the token type and value
    assert parser._force_token(TokenType.TEXT, "Some other text") == Token(
        TokenType.TEXT, "Some other text"
    )

    # At this point the current token is EOL.

    # Force the token type only - wrong type
    with pytest.raises(MauParserException) as exc:
        parser._force_token(TokenType.TEXT)

    # Force the token type and value - wrong value
    with pytest.raises(MauParserException) as exc:
        parser._force_token(TokenType.EOL, "Wrong value")

    # This is the position of the expected token,
    # EOL in this case.
    assert exc.value.token.type == TokenType.EOL
    assert exc.value.token.context == Context(1, 15, "main")


def test_collect():
    parser = init_parser("Some text\nSome other text", Environment())

    # This collects everything up to EOF excluded.
    tokens = parser._collect([Token(TokenType.EOF)])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "Some other text"),
        Token(TokenType.EOL),
    ]

    tokens = parser._collect([Token(TokenType.EOF)])

    assert tokens == []


def test_collect_join():
    parser = init_parser("Some te\nxt that will be joined\n!", Environment())

    expected = "Some text that will be joined!"

    assert parser._collect_join([Token(TokenType.EOF)]) == expected


def test_collect_join_with_different_joiner():
    parser = init_parser("Some te\nxt that will be joined\n!", Environment())

    expected = "Some te-xt that will be joined-!"

    assert parser._collect_join([Token(TokenType.EOF)], "-") == expected


def test_collect_escapes_are_kept():
    parser = init_parser("", Environment())
    parser.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "Some other text"),
        Token(TokenType.EOF),
    ]

    tokens = parser._collect([Token(TokenType.EOF)])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "Some other text"),
    ]


def test_collect_escape_stop_tokens_are_removed():
    parser = init_parser("", Environment())
    parser.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]

    tokens = parser._collect([Token(TokenType.LITERAL, "[")])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "["),
    ]


def test_collect_escape_stop_tokens_are_removed2():
    parser = init_parser("", Environment())
    parser.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]

    tokens = parser._collect(
        [Token(TokenType.LITERAL, "[")], preserve_escaped_stop_tokens=True
    )

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]


def test_error_no_token():
    parser = init_parser("Some text", Environment())

    # This advances to the first token
    parser._get_token()

    with pytest.raises(MauParserException) as exc:
        parser._error("A message")

    assert exc.value.message == "A message"
    assert exc.value.token == Token(TokenType.TEXT, "Some text")


def test_error_with_token():
    parser = init_parser("Some text", Environment())

    with pytest.raises(MauParserException) as exc:
        parser._error("A message", Token(TokenType.TEXT, "Random text"))

    assert exc.value.message == "A message"
    assert exc.value.token == Token(TokenType.TEXT, "Random text")


def test_unknown_token():
    parser = BaseParser(Environment())
    parser.tokens = [Token("UNKNOWN")]

    with pytest.raises(MauParserException) as exc:
        parser.parse()

    assert exc.value.message == "Cannot parse token"
    assert exc.value.token == Token("UNKNOWN", "")
