import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.node import Node, NodeContent
from mau.parsers.base_parser.managers.tokens_manager import TokensManager
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    init_tokens_manager_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)
init_tm = init_tokens_manager_factory(DocumentLexer, TokensManager)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_single_line_comments():
    source = "// Just a comment"

    expected_nodes: list[Node[NodeContent]] = []

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

    expected_nodes: list[Node[NodeContent]] = []

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

    expected_nodes: list[Node[NodeContent]] = []

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

    with pytest.raises(MauParserException) as exc:
        runner(source)

    assert exc.value.context == generate_context(1, 0)
