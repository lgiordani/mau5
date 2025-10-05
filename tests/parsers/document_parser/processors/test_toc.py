import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.toc import TocItemNodeContent, TocNodeContent
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.command import command_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_command_toc():
    source = "::toc"

    parser: DocumentParser = init_parser(source)
    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 5)),
            )
        ],
    )


def test_command_toc_inline_arguments():
    source = "::toc:arg1,#tag1,*subtype1,key1=value1"

    parser: DocumentParser = init_parser(source)
    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_boxed_arguments():
    source = "::toc"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    command_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_boxed_and_inline_arguments_are_forbidden():
    source = "::toc:arg2"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    with pytest.raises(MauParserException) as exc:
        command_processor(parser)

    assert (
        exc.value.message
        == "Syntax error. You cannot specify both boxed and inline arguments."
    )
    assert exc.value.context == generate_context(0, 0, 0, 5)


def test_toc():
    def _header_unique_id(node: Node[HeaderNodeContent]) -> str:
        # Lowercase the text of the header.
        text_node = node.children["text"][0]
        text = text_node.content.value

        return f"{text}-XXXXXX"

    environment = Environment()
    environment.setvar("mau.parser.header_unique_id_function", _header_unique_id)

    source = """
    = Header 1
    == Header 1.1
    = Header 2

    ::toc
    """

    parser = runner(source, environment)

    node_header_1_1 = Node(
        content=HeaderNodeContent(level=2, unique_id="Header 1.1-XXXXXX"),
        info=NodeInfo(context=generate_context(2, 0, 2, 13)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 1.1"),
                    info=NodeInfo(context=generate_context(2, 3, 2, 13)),
                )
            ],
        },
    )

    node_header_1 = Node(
        content=HeaderNodeContent(level=1, unique_id="Header 1-XXXXXX"),
        info=NodeInfo(context=generate_context(1, 0, 1, 10)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 1"),
                    info=NodeInfo(context=generate_context(1, 2, 1, 10)),
                )
            ],
        },
    )

    node_header_2 = Node(
        content=HeaderNodeContent(level=1, unique_id="Header 2-XXXXXX"),
        info=NodeInfo(context=generate_context(3, 0, 3, 10)),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header 2"),
                    info=NodeInfo(context=generate_context(3, 2, 3, 10)),
                )
            ],
        },
    )

    node_toc_item_1_1 = Node(
        content=TocItemNodeContent(level=2, unique_id="Header 1.1-XXXXXX"),
        info=NodeInfo(context=generate_context(2, 0, 2, 13)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Header 1.1"),
                    info=NodeInfo(context=generate_context(2, 3, 2, 13)),
                )
            ],
        },
    )

    node_toc_item_1 = Node(
        content=TocItemNodeContent(level=1, unique_id="Header 1-XXXXXX"),
        info=NodeInfo(context=generate_context(1, 0, 1, 10)),
        children={
            "entries": [node_toc_item_1_1],
            "text": [
                Node(
                    content=TextNodeContent("Header 1"),
                    info=NodeInfo(context=generate_context(1, 2, 1, 10)),
                )
            ],
        },
    )

    node_toc_item_2 = Node(
        content=TocItemNodeContent(level=1, unique_id="Header 2-XXXXXX"),
        info=NodeInfo(context=generate_context(3, 0, 3, 10)),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Header 2"),
                    info=NodeInfo(context=generate_context(3, 2, 3, 10)),
                )
            ],
        },
    )

    node_toc = Node(
        content=TocNodeContent(),
        info=NodeInfo(context=generate_context(5, 0, 5, 5)),
        children={
            "nested_entries": [
                node_toc_item_1,
                node_toc_item_2,
            ],
            "plain_entries": [
                node_header_1,
                node_header_1_1,
                node_header_2,
            ],
        },
    )

    compare_nodes(
        parser.nodes,
        [
            node_header_1,
            node_header_1_1,
            node_header_2,
            node_toc,
        ],
    )
