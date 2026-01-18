from mau.nodes.block import BlockNode
from mau.nodes.commands import BlockGroupNode, FootnotesNode, TocItemNode, TocNode
from mau.nodes.footnotes import FootnoteNode
from mau.nodes.headers import HeaderNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_footnotes_node_empty():
    node = FootnotesNode()

    expected = {
        "_type": "footnotes",
        "footnotes": [],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_footnotes_node():
    footnotes = [
        FootnoteNode("somename1"),
        FootnoteNode("somename2"),
    ]
    node = FootnotesNode(footnotes=footnotes)

    expected = {
        "_type": "footnotes",
        "footnotes": [
            {
                "_type": "footnote",
                "name": "somename1",
                "public_id": None,
                "private_id": None,
                "content": [],
                "_info": NodeInfo.empty().asdict(),
            },
            {
                "_type": "footnote",
                "name": "somename2",
                "public_id": None,
                "private_id": None,
                "content": [],
                "_info": NodeInfo.empty().asdict(),
            },
        ],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_toc_item_node_without_entries():
    node = TocItemNode(
        header=HeaderNode(level=1),
        entries=[],
    )

    expected = {
        "_type": "toc-item",
        "entries": [],
        "header": {
            "_type": "header",
            "level": 1,
            "internal_id": None,
            "alias": None,
            "labels": {},
            "content": [],
            "_info": NodeInfo.empty().asdict(),
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_toc_item_node_with_entries():
    toc_item_child = TocItemNode(
        header=HeaderNode(level=2),
        entries=[],
    )

    node = TocItemNode(
        header=HeaderNode(level=1),
        entries=[toc_item_child],
    )

    expected = {
        "_type": "toc-item",
        "entries": [
            {
                "_type": "toc-item",
                "entries": [],
                "header": {
                    "_type": "header",
                    "level": 2,
                    "internal_id": None,
                    "alias": None,
                    "labels": {},
                    "content": [],
                    "_info": NodeInfo.empty().asdict(),
                },
                "_info": NodeInfo.empty().asdict(),
            }
        ],
        "header": {
            "_type": "header",
            "level": 1,
            "internal_id": None,
            "alias": None,
            "labels": {},
            "content": [],
            "_info": NodeInfo.empty().asdict(),
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_toc_node():
    node = TocNode()

    expected = {
        "_type": "toc",
        "plain_entries": [],
        "nested_entries": [],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_block_group_node_empty():
    node = BlockGroupNode("somename")

    expected = {
        "_type": "block-group",
        "name": "somename",
        "blocks": {},
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_block_group_node_with_blocks():
    block_node1 = BlockNode()
    block_node2 = BlockNode()

    node = BlockGroupNode(
        "somename", blocks={"position1": block_node1, "position2": block_node2}
    )

    expected = {
        "_type": "block-group",
        "name": "somename",
        "labels": {},
        "blocks": {
            "position1": {
                "_type": "block",
                "classes": [],
                "content": [],
                "labels": {},
                "_info": NodeInfo.empty().asdict(),
            },
            "position2": {
                "_type": "block",
                "classes": [],
                "content": [],
                "labels": {},
                "_info": NodeInfo.empty().asdict(),
            },
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
