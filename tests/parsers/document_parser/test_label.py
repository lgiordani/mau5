from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_label():
    source = """
    . Some title
    """

    parser = runner(source)

    compare_nodes(
        parser.label_buffer.pop()["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(1, 2, 1, 12)),
            )
        ],
    )


def test_label_with_spaces():
    source = """
    .   Some title
    """

    parser = runner(source)

    compare_nodes(
        parser.label_buffer.pop()["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(1, 4, 1, 14)),
            )
        ],
    )


def test_label_role():
    source = """
    .arole Some label
    """

    parser = runner(source)

    compare_nodes(
        parser.label_buffer.pop()["arole"],
        [
            Node(
                content=TextNodeContent("Some label"),
                info=NodeInfo(context=generate_context(1, 7, 1, 17)),
            )
        ],
    )


def test_label_multiple():
    source = """
    . Some title
    .arole Some label
    """

    parser = runner(source)
    labels = parser.label_buffer.pop()

    assert set(labels.keys()) == set(["title", "arole"])

    compare_nodes(
        labels["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(1, 2, 1, 12)),
            )
        ],
    )
    compare_nodes(
        labels["arole"],
        [
            Node(
                content=TextNodeContent("Some label"),
                info=NodeInfo(context=generate_context(2, 7, 2, 17)),
            )
        ],
    )
