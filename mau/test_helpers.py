import textwrap

from mau.environment.environment import Environment
from mau.text_buffer import Context, TextBuffer
from mau.token import Token

TEST_CONTEXT_SOURCE = "test.py"


def dedent(text):
    return textwrap.dedent(text).strip()


def compare_token(token_left: Token, token_right: Token):
    assert token_left.asdict() == token_right.asdict()


def compare_tokens(tokens_left: list[Token], tokens_right: list[Token]):
    assert [i.asdict() for i in tokens_left] == [i.asdict() for i in tokens_right]


def compare_text_lines(left: str, right: str):
    assert left.split("\n") == right.split("\n")


def generate_context(line: int, column: int, end_line: int, end_column: int):
    return Context(line, column, end_line, end_column, TEST_CONTEXT_SOURCE)


def init_lexer_factory(lexer_class):
    """
    A factory that returns a lexer initialiser.
    The returned function initialises the lexer
    and returns it.
    """

    def _init_lexer(text_buffer: TextBuffer, environment: Environment | None = None):
        return lexer_class(text_buffer, environment)

    return _init_lexer


def lexer_runner_factory(lexer_class, *args, **kwds):
    """
    A factory that returns a lexer runner.
    The returned function initialises and
    runs the lexer on the given source.
    """

    init_lexer = init_lexer_factory(lexer_class)

    def _run(text, environment: Environment | None = None, **kwargs):
        kwds.update(kwargs)

        environment = environment or Environment()

        text_buffer = TextBuffer(
            textwrap.dedent(text),
            source_filename=TEST_CONTEXT_SOURCE,
        )

        lexer = init_lexer(text_buffer, environment, *args, **kwds)
        lexer.process()

        return lexer

    return _run


def init_tokens_manager_factory(lexer_class, tokens_manager_class):
    def _init_tokens_manager(text: str, environment):
        text_buffer = TextBuffer(text, source_filename=TEST_CONTEXT_SOURCE)

        lex = lexer_class(text_buffer, environment)
        lex.process()

        tm = tokens_manager_class(lex.tokens)

        return tm

    return _init_tokens_manager


def init_parser_factory(lexer_class, parser_class):
    """
    A factory that returns a parser initialiser.
    The returned function initialises and runs the lexer,
    initialises the parser and returns it.
    """

    def _init_parser(source: str, environment=None, *args, **kwargs):
        text_buffer = TextBuffer(
            textwrap.dedent(source),
            source_filename=TEST_CONTEXT_SOURCE,
        )

        lex = lexer_class(text_buffer, environment)
        lex.process()

        par = parser_class(lex.tokens, environment, *args, **kwargs)

        return par

    return _init_parser


def parser_runner_factory(lexer_class, parser_class, *args, **kwds):
    """
    A factory that returns a parser runner.
    The returned function runs the parser on the given source.
    """

    init_parser = init_parser_factory(lexer_class, parser_class)

    def _run(source, environment=None, **kwargs):
        kwds.update(kwargs)

        environment = environment or Environment()

        parser = init_parser(source, environment, *args, **kwds)
        parser.parse()
        parser.finalise()

        return parser

    return _run
