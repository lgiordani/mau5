from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.commands import TocItemNode, TocNode
from mau.nodes.headers import HeaderNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_list,
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

    compare_asdict_list(
        parser.nodes,
        [
            TocNode(
                nested_entries=[],
                plain_entries=[],
                info=NodeInfo(context=generate_context(1, 0, 1, 5)),
            )
        ],
    )


def test_command_toc_supports_inline_arguments():
    source = """
    ::toc:arg1,#tag1,*subtype1,key1=value1
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            TocNode(
                nested_entries=[],
                plain_entries=[],
                info=NodeInfo(
                    context=generate_context(1, 0, 1, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_supports_boxed_arguments():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    ::toc
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            TocNode(
                nested_entries=[],
                plain_entries=[],
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 5),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            )
        ],
    )


def test_command_toc_supports_labels():
    source = """
    . Some label
    ::toc
    """

    parser = runner(source)

    compare_asdict_list(
        parser.nodes,
        [
            TocNode(
                nested_entries=[],
                plain_entries=[],
                labels={
                    "title": [
                        TextNode(
                            "Some label",
                            info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                        )
                    ]
                },
                info=NodeInfo(context=generate_context(2, 0, 2, 5)),
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

    compare_asdict_list(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None


def test_command_toc_with_entries():
    def _header_internal_id(node: HeaderNode) -> str:
        # Lowercase the text of the header.
        text = node.source_text

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

    header_1_1 = HeaderNode(
        level=2,
        internal_id="Header 1.1-XXXXXX",
        source_text="Header 1.1",
        content=[
            TextNode(
                "Header 1.1",
                info=NodeInfo(context=generate_context(2, 3, 2, 13)),
            )
        ],
        info=NodeInfo(context=generate_context(2, 0, 2, 13)),
    )

    header_1 = HeaderNode(
        level=1,
        internal_id="Header 1-XXXXXX",
        source_text="Header 1",
        content=[
            TextNode(
                "Header 1",
                info=NodeInfo(context=generate_context(1, 2, 1, 10)),
            )
        ],
        info=NodeInfo(context=generate_context(1, 0, 1, 10)),
    )

    header_2 = HeaderNode(
        level=1,
        internal_id="Header 2-XXXXXX",
        source_text="Header 2",
        content=[
            TextNode(
                "Header 2",
                info=NodeInfo(context=generate_context(3, 2, 3, 10)),
            )
        ],
        info=NodeInfo(context=generate_context(3, 0, 3, 10)),
    )

    toc_item_1_1 = TocItemNode(header=header_1_1)

    toc_item_1 = TocItemNode(header=header_1, entries=[toc_item_1_1])

    toc_item_2 = TocItemNode(header=header_2)

    node_toc = TocNode(
        nested_entries=[
            toc_item_1,
            toc_item_2,
        ],
        plain_entries=[
            header_1,
            header_1_1,
            header_2,
        ],
        info=NodeInfo(context=generate_context(5, 0, 5, 5)),
    )

    compare_asdict_list(
        parser.nodes,
        [
            header_1,
            header_1_1,
            header_2,
            node_toc,
        ],
    )
