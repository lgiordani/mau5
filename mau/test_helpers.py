import textwrap

from mau.environment.environment import Environment
from mau.text_buffer.context import Context
from mau.text_buffer.text_buffer import TextBuffer

TEST_CONTEXT_SOURCE = "test.py"


def dedent(text):
    return textwrap.dedent(text).strip()


def compare_tokens(tokens_left, tokens_right):
    assert [i.asdict() for i in tokens_left] == [i.asdict() for i in tokens_right]


def compare_nodes(nodes_left, nodes_right):
    assert [i.asdict() for i in nodes_left] == [i.asdict() for i in nodes_right]


def generate_context(line: int, column: int):
    return Context(line, column, TEST_CONTEXT_SOURCE)


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
            textwrap.dedent(text), Context(source=TEST_CONTEXT_SOURCE)
        )

        lexer = init_lexer(text_buffer, environment, *args, **kwds)
        lexer.process()

        return lexer

    return _run


def init_parser_factory(lexer_class, parser_class):
    """
    A factory that returns a parser initialiser.
    The returned function initialises and runs the lexer,
    initialises the parser and returns it.
    """

    def _init_parser(text: str, environment, *args, **kwargs):
        text_buffer = TextBuffer(text, Context(source=TEST_CONTEXT_SOURCE))

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

        parser = init_parser(textwrap.dedent(source), environment, *args, **kwds)
        parser.parse()
        parser.finalise()

        return parser

    return _run
