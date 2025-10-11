import textwrap

from mau.text_buffer.context import Context

TEST_CONTEXT_SOURCE = "test.py"


def dedent(text):
    return textwrap.dedent(text).strip()


def compare_text_lines(left: str, right: str):
    assert left.split("\n") == right.split("\n")


def generate_context(line: int, column: int, end_line: int, end_column: int):
    return Context(line, column, end_line, end_column, TEST_CONTEXT_SOURCE)


# def init_lexer_factory(lexer_class):
#     """
#     A factory that returns a lexer initialiser.
#     The returned function initialises the lexer
#     and returns it.
#     """

#     def _init_lexer(text_buffer: TextBuffer, environment: Environment | None = None):
#         return lexer_class(text_buffer, environment)

#     return _init_lexer


# def lexer_runner_factory(lexer_class, *args, **kwds):
#     """
#     A factory that returns a lexer runner.
#     The returned function initialises and
#     runs the lexer on the given source.
#     """

#     init_lexer = init_lexer_factory(lexer_class)

#     def _run(text, environment: Environment | None = None, **kwargs):
#         kwds.update(kwargs)

#         environment = environment or Environment()

#         text_buffer = TextBuffer(
#             textwrap.dedent(text), Context(source=TEST_CONTEXT_SOURCE)
#         )

#         lexer = init_lexer(text_buffer, environment, *args, **kwds)
#         lexer.process()

#         return lexer

#     return _run
