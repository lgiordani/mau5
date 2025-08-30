from mau.lexers.text_lexer import TextLexer
from mau.test_helpers import init_lexer_factory, lexer_runner_factory
from mau.tokens.token import Token, TokenType

init_lexer = init_lexer_factory(TextLexer)

runner = lexer_runner_factory(TextLexer)


def test_normal_text():
    lex = runner("Normal text")

    assert lex.tokens == [
        Token(TokenType.TEXT, "Normal"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "text"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_underscore():
    lex = runner("_underscore_")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "_"),
        Token(TokenType.TEXT, "underscore"),
        Token(TokenType.LITERAL, "_"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_star():
    lex = runner("*star*")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "*"),
        Token(TokenType.TEXT, "star"),
        Token(TokenType.LITERAL, "*"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_caret():
    lex = runner("^caret^")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "^"),
        Token(TokenType.TEXT, "caret"),
        Token(TokenType.LITERAL, "^"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_tilde():
    lex = runner("~tilde~")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "~"),
        Token(TokenType.TEXT, "tilde"),
        Token(TokenType.LITERAL, "~"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_backtick():
    lex = runner("`backtick`")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.TEXT, "backtick"),
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_dollar():
    lex = runner("$dollar$")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "$"),
        Token(TokenType.TEXT, "dollar"),
        Token(TokenType.LITERAL, "$"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_percent():
    lex = runner("%percent%")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "%"),
        Token(TokenType.TEXT, "percent"),
        Token(TokenType.LITERAL, "%"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_curly_braces():
    lex = runner("{curly}")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "{"),
        Token(TokenType.TEXT, "curly"),
        Token(TokenType.LITERAL, "}"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_round_brackets():
    lex = runner("(round)")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "("),
        Token(TokenType.TEXT, "round"),
        Token(TokenType.LITERAL, ")"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_square_brackets():
    lex = runner("[square]")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "["),
        Token(TokenType.TEXT, "square"),
        Token(TokenType.LITERAL, "]"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_macro():
    lex = runner("[macro](value1,value2)")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "["),
        Token(TokenType.TEXT, "macro"),
        Token(TokenType.LITERAL, "]"),
        Token(TokenType.LITERAL, "("),
        Token(TokenType.TEXT, "value1,value2"),
        Token(TokenType.LITERAL, ")"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_macro_named_attributes():
    lex = runner("[macro](attr1=value1,attr2=value2)")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "["),
        Token(TokenType.TEXT, "macro"),
        Token(TokenType.LITERAL, "]"),
        Token(TokenType.LITERAL, "("),
        Token(TokenType.TEXT, "attr1=value1,attr2=value2"),
        Token(TokenType.LITERAL, ")"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_underscore():
    lex = runner(r"\_underscore\_")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "_"),
        Token(TokenType.TEXT, "underscore"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "_"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_square_brackets():
    lex = runner(r"\[square\]")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "["),
        Token(TokenType.TEXT, "square"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "]"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_round_brackets():
    lex = runner(r"\(round\)")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "("),
        Token(TokenType.TEXT, "round"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, ")"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_curly_braces():
    lex = runner(r"\{curly\}")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "{"),
        Token(TokenType.TEXT, "curly"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "}"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_quotes():
    lex = runner(r"\"quotes\"")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.TEXT, "quotes"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, '"'),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_backticks():
    lex = runner(r"\`backticks\`")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.TEXT, "backticks"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_dollar():
    lex = runner(r"\$dollar\$")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "$"),
        Token(TokenType.TEXT, "dollar"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "$"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escaped_percent():
    lex = runner(r"\%pecent\%")

    assert lex.tokens == [
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "%"),
        Token(TokenType.TEXT, "pecent"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "%"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]
