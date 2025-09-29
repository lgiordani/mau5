from unittest.mock import Mock

import pytest


from mau.environment.environment import Environment
from mau.lexers.base_lexer.lexer import BaseLexer
from mau.parsers.base_parser.managers.tokens_manager import TokenError, TokensManager
from mau.test_helpers import (
    generate_context,
    init_tokens_manager_factory,
)
from mau.tokens.token import Token, TokenType

init_tokens_manager = init_tokens_manager_factory(BaseLexer, TokensManager)


def test_initial_state():
    tm = init_tokens_manager("", Environment())

    assert tm.index == -1
    assert tm.current_token == Token(TokenType.EOF)


def test_current_token_if_no_tokens():
    tm = init_tokens_manager("", Environment())
    tm.tokens = []

    with pytest.raises(TokenError):
        tm.current_token  # pylint: disable=pointless-statement


def test_advance_past_end():
    tm = init_tokens_manager("", Environment())

    # Advance to index 0 (EOF)
    tm._advance()

    # Advance to index 1 (past the end)
    tm._advance()

    # Advance again
    tm._advance()

    assert tm.index == 1


def test_get_token():
    mock_check_token = Mock()
    tm = init_tokens_manager("", Environment())

    tm._check_token = mock_check_token

    tm.get_token()

    assert tm.index == 0
    mock_check_token.assert_called_once()


def test_get_token_sets_current_token():
    tm = init_tokens_manager("Some text", Environment())

    assert tm.get_token() == Token(TokenType.TEXT, "Some text")
    assert tm.current_token == Token(TokenType.TEXT, "Some text")


def test_get_token_can_check_value_with_function():
    tm = init_tokens_manager("Some text", Environment())

    # Next token is Token(TokenType.TEXT, "Some text")
    tm.get_token(value_check_function=lambda x: x == "Some text")

    # Failed attempts don't increase the index
    assert tm.index == 0

    # Next token is Token(TokenType.EOL, "")
    with pytest.raises(TokenError):
        tm.get_token(value_check_function=lambda x: x == "foobar")

    # Failed attempts don't increase the index
    assert tm.index == 0


def test_check_token_checks_type():
    tm = init_tokens_manager("", Environment())

    tm._check_token(Token(TokenType.TEXT), TokenType.TEXT)

    with pytest.raises(TokenError):
        tm._check_token(Token(TokenType.TEXT), TokenType.EOL)


def test_check_token_checks_type_and_value():
    tm = init_tokens_manager("", Environment())

    tm._check_token(
        Token(TokenType.TEXT, "Some text"),
        TokenType.TEXT,
        "Some text",
    )

    with pytest.raises(TokenError):
        tm._check_token(
            Token(TokenType.TEXT, "Some text"),
            TokenType.TEXT,
            "Some other text",
        )


def test_check_token_accepts_check_function():
    tm = init_tokens_manager("", Environment())

    tm._check_token(
        Token(TokenType.TEXT, "foobar"),
        TokenType.TEXT,
        value_check_function=lambda x: x == "foobar",
    )

    with pytest.raises(TokenError):
        tm._check_token(
            Token(TokenType.TEXT, "Some text"),
            TokenType.TEXT,
            value_check_function=lambda x: x == "foobar",
        )


def test_peek_token():
    tm = init_tokens_manager("Some text", Environment())

    assert tm.peek_token() == Token(TokenType.TEXT, "Some text")

    # Peeking doesn't advance the index.
    assert tm.index == -1

    tm.get_token()
    assert tm.peek_token() == Token(TokenType.EOF)


def test_base_lexer_can_peek_after_eof():
    tm = init_tokens_manager("Some text", Environment())

    # Get "Some text".
    tm.get_token()

    # Get "EOL".
    tm.get_token()

    # Get "EOF".
    tm.get_token()

    assert tm.peek_token() == Token(TokenType.EOF)


def test_peek_token_checks_type():
    tm = init_tokens_manager("Some text", Environment())

    assert tm.peek_token(TokenType.TEXT) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        tm.peek_token(TokenType.EOL)


def test_peek_token_checks_type_and_value():
    tm = init_tokens_manager("Some text", Environment())

    assert tm.peek_token(
        TokenType.TEXT,
        "Some text",
    ) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        tm.peek_token(
            TokenType.EOL,
            "",
        )


def test_peek_token_accepts_check_function():
    tm = init_tokens_manager("Some text", Environment())

    assert tm.peek_token(
        TokenType.TEXT,
        value_check_function=lambda x: x.startswith("Some"),
    ) == Token(TokenType.TEXT, "Some text")

    with pytest.raises(TokenError):
        tm.peek_token(
            TokenType.TEXT,
            value_check_function=lambda x: x.startswith("Other"),
        )


def test_context_manager():
    tm = init_tokens_manager("Some text", Environment())

    with tm:
        assert tm.get_token() == Token(TokenType.TEXT, "Some text")


def test_context_manager_does_not_restore_status_if_no_error():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with tm:
        assert tm.get_token(TokenType.TEXT, "Some text")
        assert tm.get_token(TokenType.TEXT, "Some other text")

    assert tm.get_token(TokenType.EOF)


def test_context_manager_restores_status_if_error():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with tm:
        assert tm.get_token(TokenType.TEXT, "Some text")
        assert tm.get_token(TokenType.TEXT, "Some other text")
        # This is an error, so the context manager
        # should restore the status, basically undoing
        # all the previous actions.
        assert tm.get_token(TokenType.TEXT, "Some final text")

    assert tm.get_token(TokenType.TEXT, "Some text")


def test_context_manager_leaves_exceptions_untouched():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with pytest.raises(ValueError):
        with tm:
            raise ValueError


def test_context_manager_token_error_exception_is_stopped():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with tm:
        assert tm.get_token(TokenType.TEXT, "Some text")
        raise TokenError

    assert tm.get_token(TokenType.TEXT, "Some text")


def test_context_manager_nested_success():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with tm:
        tm.get_token(TokenType.TEXT, "Some text")
        with tm:
            tm.get_token(TokenType.TEXT, "Some other text")

        tm.get_token(TokenType.EOF)

    assert tm.get_token(TokenType.EOF)


def test_context_manager_nested_failure():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    with tm:
        tm.get_token(TokenType.TEXT, "Some text")
        with tm:
            tm.get_token(TokenType.TEXT, "Some text")

        tm.get_token(TokenType.TEXT, "Some other text")

    assert tm.get_token(TokenType.EOF)


def test_peek_token_is():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    assert tm.peek_token_is(TokenType.EOL) is False
    assert tm.peek_token_is(TokenType.TEXT) is True


def test_collect():
    tm = init_tokens_manager("Some text\nSome other text", Environment())

    # This collects everything up to EOF excluded.
    tokens = tm.collect([Token(TokenType.EOF)])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.TEXT, "Some other text"),
    ]

    tokens = tm.collect([Token(TokenType.EOF)])

    assert tokens == []


def test_collect_join():
    tm = init_tokens_manager("Some te\nxt that will be joined\n!", Environment())

    expected = Token(
        TokenType.TEXT,
        "Some text that will be joined!",
        context=generate_context(0, 0, 2, 1),
    )

    assert tm.collect_join([Token(TokenType.EOF)]) == expected


def test_collect_join_with_different_joiner():
    tm = init_tokens_manager("Some te\nxt that will be joined\n!", Environment())

    expected = Token(
        TokenType.TEXT,
        "Some te-xt that will be joined-!",
        context=generate_context(0, 0, 2, 1),
    )

    assert tm.collect_join([Token(TokenType.EOF)], "-") == expected


def test_collect_escapes_are_kept():
    tm = init_tokens_manager("", Environment())
    tm.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "Some other text"),
        Token(TokenType.EOF),
    ]

    tokens = tm.collect([Token(TokenType.EOF)])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "Some other text"),
    ]


def test_collect_escape_stop_tokens_are_removed():
    tm = init_tokens_manager("", Environment())
    tm.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]

    tokens = tm.collect([Token(TokenType.LITERAL, "[")])

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "["),
    ]


def test_collect_escape_stop_tokens_are_removed2():
    tm = init_tokens_manager("", Environment())
    tm.tokens = [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]

    tokens = tm.collect(
        [Token(TokenType.LITERAL, "[")], preserve_escaped_stop_tokens=True
    )

    assert tokens == [
        Token(TokenType.TEXT, "Some text"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
    ]
