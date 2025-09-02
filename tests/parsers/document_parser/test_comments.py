import pytest

from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.base_parser import MauParserException
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_single_line_comments():
    source = "// Just a comment"

    expected_nodes = []

    parser = runner(source)

    assert parser.nodes == expected_nodes


def test_parse_multi_line_comments():
    source = """
    ////
    This is a
    multiline
    comment
    ////
    """

    expected_nodes = []

    parser = runner(source)

    assert parser.nodes == expected_nodes


def test_parse_multi_line_comments_with_mau_syntax():
    source = """
    ////
    .This is a
    [multiline]
    ----
    comment
    ////
    """

    expected_nodes = []

    parser = runner(source)

    assert parser.nodes == expected_nodes


def test_parse_multi_line_comments_left_open():
    source = """
    ////
    .This is a
    [multiline]
    ----
    comment
    """

    with pytest.raises(MauParserException):
        runner(source)
