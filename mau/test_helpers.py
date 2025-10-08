import textwrap

from mau.text_buffer.context import Context

TEST_CONTEXT_SOURCE = "test.py"


def dedent(text):
    return textwrap.dedent(text).strip()


def compare_text_lines(left: str, right: str):
    assert left.split("\n") == right.split("\n")


def generate_context(
    line: int, column: int, end_line: int = 0, end_column: int = 0
):  # TODO remove the default values
    return Context(line, column, end_line, end_column, TEST_CONTEXT_SOURCE)
