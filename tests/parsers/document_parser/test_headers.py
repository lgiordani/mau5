from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
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


def test_header_level_1():
    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = lambda node: "XXXXXY"

    source = """
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(context=generate_context(1, 0, 1, 22)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of the section"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 22)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_level_3():
    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = lambda node: "XXXXXY"

    source = """
    === Title of a subsection
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(3, "XXXXXY"),
                info=NodeInfo(context=generate_context(1, 0, 1, 25)),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Title of a subsection"),
                            info=NodeInfo(context=generate_context(1, 4, 1, 25)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_attributes():
    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = lambda node: "XXXXXY"

    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "XXXXXY"),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 22),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
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


def test_header_attributes_can_overwrite_internal_id():
    source = """
    [arg1, #tag1, *subtype1, internal_id=someheader]
    = Header
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=HeaderNodeContent(1, "someheader"),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 8),
                    unnamed_args=["arg1"],
                    named_args={},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "text": [
                        Node(
                            content=TextNodeContent("Header"),
                            info=NodeInfo(context=generate_context(2, 2, 2, 8)),
                        )
                    ]
                },
            )
        ],
    )


def test_header_ignores_label():
    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = lambda node: "XXXXXY"

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

    assert list(parser.label_buffer.labels.keys()) == ["title"]


def test_header_uses_control_positive():
    environment = Environment()
    environment["mau.parser.header_internal_id_function"] = lambda node: "XXXXXY"
    environment["answer"] = "42"

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
    environment["answer"] = "24"

    source = """
    @if answer==42
    = Title of the section
    """

    parser = runner(source, environment)

    compare_nodes(parser.nodes, [])
