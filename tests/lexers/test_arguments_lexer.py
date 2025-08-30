from mau.environment.environment import Environment
from mau.lexers.arguments_lexer import ArgumentsLexer
from mau.lexers.base_lexer import TokenType
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer
from mau.tokens.token import Token


def test_single_unnamed_argument():
    text_buffer = TextBuffer("value1")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_single_named_argument():
    text_buffer = TextBuffer("argument1=value1")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiple_unnamed_arguments():
    text_buffer = TextBuffer("value1, value2")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_multiple_named_arguments():
    text_buffer = TextBuffer("argument1=value1, argument2=value2")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "argument2"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_mixed_arguments():
    text_buffer = TextBuffer("value1, value2,argument1=value1, argument2=value2")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "argument2"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_quotes():
    text_buffer = TextBuffer('argument1="value1,value2"')
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.LITERAL, ","),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_spaces():
    text_buffer = TextBuffer("argument1=value1 value2")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "value2"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_quotes():
    text_buffer = TextBuffer(r"Argument \"with\" quotes")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "Argument"),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.TEXT, "with"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.WHITESPACE, " "),
        Token(TokenType.TEXT, "quotes"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_context():
    text_buffer = TextBuffer("argument1=value1")
    lex = ArgumentsLexer(text_buffer, Environment())
    lex.process()

    assert lex.tokens == [
        Token(TokenType.TEXT, "argument1"),
        Token(TokenType.LITERAL, "="),
        Token(TokenType.TEXT, "value1"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]

    assert [t.context for t in lex.tokens] == [
        Context(line=0, column=0),
        Context(line=0, column=9),
        Context(line=0, column=10),
        Context(line=0, column=16),
        Context(line=1, column=0),
    ]
