from unittest.mock import call, patch

from mau.nodes.command import (
    TocItemNodeContent,
    TocNodeContent,
)
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.managers.toc_manager import (
    TocManager,
    add_nodes_under_level,
    header_to_toc_item,
)
from mau.test_helpers import (
    compare_node,
    compare_nodes,
    generate_context,
)


def test_toc_manager_init():
    tm = TocManager()

    assert tm.headers == []
    assert tm.toc_nodes == []


def test_toc_manager_add_header():
    tm = TocManager()
    test_node = Node(content=HeaderNodeContent(1))

    tm.add_header(test_node)

    assert tm.headers == [test_node]


def test_toc_manager_add_toc_node():
    tm = TocManager()
    test_node = Node(content=TocNodeContent())

    tm.add_toc_node(test_node)

    assert tm.toc_nodes == [test_node]


def test_toc_manager_update():
    test_tm = TocManager()
    test_header_node = Node(content=HeaderNodeContent(1))
    test_toc_node = Node(content=TocNodeContent())
    test_tm.add_header(test_header_node)
    test_tm.add_toc_node(test_toc_node)

    tm = TocManager()
    tm.update(test_tm)

    assert tm.headers == [test_header_node]
    assert tm.toc_nodes == [test_toc_node]


def test_header_to_toc_item():
    header = Node(
        content=HeaderNodeContent(1, "A"),
        children={
            "text": [
                Node(
                    content=TextNodeContent("Header A"),
                    info=NodeInfo(context=generate_context(3, 2, 3, 15)),
                )
            ]
        },
    )

    expected_toc_item = Node(
        content=TocItemNodeContent(1, "A"),
        children={
            "entries": [],
            "text": [
                Node(
                    content=TextNodeContent("Header A"),
                    info=NodeInfo(context=generate_context(3, 2, 3, 15)),
                )
            ],
        },
    )

    compare_node(header_to_toc_item(header), expected_toc_item)


def test_add_nodes_without_nesting():
    node_header_a = Node(content=HeaderNodeContent(1, "A"))
    node_header_b = Node(content=HeaderNodeContent(1, "B"))
    node_header_c = Node(content=HeaderNodeContent(1, "C"))

    node_toc_item_a = Node(
        content=TocItemNodeContent(1, "A"),
        children={
            "text": [],
            "entries": [],
        },
    )
    node_toc_item_b = Node(
        content=TocItemNodeContent(1, "B"),
        children={
            "text": [],
            "entries": [],
        },
    )
    node_toc_item_c = Node(
        content=TocItemNodeContent(1, "C"),
        children={
            "text": [],
            "entries": [],
        },
    )

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[Node[TocItemNodeContent]] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_nodes(children, [node_toc_item_a, node_toc_item_b, node_toc_item_c])

    assert node_header_a.children == {"text": []}
    assert node_header_b.children == {"text": []}
    assert node_header_c.children == {"text": []}


def test_add_nodes_with_nesting():
    node_header_a = Node(content=HeaderNodeContent(1, "A"))
    node_header_b = Node(content=HeaderNodeContent(2, "B"))
    node_header_c = Node(content=HeaderNodeContent(3, "C"))
    node_header_d = Node(content=HeaderNodeContent(2, "D"))
    node_header_e = Node(content=HeaderNodeContent(2, "E"))
    node_header_f = Node(content=HeaderNodeContent(1, "F"))
    node_header_g = Node(content=HeaderNodeContent(3, "G"))

    node_toc_item_c = Node(
        content=TocItemNodeContent(3, "C"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_b = Node(
        content=TocItemNodeContent(2, "B"),
        children={
            "text": [],
            "entries": [node_toc_item_c],
        },
    )

    node_toc_item_d = Node(
        content=TocItemNodeContent(2, "D"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_e = Node(
        content=TocItemNodeContent(2, "E"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_a = Node(
        content=TocItemNodeContent(1, "A"),
        children={
            "text": [],
            "entries": [node_toc_item_b, node_toc_item_d, node_toc_item_e],
        },
    )

    node_toc_item_g = Node(
        content=TocItemNodeContent(3, "G"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_f = Node(
        content=TocItemNodeContent(1, "F"),
        children={
            "text": [],
            "entries": [node_toc_item_g],
        },
    )

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
        node_header_d,
        node_header_e,
        node_header_f,
        node_header_g,
    ]

    children: list[Node[TocItemNodeContent]] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_nodes(children, [node_toc_item_a, node_toc_item_f])

    assert node_header_a.children == {"text": []}
    assert node_header_b.children == {"text": []}
    assert node_header_c.children == {"text": []}
    assert node_header_d.children == {"text": []}
    assert node_header_e.children == {"text": []}
    assert node_header_f.children == {"text": []}
    assert node_header_g.children == {"text": []}


def test_add_nodes_under_level_starts_with_any_level():
    node_header_a = Node(content=HeaderNodeContent(3, "A"))
    node_header_b = Node(content=HeaderNodeContent(2, "B"))
    node_header_c = Node(content=HeaderNodeContent(3, "C"))

    node_toc_item_c = Node(
        content=TocItemNodeContent(3, "C"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_b = Node(
        content=TocItemNodeContent(2, "B"),
        children={
            "text": [],
            "entries": [node_toc_item_c],
        },
    )

    node_toc_item_a = Node(
        content=TocItemNodeContent(3, "A"),
        children={
            "text": [],
            "entries": [],
        },
    )

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[Node[TocItemNodeContent]] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_nodes(children, [node_toc_item_a, node_toc_item_b])

    assert node_header_a.children == {"text": []}
    assert node_header_b.children == {"text": []}
    assert node_header_c.children == {"text": []}


def test_add_nodes_under_level_can_terminate_with_single_node():
    node_header_a = Node(content=HeaderNodeContent(3, "A"))
    node_header_b = Node(content=HeaderNodeContent(2, "B"))
    node_header_c = Node(content=HeaderNodeContent(1, "C"))

    node_toc_item_a = Node(
        content=TocItemNodeContent(3, "A"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_b = Node(
        content=TocItemNodeContent(2, "B"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_c = Node(
        content=TocItemNodeContent(1, "C"),
        children={
            "text": [],
            "entries": [],
        },
    )

    nodes = [
        node_header_a,
        node_header_b,
        node_header_c,
    ]

    children: list[Node[TocItemNodeContent]] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    compare_nodes(children, [node_toc_item_a, node_toc_item_b, node_toc_item_c])

    assert node_header_a.children == {"text": []}
    assert node_header_b.children == {"text": []}
    assert node_header_c.children == {"text": []}


@patch("mau.parsers.managers.toc_manager.default_header_internal_id")
def test_process(mock_default_header_internal_id):
    mock_default_header_internal_id.return_value = "some_uid"

    node_header_a = Node(content=HeaderNodeContent(1))
    node_header_b = Node(content=HeaderNodeContent(2))

    node_toc_item_b = Node(
        content=TocItemNodeContent(2, "some_uid"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_a = Node(
        content=TocItemNodeContent(1, "some_uid"),
        children={
            "text": [],
            "entries": [node_toc_item_b],
        },
    )

    header_nodes = [
        node_header_a,
        node_header_b,
    ]

    tm = TocManager()
    tm.headers = header_nodes
    test_toc_node = Node(content=TocNodeContent())
    tm.add_toc_node(test_toc_node)

    tm.process()

    compare_nodes(test_toc_node.children["plain_entries"], header_nodes)
    compare_nodes(test_toc_node.children["nested_entries"], [node_toc_item_a])
    assert mock_default_header_internal_id.mock_calls == [
        call(node_header_a),
        call(node_header_b),
    ]


def test_process_internal_id():
    node_header_a = Node(content=HeaderNodeContent(1, "A"))
    node_header_b = Node(content=HeaderNodeContent(2, "B"))

    node_toc_item_b = Node(
        content=TocItemNodeContent(2, "B"),
        children={
            "text": [],
            "entries": [],
        },
    )

    node_toc_item_a = Node(
        content=TocItemNodeContent(1, "A"),
        children={
            "text": [],
            "entries": [node_toc_item_b],
        },
    )

    header_nodes = [
        node_header_a,
        node_header_b,
    ]

    tm = TocManager()
    tm.headers = header_nodes
    test_toc_node = Node(content=TocNodeContent())
    tm.add_toc_node(test_toc_node)

    tm.process()

    compare_nodes(test_toc_node.children["plain_entries"], header_nodes)
    compare_nodes(test_toc_node.children["nested_entries"], [node_toc_item_a])
