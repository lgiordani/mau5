from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.inline import StyleNodeData, TextNodeData
from mau.nodes.node import Node, NodeInfo, WrapperNodeData
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_object,
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
    labels = parser.label_buffer.pop()

    compare_asdict_object(
        labels["title"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some title"),
                        info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(1, 0, 1, 12)),
        ),
    )


def test_label_with_spaces():
    source = """
    .   Some title
    """

    parser = runner(source)
    labels = parser.label_buffer.pop()

    compare_asdict_object(
        labels["title"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some title"),
                        info=NodeInfo(context=generate_context(1, 4, 1, 14)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(1, 0, 1, 14)),
        ),
    )


def test_label_role():
    source = """
    .arole Some label
    """

    parser = runner(source)
    labels = parser.label_buffer.pop()

    compare_asdict_object(
        labels["arole"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some label"),
                        info=NodeInfo(context=generate_context(1, 7, 1, 17)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(1, 0, 1, 17)),
        ),
    )


def test_label_multiple():
    source = """
    . Some title
    .arole Some label
    """

    parser = runner(source)
    labels = parser.label_buffer.pop()

    assert set(labels.keys()) == set(["title", "arole"])

    compare_asdict_object(
        labels["title"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some title"),
                        info=NodeInfo(context=generate_context(1, 2, 1, 12)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(1, 0, 1, 12)),
        ),
    )

    compare_asdict_object(
        labels["arole"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some label"),
                        info=NodeInfo(context=generate_context(2, 7, 2, 17)),
                    )
                ]
            ),
            info=NodeInfo(context=generate_context(2, 0, 2, 17)),
        ),
    )


def test_label_can_contain_mau_syntax():
    source = """
    . Some _title_
    """

    parser = runner(source)
    labels = parser.label_buffer.pop()

    compare_asdict_object(
        labels["title"],
        Node(
            data=WrapperNodeData(
                content=[
                    Node(
                        data=TextNodeData("Some "),
                        info=NodeInfo(context=generate_context(1, 2, 1, 7)),
                    ),
                    Node(
                        data=StyleNodeData(
                            "underscore",
                            content=[
                                Node(
                                    data=TextNodeData("title"),
                                    info=NodeInfo(
                                        context=generate_context(1, 8, 1, 13)
                                    ),
                                )
                            ],
                        ),
                        info=NodeInfo(context=generate_context(1, 7, 1, 14)),
                    ),
                ]
            ),
            info=NodeInfo(context=generate_context(1, 0, 1, 14)),
        ),
    )
