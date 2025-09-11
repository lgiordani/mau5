from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.lists import ListItemNodeContent, ListNodeContent
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


def test_parse_list_with_one_item():
    source = """
    * This is a list with one element
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is a list with one element"
                                        ),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_list_with_multiple_items():
    source = """
    * Item 1
    * Item 2
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(2, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_list_with_multiple_levels():
    source = """
    * Item 1
    ** Item 1.1
    * Item 2
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=ListNodeContent(ordered=False, main_node=False),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "nodes": [
                                    Node(
                                        content=ListItemNodeContent("2"),
                                        info=NodeInfo(context=generate_context(2, 0)),
                                        children={
                                            "text": [
                                                Node(
                                                    content=TextNodeContent("Item 1.1"),
                                                    info=NodeInfo(
                                                        context=generate_context(2, 3)
                                                    ),
                                                )
                                            ]
                                        },
                                    )
                                ],
                            },
                        ),
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(3, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_numbered_list():
    source = """
    # Item 1
    ## Item 1.1
    # Item 2
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=True, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=ListNodeContent(ordered=True, main_node=False),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "nodes": [
                                    Node(
                                        content=ListItemNodeContent("2"),
                                        info=NodeInfo(context=generate_context(2, 0)),
                                        children={
                                            "text": [
                                                Node(
                                                    content=TextNodeContent("Item 1.1"),
                                                    info=NodeInfo(
                                                        context=generate_context(2, 3)
                                                    ),
                                                )
                                            ]
                                        },
                                    )
                                ],
                            },
                        ),
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(3, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_mixed_list():
    source = """
    * Item 1
    ## Item 1.1
    * Item 2
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=ListNodeContent(ordered=True, main_node=False),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "nodes": [
                                    Node(
                                        content=ListItemNodeContent("2"),
                                        info=NodeInfo(context=generate_context(2, 0)),
                                        children={
                                            "text": [
                                                Node(
                                                    content=TextNodeContent("Item 1.1"),
                                                    info=NodeInfo(
                                                        context=generate_context(2, 3)
                                                    ),
                                                )
                                            ]
                                        },
                                    )
                                ],
                            },
                        ),
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(3, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_mixed_list_cannot_change_type():
    source1 = """
    * Item 1
    ## Item 1.1
    # Item 2
    """

    source2 = """
    * Item 1
    ## Item 1.1
    * Item 2
    """

    assert runner(source1).nodes == runner(source2).nodes


def test_parse_numbered_list_continue():
    source = """
    # Item 1
    # Item 2

    [start=auto]
    # Item 3
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=True, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(2, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ListNodeContent(ordered=True, main_node=True, start=3),
                info=NodeInfo(context=generate_context(5, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(5, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 3"),
                                        info=NodeInfo(context=generate_context(5, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_numbered_list_continue_after_forced():
    source = """
    # Item 1

    [start=20]
    # Item 20

    [start=auto]
    # Item 21
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=True, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ListNodeContent(ordered=True, main_node=True, start=20),
                info=NodeInfo(context=generate_context(4, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(4, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 20"),
                                        info=NodeInfo(context=generate_context(4, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ListNodeContent(ordered=True, main_node=True, start=21),
                info=NodeInfo(context=generate_context(7, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(7, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 21"),
                                        info=NodeInfo(context=generate_context(7, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_numbered_list_do_not_continue_by_default():
    source = """
    # Item 1

    # Item 2
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=True, main_node=True),
                info=NodeInfo(context=generate_context(1, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(1, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 1"),
                                        info=NodeInfo(context=generate_context(1, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
            Node(
                content=ListNodeContent(ordered=True, main_node=True),
                info=NodeInfo(context=generate_context(3, 0)),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(3, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent("Item 2"),
                                        info=NodeInfo(context=generate_context(3, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )


def test_parse_list_arguments():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    * This is a list with one element
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=ListNodeContent(ordered=False, main_node=True),
                info=NodeInfo(
                    context=generate_context(2, 0),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
                children={
                    "nodes": [
                        Node(
                            content=ListItemNodeContent("1"),
                            info=NodeInfo(context=generate_context(2, 0)),
                            children={
                                "text": [
                                    Node(
                                        content=TextNodeContent(
                                            "This is a list with one element"
                                        ),
                                        info=NodeInfo(context=generate_context(2, 2)),
                                    )
                                ]
                            },
                        ),
                    ]
                },
            ),
        ],
    )
