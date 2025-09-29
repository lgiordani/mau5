from mau.lexers.base_lexer.lexer import TokenType
from mau.lexers.preprocess_variables_lexer.lexer import PreprocessVariablesLexer
from mau.test_helpers import (
    compare_tokens,
    generate_context,
    init_lexer_factory,
    lexer_runner_factory,
)
from mau.tokens.token import Token

init_lexer = init_lexer_factory(PreprocessVariablesLexer)

runner = lexer_runner_factory(PreprocessVariablesLexer)


def test_normal_text():
    lex = runner("Some text")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "S", generate_context(0, 0, 0, 1)),
            Token(TokenType.TEXT, "o", generate_context(0, 1, 0, 2)),
            Token(TokenType.TEXT, "m", generate_context(0, 2, 0, 3)),
            Token(TokenType.TEXT, "e", generate_context(0, 3, 0, 4)),
            Token(TokenType.TEXT, " ", generate_context(0, 4, 0, 5)),
            Token(TokenType.TEXT, "t", generate_context(0, 5, 0, 6)),
            Token(TokenType.TEXT, "e", generate_context(0, 6, 0, 7)),
            Token(TokenType.TEXT, "x", generate_context(0, 7, 0, 8)),
            Token(TokenType.TEXT, "t", generate_context(0, 8, 0, 9)),
            Token(TokenType.EOF, "", generate_context(0, 9, 0, 9)),
        ],
    )


def test_match_only_backticks_and_curly_braces():
    lex = runner("Normal text `{curly}` _other_ *text*")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "N", generate_context(0, 0, 0, 1)),
            Token(TokenType.TEXT, "o", generate_context(0, 1, 0, 2)),
            Token(TokenType.TEXT, "r", generate_context(0, 2, 0, 3)),
            Token(TokenType.TEXT, "m", generate_context(0, 3, 0, 4)),
            Token(TokenType.TEXT, "a", generate_context(0, 4, 0, 5)),
            Token(TokenType.TEXT, "l", generate_context(0, 5, 0, 6)),
            Token(TokenType.TEXT, " ", generate_context(0, 6, 0, 7)),
            Token(TokenType.TEXT, "t", generate_context(0, 7, 0, 8)),
            Token(TokenType.TEXT, "e", generate_context(0, 8, 0, 9)),
            Token(TokenType.TEXT, "x", generate_context(0, 9, 0, 10)),
            Token(TokenType.TEXT, "t", generate_context(0, 10, 0, 11)),
            Token(TokenType.TEXT, " ", generate_context(0, 11, 0, 12)),
            Token(TokenType.LITERAL, "`", generate_context(0, 12, 0, 13)),
            Token(TokenType.LITERAL, "{", generate_context(0, 13, 0, 14)),
            Token(TokenType.TEXT, "c", generate_context(0, 14, 0, 15)),
            Token(TokenType.TEXT, "u", generate_context(0, 15, 0, 16)),
            Token(TokenType.TEXT, "r", generate_context(0, 16, 0, 17)),
            Token(TokenType.TEXT, "l", generate_context(0, 17, 0, 18)),
            Token(TokenType.TEXT, "y", generate_context(0, 18, 0, 19)),
            Token(TokenType.LITERAL, "}", generate_context(0, 19, 0, 20)),
            Token(TokenType.LITERAL, "`", generate_context(0, 20, 0, 21)),
            Token(TokenType.TEXT, " ", generate_context(0, 21, 0, 22)),
            Token(TokenType.TEXT, "_", generate_context(0, 22, 0, 23)),
            Token(TokenType.TEXT, "o", generate_context(0, 23, 0, 24)),
            Token(TokenType.TEXT, "t", generate_context(0, 24, 0, 25)),
            Token(TokenType.TEXT, "h", generate_context(0, 25, 0, 26)),
            Token(TokenType.TEXT, "e", generate_context(0, 26, 0, 27)),
            Token(TokenType.TEXT, "r", generate_context(0, 27, 0, 28)),
            Token(TokenType.TEXT, "_", generate_context(0, 28, 0, 29)),
            Token(TokenType.TEXT, " ", generate_context(0, 29, 0, 30)),
            Token(TokenType.TEXT, "*", generate_context(0, 30, 0, 31)),
            Token(TokenType.TEXT, "t", generate_context(0, 31, 0, 32)),
            Token(TokenType.TEXT, "e", generate_context(0, 32, 0, 33)),
            Token(TokenType.TEXT, "x", generate_context(0, 33, 0, 34)),
            Token(TokenType.TEXT, "t", generate_context(0, 34, 0, 35)),
            Token(TokenType.TEXT, "*", generate_context(0, 35, 0, 36)),
            Token(TokenType.EOF, "", generate_context(0, 36, 0, 36)),
        ],
    )


def test_escape_curly_braces():
    lex = runner(r"Normal text \{curly\} _other_ *text*")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "N", generate_context(0, 0, 0, 1)),
            Token(TokenType.TEXT, "o", generate_context(0, 1, 0, 2)),
            Token(TokenType.TEXT, "r", generate_context(0, 2, 0, 3)),
            Token(TokenType.TEXT, "m", generate_context(0, 3, 0, 4)),
            Token(TokenType.TEXT, "a", generate_context(0, 4, 0, 5)),
            Token(TokenType.TEXT, "l", generate_context(0, 5, 0, 6)),
            Token(TokenType.TEXT, " ", generate_context(0, 6, 0, 7)),
            Token(TokenType.TEXT, "t", generate_context(0, 7, 0, 8)),
            Token(TokenType.TEXT, "e", generate_context(0, 8, 0, 9)),
            Token(TokenType.TEXT, "x", generate_context(0, 9, 0, 10)),
            Token(TokenType.TEXT, "t", generate_context(0, 10, 0, 11)),
            Token(TokenType.TEXT, " ", generate_context(0, 11, 0, 12)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 12, 0, 13)),
            Token(TokenType.LITERAL, "{", generate_context(0, 13, 0, 14)),
            Token(TokenType.TEXT, "c", generate_context(0, 14, 0, 15)),
            Token(TokenType.TEXT, "u", generate_context(0, 15, 0, 16)),
            Token(TokenType.TEXT, "r", generate_context(0, 16, 0, 17)),
            Token(TokenType.TEXT, "l", generate_context(0, 17, 0, 18)),
            Token(TokenType.TEXT, "y", generate_context(0, 18, 0, 19)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 19, 0, 20)),
            Token(TokenType.LITERAL, "}", generate_context(0, 20, 0, 21)),
            Token(TokenType.TEXT, " ", generate_context(0, 21, 0, 22)),
            Token(TokenType.TEXT, "_", generate_context(0, 22, 0, 23)),
            Token(TokenType.TEXT, "o", generate_context(0, 23, 0, 24)),
            Token(TokenType.TEXT, "t", generate_context(0, 24, 0, 25)),
            Token(TokenType.TEXT, "h", generate_context(0, 25, 0, 26)),
            Token(TokenType.TEXT, "e", generate_context(0, 26, 0, 27)),
            Token(TokenType.TEXT, "r", generate_context(0, 27, 0, 28)),
            Token(TokenType.TEXT, "_", generate_context(0, 28, 0, 29)),
            Token(TokenType.TEXT, " ", generate_context(0, 29, 0, 30)),
            Token(TokenType.TEXT, "*", generate_context(0, 30, 0, 31)),
            Token(TokenType.TEXT, "t", generate_context(0, 31, 0, 32)),
            Token(TokenType.TEXT, "e", generate_context(0, 32, 0, 33)),
            Token(TokenType.TEXT, "x", generate_context(0, 33, 0, 34)),
            Token(TokenType.TEXT, "t", generate_context(0, 34, 0, 35)),
            Token(TokenType.TEXT, "*", generate_context(0, 35, 0, 36)),
            Token(TokenType.EOF, "", generate_context(0, 36, 0, 36)),
        ],
    )


def test_preserve_escapes():
    lex = runner(r"Normal \text \_other\_")

    compare_tokens(
        lex.tokens,
        [
            Token(TokenType.TEXT, "N", generate_context(0, 0, 0, 1)),
            Token(TokenType.TEXT, "o", generate_context(0, 1, 0, 2)),
            Token(TokenType.TEXT, "r", generate_context(0, 2, 0, 3)),
            Token(TokenType.TEXT, "m", generate_context(0, 3, 0, 4)),
            Token(TokenType.TEXT, "a", generate_context(0, 4, 0, 5)),
            Token(TokenType.TEXT, "l", generate_context(0, 5, 0, 6)),
            Token(TokenType.TEXT, " ", generate_context(0, 6, 0, 7)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 7, 0, 8)),
            Token(TokenType.TEXT, "t", generate_context(0, 8, 0, 9)),
            Token(TokenType.TEXT, "e", generate_context(0, 9, 0, 10)),
            Token(TokenType.TEXT, "x", generate_context(0, 10, 0, 11)),
            Token(TokenType.TEXT, "t", generate_context(0, 11, 0, 12)),
            Token(TokenType.TEXT, " ", generate_context(0, 12, 0, 13)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 13, 0, 14)),
            Token(TokenType.TEXT, "_", generate_context(0, 14, 0, 15)),
            Token(TokenType.TEXT, "o", generate_context(0, 15, 0, 16)),
            Token(TokenType.TEXT, "t", generate_context(0, 16, 0, 17)),
            Token(TokenType.TEXT, "h", generate_context(0, 17, 0, 18)),
            Token(TokenType.TEXT, "e", generate_context(0, 18, 0, 19)),
            Token(TokenType.TEXT, "r", generate_context(0, 19, 0, 20)),
            Token(TokenType.LITERAL, "\\", generate_context(0, 20, 0, 21)),
            Token(TokenType.TEXT, "_", generate_context(0, 21, 0, 22)),
            Token(TokenType.EOF, "", generate_context(0, 22, 0, 22)),
        ],
    )
