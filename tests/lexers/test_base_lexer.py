from unittest.mock import Mock

import pytest

from mau.environment.environment import Environment
from mau.lexers.base_lexer import (
    BaseLexer,
    MauLexerException,
    format_lexer_error,
)
from mau.test_helpers import dedent, init_lexer_factory, lexer_runner_factory
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer
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

    assert lex.tokens == [
        Token(TokenType.EOF, ""),
    ]


def test_empty_lines():
    lex = runner("\n")

    assert lex.tokens == [
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_lines_with_only_spaces():
    lex = runner("      \n      ")

    assert lex.tokens == [
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_text():
    text = "Just simple text"
    lex = runner(text)

    assert lex.tokens == [
        Token(TokenType.TEXT, text),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiple_lines():
    text = dedent(
        """
        This is text
        split into multiple lines

        with an empty line
        """
    )
    lex = runner(text)

    assert lex.tokens == [
        Token(TokenType.TEXT, "This is text"),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "split into multiple lines"),
        Token(TokenType.EOL),
        Token(TokenType.EOL),
        Token(TokenType.TEXT, "with an empty line"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_positions_default_context():
    text = dedent(
        """
        This is a line of text

        ---

        This is another line of text
        """
    )
    lex = runner(text)

    assert [i.context.asdict() for i in lex.tokens] == [
        {"column": 0, "line": 0, "source": None},
        {"column": 22, "line": 0, "source": None},
        {"column": 0, "line": 1, "source": None},
        {"column": 0, "line": 2, "source": None},
        {"column": 3, "line": 2, "source": None},
        {"column": 0, "line": 3, "source": None},
        {
            "column": 0,
            "line": 4,
            "source": None,
        },
        {
            "column": 28,
            "line": 4,
            "source": None,
        },
        {
            "column": 0,
            "line": 5,
            "source": None,
        },
    ]


def test_positions():
    text = dedent(
        """
        This is a line of text

        ---

        This is another line of text
        """
    )
    text_buffer = TextBuffer(text, Context(line=42, column=123, source="main"))
    lex = BaseLexer(text_buffer, Environment())
    lex.process()

    assert [i.context.asdict() for i in lex.tokens] == [
        {"column": 123, "line": 42, "source": "main"},
        {"column": 145, "line": 42, "source": "main"},
        {"column": 123, "line": 43, "source": "main"},
        {"column": 123, "line": 44, "source": "main"},
        {"column": 126, "line": 44, "source": "main"},
        {"column": 123, "line": 45, "source": "main"},
        {
            "column": 123,
            "line": 46,
            "source": "main",
        },
        {
            "column": 151,
            "line": 46,
            "source": "main",
        },
        {
            "column": 123,
            "line": 47,
            "source": "main",
        },
    ]
