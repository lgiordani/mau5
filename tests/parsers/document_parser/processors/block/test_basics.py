
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.block import EngineType
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_block_with_empty_body():
    source = """
    ----
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(1, 0)),
                children={"content": []},
            )
        ],
    )


def test_block_content():
    source = """
    ----
    This is a paragraph.
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "content": [
                        Node(
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is a paragraph."),
                                        info=NodeInfo(context=generate_context(2, 0)),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_block_content_variables():
    source = """
    ----
    :answer:42
    The answer is {answer}.
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "content": [
                        Node(
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("The answer is 42."),
                                        info=NodeInfo(context=generate_context(3, 0)),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_block_content_external_variables():
    source = """
    :answer:42
    ----
    The answer is {answer}.
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(2, 0)),
                children={
                    "content": [
                        Node(
                            content=ParagraphNodeContent(),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("The answer is 42."),
                                        info=NodeInfo(context=generate_context(3, 0)),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_block_inside_block():
    source = """
    ----
    ++++
    ++++
    ----
    """

    parser: DocumentParser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine=EngineType.DEFAULT.value,
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "content": [
                        Node(
                            content=BlockNodeContent(
                                classes=[],
                                engine=EngineType.DEFAULT.value,
                                preprocessor=None,
                            ),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={"content": []},
                        )
                    ],
                },
            )
        ],
    )
