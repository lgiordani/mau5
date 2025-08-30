from mau.lexers.base_lexer import TokenType
from mau.lexers.preprocess_variables_lexer import PreprocessVariablesLexer
from mau.test_helpers import init_lexer_factory, lexer_runner_factory
from mau.tokens.token import Token

init_lexer = init_lexer_factory(PreprocessVariablesLexer)

runner = lexer_runner_factory(PreprocessVariablesLexer)


def test_normal_text():
    lex = runner("Some text")

    assert lex.tokens == [
        Token(TokenType.TEXT, "S"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "m"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_match_only_backticks_and_curly_braces():
    lex = runner("Normal text `{curly}` _other_ *text*")

    assert lex.tokens == [
        Token(TokenType.TEXT, "N"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "m"),
        Token(TokenType.TEXT, "a"),
        Token(TokenType.TEXT, "l"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.LITERAL, "{"),
        Token(TokenType.TEXT, "c"),
        Token(TokenType.TEXT, "u"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "l"),
        Token(TokenType.TEXT, "y"),
        Token(TokenType.LITERAL, "}"),
        Token(TokenType.LITERAL, "`"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "h"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "*"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "*"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_escape_curly_braces():
    lex = runner(r"Normal text \{curly\} _other_ *text*")

    assert lex.tokens == [
        Token(TokenType.TEXT, "N"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "m"),
        Token(TokenType.TEXT, "a"),
        Token(TokenType.TEXT, "l"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "{"),
        Token(TokenType.TEXT, "c"),
        Token(TokenType.TEXT, "u"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "l"),
        Token(TokenType.TEXT, "y"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.LITERAL, "}"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "h"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.TEXT, "*"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "*"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]


def test_preserve_escapes():
    lex = runner(r"Normal \text \_other\_")

    assert lex.tokens == [
        Token(TokenType.TEXT, "N"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.TEXT, "m"),
        Token(TokenType.TEXT, "a"),
        Token(TokenType.TEXT, "l"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "x"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, " "),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.TEXT, "o"),
        Token(TokenType.TEXT, "t"),
        Token(TokenType.TEXT, "h"),
        Token(TokenType.TEXT, "e"),
        Token(TokenType.TEXT, "r"),
        Token(TokenType.LITERAL, "\\"),
        Token(TokenType.TEXT, "_"),
        Token(TokenType.EOL),
        Token(TokenType.EOF),
    ]
