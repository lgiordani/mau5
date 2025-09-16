from mau.lexers.text_lexer.lexer import TextLexer
from mau.test_helpers import (
    compare_tokens,
    generate_context,
    init_lexer_factory,
    lexer_runner_factory,
)
from mau.tokens.token import Token, TokenType

init_lexer = init_lexer_factory(TextLexer)

runner = lexer_runner_factory(TextLexer)


def test_normal_text():
    lex = runner("Normal text")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "Normal", generate_context(0, 0)),
            Token(TokenType.TEXT, " ", generate_context(0, 6)),
            Token(TokenType.TEXT, "text", generate_context(0, 7)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_underscore():
    lex = runner("_underscore_")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "_", generate_context(0, 0)),
            Token(TokenType.TEXT, "underscore", generate_context(0, 1)),
            Token(TokenType.LITERAL, "_", generate_context(0, 11)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_star():
    lex = runner("*star*")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "*", generate_context(0, 0)),
            Token(TokenType.TEXT, "star", generate_context(0, 1)),
            Token(TokenType.LITERAL, "*", generate_context(0, 5)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_caret():
    lex = runner("^caret^")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "^", generate_context(0, 0)),
            Token(TokenType.TEXT, "caret", generate_context(0, 1)),
            Token(TokenType.LITERAL, "^", generate_context(0, 6)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_tilde():
    lex = runner("~tilde~")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "~", generate_context(0, 0)),
            Token(TokenType.TEXT, "tilde", generate_context(0, 1)),
            Token(TokenType.LITERAL, "~", generate_context(0, 6)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_backtick():
    lex = runner("`backtick`")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "`", generate_context(0, 0)),
            Token(TokenType.TEXT, "backtick", generate_context(0, 1)),
            Token(TokenType.LITERAL, "`", generate_context(0, 9)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_dollar():
    lex = runner("$dollar$")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "$", generate_context(0, 0)),
            Token(TokenType.TEXT, "dollar", generate_context(0, 1)),
            Token(TokenType.LITERAL, "$", generate_context(0, 7)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_percent():
    lex = runner("%percent%")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "%", generate_context(0, 0)),
            Token(TokenType.TEXT, "percent", generate_context(0, 1)),
            Token(TokenType.LITERAL, "%", generate_context(0, 8)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_curly_braces():
    lex = runner("{curly}")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "{", generate_context(0, 0)),
            Token(TokenType.TEXT, "curly", generate_context(0, 1)),
            Token(TokenType.LITERAL, "}", generate_context(0, 6)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_round_brackets():
    lex = runner("(round)")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "(", generate_context(0, 0)),
            Token(TokenType.TEXT, "round", generate_context(0, 1)),
            Token(TokenType.LITERAL, ")", generate_context(0, 6)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_square_brackets():
    lex = runner("[square]")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "[", generate_context(0, 0)),
            Token(TokenType.TEXT, "square", generate_context(0, 1)),
            Token(TokenType.LITERAL, "]", generate_context(0, 7)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_macro():
    lex = runner("[macro](value1,value2)")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "[", generate_context(0, 0)),
            Token(TokenType.TEXT, "macro", generate_context(0, 1)),
            Token(TokenType.LITERAL, "]", generate_context(0, 6)),
            Token(TokenType.LITERAL, "(", generate_context(0, 7)),
            Token(TokenType.TEXT, "value1,value2", generate_context(0, 8)),
            Token(TokenType.LITERAL, ")", generate_context(0, 21)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_macro_named_arguments():
    lex = runner("[macro](attr1=value1,attr2=value2)")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "[", generate_context(0, 0)),
            Token(TokenType.TEXT, "macro", generate_context(0, 1)),
            Token(TokenType.LITERAL, "]", generate_context(0, 6)),
            Token(TokenType.LITERAL, "(", generate_context(0, 7)),
            Token(TokenType.TEXT, "attr1=value1,attr2=value2", generate_context(0, 8)),
            Token(TokenType.LITERAL, ")", generate_context(0, 33)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_underscore():
    lex = runner(r"\_underscore\_")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "_", generate_context(0, 1)),
            Token(TokenType.TEXT, "underscore", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 12)),
            Token(TokenType.LITERAL, "_", generate_context(0, 13)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_square_brackets():
    lex = runner(r"\[square\]")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "[", generate_context(0, 1)),
            Token(TokenType.TEXT, "square", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 8)),
            Token(TokenType.LITERAL, "]", generate_context(0, 9)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_round_brackets():
    lex = runner(r"\(round\)")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "(", generate_context(0, 1)),
            Token(TokenType.TEXT, "round", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 7)),
            Token(TokenType.LITERAL, ")", generate_context(0, 8)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_curly_braces():
    lex = runner(r"\{curly\}")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "{", generate_context(0, 1)),
            Token(TokenType.TEXT, "curly", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 7)),
            Token(TokenType.LITERAL, "}", generate_context(0, 8)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_quotes():
    lex = runner(r"\"quotes\"")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, '"', generate_context(0, 1)),
            Token(TokenType.TEXT, "quotes", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 8)),
            Token(TokenType.LITERAL, '"', generate_context(0, 9)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_backticks():
    lex = runner(r"\`backticks\`")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "`", generate_context(0, 1)),
            Token(TokenType.TEXT, "backticks", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 11)),
            Token(TokenType.LITERAL, "`", generate_context(0, 12)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_dollar():
    lex = runner(r"\$dollar\$")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "$", generate_context(0, 1)),
            Token(TokenType.TEXT, "dollar", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 8)),
            Token(TokenType.LITERAL, "$", generate_context(0, 9)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )


def test_escaped_percent():
    lex = runner(r"\%percent\%")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.LITERAL, "\\", generate_context(0, 0)),
            Token(TokenType.LITERAL, "%", generate_context(0, 1)),
            Token(TokenType.TEXT, "percent", generate_context(0, 2)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 9)),
            Token(TokenType.LITERAL, "%", generate_context(0, 10)),
            Token(TokenType.EOF, "", generate_context(1, 0)),
        ],
    )
