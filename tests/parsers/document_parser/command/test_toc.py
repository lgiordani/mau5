from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.command import TocItemNodeContent, TocNodeContent
from mau.nodes.headers import HeaderNodeContent
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


def test_command_toc_empty():
    source = """
    ::toc
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 5)),
                children={
                    "nested_entries": [],
                    "plain_entries": [],
                },
            )
        ],
    )


def test_command_toc_supports_inline_arguments():
    source = """
    ::toc:arg1,#tag1,*subtype1,key1=value1
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "nested_entries": [],
                    "plain_entries": [],
                },
            )
        ],
    )


def test_command_toc_supports_boxed_arguments():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    ::toc
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "nested_entries": [],
                    "plain_entries": [],
                },
            )
        ],
    )


def test_command_toc_supports_labels():
    source = """
    . Some label
    ::toc
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=TocNodeContent(),
                info=NodeInfo(context=generate_context(2, 0, 2, 5)),
                children={
                    "nested_entries": [],
                    "plain_entries": [],
                    "title": [
                        Node(
                            content=TextNodeContent("Some label"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                        )
                    ],
                },
            )
        ],
    )


def test_command_toc_supports_control():
    environment = Environment()
    environment["answer"] = "24"

    source = """
    @if answer==42
    [arg1, arg2]
    . Some title
    ::toc
    """

    parser = runner(source, environment)

    compare_nodes(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None


def test_command_toc():
    def _header_internal_id(node: Node[HeaderNodeContent]) -> str:
        # Lowercase the text of the header.
        text_node = node.children["text"][0]
        text = text_node.content.value

        return f"{text}-XXXXXX"

    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = _header_internal_id

    source = """
    = Header 1
    == Header 1.1
    = Header 2

    ::toc
    """

    parser = runner(source, environment)

    node_header_1_1 = Node(
        content=HeaderNodeContent(level=2, internal_id="Header 1.1-XXXXXX"),
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
        content=HeaderNodeContent(level=1, internal_id="Header 1-XXXXXX"),
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
        content=HeaderNodeContent(level=1, internal_id="Header 2-XXXXXX"),
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
        content=TocItemNodeContent(level=2, internal_id="Header 1.1-XXXXXX"),
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
        content=TocItemNodeContent(level=1, internal_id="Header 1-XXXXXX"),
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
        content=TocItemNodeContent(level=1, internal_id="Header 2-XXXXXX"),
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
