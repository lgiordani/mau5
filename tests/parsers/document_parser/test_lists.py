from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.inline import TextNode
from mau.nodes.list import ListItemNode, ListNode
from mau.nodes.node import NodeInfo
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes_sequence,
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

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "This is a list with one element",
                                info=NodeInfo(context=generate_context(1, 2, 1, 33)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 33)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 33)),
            ),
        ],
    )


def test_parse_list_with_multiple_items():
    source = """
    * Item 1
    * Item 2
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(2, 2, 2, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 2, 8)),
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

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                    ListNode(
                        ordered=False,
                        main_node=False,
                        content=[
                            ListItemNode(
                                2,
                                content=[
                                    TextNode(
                                        "Item 1.1",
                                        info=NodeInfo(
                                            context=generate_context(2, 3, 2, 11)
                                        ),
                                    )
                                ],
                                info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                    ),
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(3, 2, 3, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 3, 8)),
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

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=True,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                    ListNode(
                        ordered=True,
                        main_node=False,
                        content=[
                            ListItemNode(
                                2,
                                content=[
                                    TextNode(
                                        "Item 1.1",
                                        info=NodeInfo(
                                            context=generate_context(2, 3, 2, 11)
                                        ),
                                    )
                                ],
                                info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                    ),
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(3, 2, 3, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 3, 8)),
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

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                    ListNode(
                        ordered=True,
                        main_node=False,
                        content=[
                            ListItemNode(
                                2,
                                content=[
                                    TextNode(
                                        "Item 1.1",
                                        info=NodeInfo(
                                            context=generate_context(2, 3, 2, 11)
                                        ),
                                    )
                                ],
                                info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 11)),
                    ),
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(3, 2, 3, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 3, 8)),
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

    compare_nodes_sequence(runner(source1).nodes, runner(source2).nodes)


def test_parse_numbered_list_continue():
    source = """
    # Item 1
    # Item 2

    [start=auto]
    # Item 3
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=True,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(2, 2, 2, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 2, 8)),
            ),
            ListNode(
                ordered=True,
                main_node=True,
                start=3,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 3",
                                info=NodeInfo(context=generate_context(5, 2, 5, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(5, 0, 5, 8)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(5, 0, 5, 8), named_args={"start": "auto"}
                ),
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

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=True,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 8)),
            ),
            ListNode(
                ordered=True,
                main_node=True,
                start=20,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 20",
                                info=NodeInfo(context=generate_context(4, 2, 4, 9)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(4, 0, 4, 9)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(4, 0, 4, 9), named_args={"start": "20"}
                ),
            ),
            ListNode(
                ordered=True,
                main_node=True,
                start=21,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 21",
                                info=NodeInfo(context=generate_context(7, 2, 7, 9)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(7, 0, 7, 9)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(7, 0, 7, 9), named_args={"start": "auto"}
                ),
            ),
        ],
    )


def test_parse_numbered_list_do_not_continue_by_default():
    source = """
    # Item 1

    # Item 2
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=True,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 1",
                                info=NodeInfo(context=generate_context(1, 2, 1, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(1, 0, 1, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(1, 0, 1, 8)),
            ),
            ListNode(
                ordered=True,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "Item 2",
                                info=NodeInfo(context=generate_context(3, 2, 3, 8)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(3, 0, 3, 8)),
                    ),
                ],
                info=NodeInfo(context=generate_context(3, 0, 3, 8)),
            ),
        ],
    )


def test_parse_list_arguments():
    source = """
    [arg1, #tag1, *subtype1, key1=value1]
    * This is a list with one element
    """

    parser = runner(source)

    compare_nodes_sequence(
        parser.nodes,
        [
            ListNode(
                ordered=False,
                main_node=True,
                content=[
                    ListItemNode(
                        1,
                        content=[
                            TextNode(
                                "This is a list with one element",
                                info=NodeInfo(context=generate_context(2, 2, 2, 33)),
                            )
                        ],
                        info=NodeInfo(context=generate_context(2, 0, 2, 33)),
                    ),
                ],
                info=NodeInfo(
                    context=generate_context(2, 0, 2, 33),
                    unnamed_args=["arg1"],
                    named_args={"key1": "value1"},
                    tags=["tag1"],
                    subtype="subtype1",
                ),
            ),
        ],
    )


def test_parse_list_control():
    source = """
    :answer:44

    @if answer==42
    [arg1, arg2]
    . Some title
    * This is a list with one element
    """

    parser = runner(source)

    compare_nodes_sequence(parser.nodes, [])

    assert parser.arguments_buffer.arguments is None
    assert parser.label_buffer.labels == {}
    assert parser.control_buffer.control is None
