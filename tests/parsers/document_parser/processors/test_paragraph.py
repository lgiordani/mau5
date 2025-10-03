from mau.text_buffer.context import Context
from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 56)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 1, 35)),
            )
        ],
    )


def test_paragraph_full_parse():
    source = """
    This is a paragraph.
    This is part of the same paragraph.

    This is another paragraph.
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
                            info=NodeInfo(context=generate_context(1, 0, 1, 56)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 35)),
            ),
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is another paragraph."),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
            ),
        ],
    )


def test_paragraph_with_style_full_parse():
    source = """
    This is a *paragraph*.
    This is part of the same paragraph.

    This is another paragraph.
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a "),
                            info=NodeInfo(context=generate_context(1, 0, 1, 10)),
                        ),
                        Node(
                            content=StyleNodeContent("star"),
                            info=NodeInfo(context=generate_context(1, 10, 1, 21)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("paragraph"),
                                        info=NodeInfo(
                                            context=generate_context(1, 11, 1, 20)
                                        ),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=TextNodeContent(
                                ". This is part of the same paragraph."
                            ),
                            info=NodeInfo(context=generate_context(1, 21, 2, 35)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 35)),
            ),
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is another paragraph."),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
            ),
        ],
    )


def test_paragraph_with_style_on_multiple_lines_full_parse():
    source = """
    This is a *paragraph
    with style*. This is part of the same paragraph.

    This is another paragraph.
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a "),
                            info=NodeInfo(context=generate_context(1, 0, 1, 10)),
                        ),
                        Node(
                            content=StyleNodeContent("star"),
                            info=NodeInfo(context=generate_context(1, 10, 2, 11)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("paragraph with style"),
                                        info=NodeInfo(
                                            context=generate_context(1, 11, 2, 10)
                                        ),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=TextNodeContent(
                                ". This is part of the same paragraph."
                            ),
                            info=NodeInfo(context=generate_context(2, 11, 2, 52)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 35)),
            ),
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is another paragraph."),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
            ),
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 30)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("This"),
                                        info=NodeInfo(
                                            context=generate_context(0, 25, 0, 29)
                                        ),
                                    ),
                                ]
                            },
                        ),
                        Node(
                            content=TextNodeContent(" is the link I want"),
                            info=NodeInfo(context=generate_context(0, 30, 0, 49)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 49)),
            ),
        ],
    )


def test_attributes_paragraph():
    source = "This is text"

    parser: DocumentParser = init_parser(source)
    parser.arguments_buffer.push(
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 12)),
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 12),
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
    parser.children_buffer.push(
        "title", "A title", generate_context(1, 2), Environment()
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 12)),
                        ),
                    ],
                    "title": [
                        Node(
                            content=TextNodeContent("A title"),
                            info=NodeInfo(context=generate_context(1, 2, 1, 9)),
                        )
                    ],
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(0, 0, 0, 12),
                ),
            ),
        ],
    )

    paragraph_node = parser.nodes[0]
    text_node = paragraph_node.children["title"][0]

    assert text_node.parent == paragraph_node


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
                            info=NodeInfo(context=generate_context(0, 0, 0, 31)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 31)),
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 31)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 31)),
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 11)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 11)),
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 38)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 38)),
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
                            info=NodeInfo(context=generate_context(0, 0, 0, 8)),
                        ),
                        Node(
                            content=StyleNodeContent("star"),
                            info=NodeInfo(context=generate_context(0, 8, 0, 19)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("IMPORTANT"),
                                        info=NodeInfo(
                                            context=generate_context(0, 9, 0, 18)
                                        ),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(0, 0, 0, 19)),
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
                            info=NodeInfo(context=generate_context(4, 0, 4, 16)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 16)),
            )
        ],
    )


def test_paragraph_uses_control_positive():
    environment = Environment()
    environment.setvar("answer", "42")

    source = """
    @if answer==42
    This is a paragraph.

    This is another paragraph.
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is a paragraph."),
                            info=NodeInfo(context=generate_context(2, 0, 2, 20)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(2, 0, 2, 20)),
            ),
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is another paragraph."),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
            ),
        ],
    )

    assert parser.control_buffer.pop() is None


def test_paragraph_uses_control_negative():
    environment = Environment()

    source = """
    @if answer==42
    This is a paragraph.

    This is another paragraph.
    """

    parser: DocumentParser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                children={
                    "content": [
                        Node(
                            content=TextNodeContent("This is another paragraph."),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                        )
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
            ),
        ],
    )

    assert parser.control_buffer.pop() is None
