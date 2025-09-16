import textwrap

import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.node import Node, NodeContent
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.comments import (
    multi_line_comment_processor,
    single_line_comment_processor,
)
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_single_line_comments():
    source = "// Just a comment"

    expected_nodes: list[Node[NodeContent]] = []

    parser: DocumentParser = init_parser(source)
    single_line_comment_processor(parser)

    compare_nodes(parser.nodes, expected_nodes)


def test_parse_multi_line_comments():
    source = textwrap.dedent("""
    ////
    This is a
    multiline
    comment
    ////
    """).removeprefix("\n")

    expected_nodes: list[Node[NodeContent]] = []

    parser: DocumentParser = init_parser(source)
    multi_line_comment_processor(parser)

    compare_nodes(parser.nodes, expected_nodes)


def test_parse_multi_line_comments_with_mau_syntax():
    source = textwrap.dedent("""
    ////
    .This is a
    [multiline]
    ----
    comment
    ////
    """).removeprefix("\n")

    expected_nodes: list[Node[NodeContent]] = []

    parser: DocumentParser = init_parser(source)
    multi_line_comment_processor(parser)

    compare_nodes(parser.nodes, expected_nodes)


def test_parse_multi_line_comments_left_open():
    source = textwrap.dedent("""
    ////
    .This is a
    [multiline]
    ----
    comment
    """).removeprefix("\n")

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(0, 0)
