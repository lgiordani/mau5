from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.inline import StyleNodeContent, TextNodeContent
from mau.nodes.macros import MacroLinkNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent, ParagraphLineNodeContent
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_paragraph():
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
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 35)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 20)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is a paragraph."),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 20)
                                        ),
                                    ),
                                ]
                            },
                        ),
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 35)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is part of the same paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 35)
                                        ),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is another paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 26)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_paragraph_with_style():
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
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 22)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is a "),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 10)
                                        ),
                                    ),
                                    Node(
                                        content=StyleNodeContent("star"),
                                        info=NodeInfo(
                                            context=generate_context(1, 10, 1, 21)
                                        ),
                                        children={
                                            "content": [
                                                Node(
                                                    content=TextNodeContent(
                                                        "paragraph"
                                                    ),
                                                    info=NodeInfo(
                                                        context=generate_context(
                                                            1, 11, 1, 20
                                                        )
                                                    ),
                                                )
                                            ]
                                        },
                                    ),
                                    Node(
                                        content=TextNodeContent("."),
                                        info=NodeInfo(
                                            context=generate_context(1, 21, 1, 22)
                                        ),
                                    ),
                                ]
                            },
                        ),
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 35)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is part of the same paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 35)
                                        ),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 35)),
            ),
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is another paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 26)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_paragraph_with_style_on_multiple_lines():
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
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 2, 48)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 20)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is a *paragraph"),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 20)
                                        ),
                                    ),
                                ]
                            },
                        ),
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 48)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "with style*. This is part of the same paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 48)
                                        ),
                                    ),
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is another paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 26)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_paragraph_starting_with_a_macro():
    source = """
    [link](http://some.where,This) is the link I want
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 49)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 49)),
                            children={
                                "content": [
                                    Node(
                                        content=MacroLinkNodeContent(
                                            "http://some.where"
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 30)
                                        ),
                                        children={
                                            "text": [
                                                Node(
                                                    content=TextNodeContent("This"),
                                                    info=NodeInfo(
                                                        context=generate_context(
                                                            1, 25, 1, 29
                                                        )
                                                    ),
                                                ),
                                            ]
                                        },
                                    ),
                                    Node(
                                        content=TextNodeContent(" is the link I want"),
                                        info=NodeInfo(
                                            context=generate_context(1, 30, 1, 49)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_attributes_paragraph():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    This is text
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 12),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 12)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is text"),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 12)
                                        ),
                                    ),
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )


def test_paragraph_label():
    source = """
    . A title
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
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 12)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is text"),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 12)
                                        ),
                                    ),
                                ]
                            },
                        )
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
                    context=generate_context(2, 0, 2, 12),
                ),
            ),
        ],
    )

    paragraph_node = parser.nodes[0]
    text_node = paragraph_node.children["title"][0]

    assert text_node.parent == paragraph_node


def test_paragraph_with_variable():
    source = """
    :variable:cat
    This is a paragraph with a {variable}.
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(2, 0, 2, 38)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 38)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is a paragraph with a cat."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 31)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_paragraph_with_namespaced_variable():
    environment = Environment.from_dict({"content": {"animal": "cat"}})
    source = """
    This is a paragraph with a {content.animal}.
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 44)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 44)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is a paragraph with a cat."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 31)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_paragraph_with_escaped_mau_syntax():
    source = r"""
    \:answer:42
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 11)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 11)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(":answer:42"),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 11)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_paragraph_with_escaped_variable():
    environment = Environment.from_dict({"variable": "cat"})
    source = r"""
    This is a paragraph with a \{variable\}.
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 40)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 40)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is a paragraph with a {variable}."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 38)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_paragraph_with_variable_containing_syntax():
    environment = Environment.from_dict({"important": "*IMPORTANT*"})
    source = """
    This is {important}
    """

    parser = runner(source, environment)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(1, 0, 1, 19)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(1, 0, 1, 19)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is "),
                                        info=NodeInfo(
                                            context=generate_context(1, 0, 1, 8)
                                        ),
                                    ),
                                    Node(
                                        content=StyleNodeContent("star"),
                                        info=NodeInfo(
                                            context=generate_context(1, 8, 1, 19)
                                        ),
                                        children={
                                            "content": [
                                                Node(
                                                    content=TextNodeContent(
                                                        "IMPORTANT"
                                                    ),
                                                    info=NodeInfo(
                                                        context=generate_context(
                                                            1, 9, 1, 18
                                                        )
                                                    ),
                                                ),
                                            ]
                                        },
                                    ),
                                ]
                            },
                        )
                    ]
                },
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
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 10)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 10)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("The answer is 42"),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 16)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            )
        ],
    )


def test_paragraph_uses_control_positive():
    environment = Environment.from_dict({"answer": "42"})

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
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(2, 0, 2, 20)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(2, 0, 2, 20)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent("This is a paragraph."),
                                        info=NodeInfo(
                                            context=generate_context(2, 0, 2, 20)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            ),
            Node(
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is another paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 26)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )

    assert parser.control_buffer.pop() is None


def test_paragraph_uses_control_negative():
    environment = Environment.from_dict({"answer": "24"})

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
                content=ParagraphNodeContent(),
                info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                children={
                    "content": [
                        Node(
                            content=ParagraphLineNodeContent(),
                            info=NodeInfo(context=generate_context(4, 0, 4, 26)),
                            children={
                                "content": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is another paragraph."
                                        ),
                                        info=NodeInfo(
                                            context=generate_context(4, 0, 4, 26)
                                        ),
                                    )
                                ]
                            },
                        )
                    ]
                },
            ),
        ],
    )

    assert parser.control_buffer.pop() is None


def test_paragraph_control():
    source = """
    :answer:44

    @if answer==42
    [arg1, arg2]
    . Some title
    This paragraph won't be rendered
    """

    parser = runner(source)

    compare_nodes(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None
