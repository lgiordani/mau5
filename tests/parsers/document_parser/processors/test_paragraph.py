from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import SentenceNodeContent, StyleNodeContent, TextNodeContent
from mau.nodes.macros import MacroLinkNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.arguments_parser.parser import Arguments
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.paragraph import paragraph_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_paragraph():
    source = "This is a paragraph.\nThis is part of the same paragraph."

    parser: DocumentParser = init_parser(source)
    paragraph_processor(parser)

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
                            info=NodeInfo(context=generate_context(0, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_starting_with_a_macro():
    source = "[link](http://some.where,This) is the link I want"

    parser: DocumentParser = init_parser(source)
    paragraph_processor(parser)

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
    source = "This is text"

    parser: DocumentParser = init_parser(source)
    parser.arguments_manager.push(
        Arguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        )
    )

    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is text"),
                            info=NodeInfo(context=generate_context(0, 0)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_paragraph_title():
    source = "This is text"

    parser: DocumentParser = init_parser(source)
    parser.title_buffer.push("A title", generate_context(1, 2), Environment())

    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is text"),
                            info=NodeInfo(context=generate_context(0, 0)),
                        ),
                    ],
                    "title": [
                        Node(
                            content=SentenceNodeContent(),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("A title"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                            info=NodeInfo(context=generate_context(1, 2)),
                        )
                    ],
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0),
                ),
            ),
        ],
    )

    paragraph_node = parser.nodes[0]
    text_node = paragraph_node.children["title"][0]

    assert text_node.parent == paragraph_node


def test_paragraphs_full_parse():
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


def test_paragraph_with_variable():
    source = "This is a paragraph with a {variable}."

    parser: DocumentParser = init_parser(
        source, environment=Environment.from_dict({"variable": "cat"})
    )
    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a paragraph with a cat."),
                            info=NodeInfo(context=generate_context(0, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_with_namespaced_variable():
    source = "This is a paragraph with a {content.animal}."

    parser: DocumentParser = init_parser(
        source, environment=Environment.from_dict({"content": {"animal": "cat"}})
    )
    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a paragraph with a cat."),
                            info=NodeInfo(context=generate_context(0, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_with_escaped_syntax():
    source = r"\:answer:42"

    parser: DocumentParser = init_parser(source)
    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent(":answer:42"),
                            info=NodeInfo(context=generate_context(0, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_with_escaped_variable():
    source = r"This is a paragraph with a \{variable\}."

    parser: DocumentParser = init_parser(
        source, environment=Environment.from_dict({"variable": "cat"})
    )
    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent(
                                "This is a paragraph with a {variable}."
                            ),
                            info=NodeInfo(context=generate_context(0, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_with_variable_containing_syntax():
    source = "This is {important}"

    parser: DocumentParser = init_parser(
        source, environment=Environment.from_dict({"important": "*IMPORTANT*"})
    )
    paragraph_processor(parser)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is "),
                            info=NodeInfo(context=generate_context(0, 0)),
                        ),
                        Node(
                            content=StyleNodeContent("star"),
                            info=NodeInfo(context=generate_context(0, 8)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("IMPORTANT"),
                                        info=NodeInfo(context=generate_context(0, 9)),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_paragraph_with_nested_variables():
    source = """
    :answer:42
    :sentence:The answer is {answer}

    {sentence}
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("The answer is 42"),
                            info=NodeInfo(context=generate_context(4, 0)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0)),
            )
        ],
    )
