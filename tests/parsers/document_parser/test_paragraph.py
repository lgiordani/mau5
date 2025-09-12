from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.macros import MacroLinkNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_paragraphs():
    source = """
    This is a paragraph.
    This is part of the same paragraph.

    This is a new paragraph.
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent(
                                "This is a paragraph. This is part of the same paragraph."
                            ),
                            info=NodeInfo(context=generate_context(1, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0)),
            ),
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a new paragraph."),
                            info=NodeInfo(context=generate_context(4, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0)),
            ),
        ],
    )


def test_parse_paragraph_starting_with_a_macro():
    source = "[link](http://some.where,This) is the link I want"

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=MacroLinkNodeContent("http://some.where"),
                            info=NodeInfo(context=generate_context(0, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("This"),
                                        info=NodeInfo(context=generate_context(0, 25)),
                                    ),
                                ]
                            },
                        ),
                        Node(
                            content=TextNodeContent(" is the link I want"),
                            info=NodeInfo(context=generate_context(0, 30)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            ),
        ],
    )


def test_attributes_paragraph():
    source = """
    [*type, arg1,key1=value1]
    This is text
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is text"),
                            info=NodeInfo(context=generate_context(2, 0)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(2, 0),
                    subtype="type",
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                ),
            ),
        ],
    )


def test_paragraph_title():
    source = """
    .Title
    This is text
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is text"),
                            info=NodeInfo(context=generate_context(2, 0)),
                        ),
                    ],
                    "title": [
                        Node(
                            content=SentenceNodeContent(),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("Title"),
                                        info=NodeInfo(context=generate_context(1, 0)),
                                    )
                                ]
                            },
                            info=NodeInfo(context=generate_context(1, 0)),
                        )
                    ],
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(2, 0),
                ),
            ),
        ],
    )

    paragraph_node = parser.nodes[0]
    text_node = paragraph_node.children["title"][0]

    assert text_node.parent == paragraph_node
