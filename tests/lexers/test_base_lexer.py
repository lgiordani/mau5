from unittest.mock import Mock

import pytest

from mau.environment.environment import Environment
from mau.lexers.base_lexer.lexer import (
    BaseLexer,
    MauLexerException,
    format_lexer_error,
)
from mau.test_helpers import (
    compare_tokens,
    dedent,
    generate_context,
    init_lexer_factory,
    lexer_runner_factory,
)
from mau.text_buffer.context import Context
from mau.tokens.token import Token, TokenType

init_lexer = init_lexer_factory(BaseLexer)

runner = lexer_runner_factory(BaseLexer)


def test_format_lexer_error():
    test_message = "A test message"

    exception = MauLexerException(test_message)

    expected = dedent(
        """
        ######################################
        ## Lexer error
        
        Message: A test message
        """
    )

    assert format_lexer_error(exception) == expected


def test_format_lexer_error_with_token():
    test_message = "A test message"
    test_context = Context(42, 24, "source.py")

    exception = MauLexerException(test_message, context=test_context)

    expected = dedent(
        """
        ######################################
        ## Lexer error

        Message: A test message

        Line: 42
        Column: 24
        Source: source.py
        """
    )

    assert format_lexer_error(exception) == expected


def test_text_buffer_properties():
    mock_text_buffer = Mock()
    lex = BaseLexer(mock_text_buffer, Environment())

    assert lex._current_char == mock_text_buffer.current_char

    assert lex._current_line == mock_text_buffer.current_line

    assert lex._tail == mock_text_buffer.tail

    lex._nextline()
    mock_text_buffer.nextline.assert_called()

    lex._skip("four")
    mock_text_buffer.skip.assert_called_with(4)


def test_create_token_and_skip():
    mock_text_buffer = Mock()
    lex = BaseLexer(mock_text_buffer, Environment())
    lex._skip = Mock()

    token = lex._create_token_and_skip("sometype", "somevalue")
    assert token == Token("sometype", "somevalue")
    lex._skip.assert_called_with("somevalue")


def test_error():
    mock_text_buffer = Mock()
    lex = BaseLexer(mock_text_buffer, Environment())

    with pytest.raises(MauLexerException):
        lex._process_error()


def test_empty_text():
    lex = runner("")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.EOF, "", generate_context(0, 0)),
        ],
    )


def test_empty_lines():
    lex = runner("\n")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.EOL, "", generate_context(0, 0)),
            Token(TokenType.EOL, "", generate_context(1, 0)),
            Token(TokenType.EOF, "", generate_context(2, 0)),
        ],
    )


def test_lines_with_only_spaces():
    lex = runner("      \n      ")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.EOL, "", generate_context(0, 0)),
            Token(TokenType.EOL, "", generate_context(1, 0)),
            Token(TokenType.EOF, "", generate_context(2, 0)),
        ],
    )


def test_text():
    lex = runner("Just simple text")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "Just simple text", generate_context(0, 0)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_multiple_lines():
    text = dedent(
        """
        This is text
        split into multiple lines

        with an empty line
        """
    )
    lex = runner(text)

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "This is text", generate_context(0, 0)),
            Token(TokenType.TEXT, "split into multiple lines", generate_context(1, 0)),
            Token(TokenType.EOL, "", generate_context(2, 0)),
            Token(TokenType.TEXT, "with an empty line", generate_context(3, 0)),
            Token(TokenType.EOF, "", generate_context(4, 0)),
        ],
    )
