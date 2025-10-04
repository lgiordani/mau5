from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.header import header_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_header_level_1():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_unique_id_function",
        lambda node: "XXXXXY",
    )

    source = "= Title of the section"

    parser: DocumentParser = init_parser(source, environment)
    header_processor(parser)
    parser.toc_manager.process()

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(context=generate_context(0, 0, 0, 22)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of the section"),
                            info=NodeInfo(context=generate_context(0, 2, 0, 22)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_level_3():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_unique_id_function",
        lambda node: "XXXXXY",
    )

    source = "=== Title of a subsection"

    parser: DocumentParser = init_parser(source, environment)
    header_processor(parser)
    parser.toc_manager.process()

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(3, "XXXXXY"),
                info=NodeInfo(context=generate_context(0, 0, 0, 25)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of a subsection"),
                            info=NodeInfo(context=generate_context(0, 4, 0, 25)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_attributes():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_unique_id_function",
        lambda node: "XXXXXY",
    )

    source = "= Title of the section"

    parser: DocumentParser = init_parser(source, environment)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    header_processor(parser)
    parser.toc_manager.process()

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 22),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of the section"),
                            info=NodeInfo(context=generate_context(0, 2, 0, 22)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_attributes_can_overwrite_unique_id():
    source = "= Header"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"unique_id": "someheader"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    header_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "someheader"),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 8),
                    unnamed_args=["arg1"],
                    named_args={},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Header"),
                            info=NodeInfo(context=generate_context(0, 2, 0, 8)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_ignore_title():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_unique_id_function",
        lambda node: "XXXXXY",
    )

    source = """
    . This is a title
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(context=generate_context(2, 0, 2, 22)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of the section"),
                            info=NodeInfo(context=generate_context(2, 2, 2, 22)),
                        )
                    ]
                },
            )
        ],
    )

    assert list(parser.children_buffer.children.keys()) == ["title"]


def test_header_uses_control_positive():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_unique_id_function",
        lambda node: "XXXXXY",
    )
    environment.setvar("answer", "42")

    source = """
    @if answer==42
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(context=generate_context(2, 0, 2, 22)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of the section"),
                            info=NodeInfo(context=generate_context(2, 2, 2, 22)),
                        )
                    ]
                },
            )
        ],
    )

    assert parser.control_buffer.pop() is None


def test_header_uses_control_negative():
    environment = Environment()

    source = """
    @if answer==42
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(parser.nodes, [])

    assert parser.control_buffer.pop() is None
