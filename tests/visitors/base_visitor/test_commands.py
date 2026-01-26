from mau.nodes.block import BlockNode
from mau.nodes.command import (
    BlockGroupNode,
    FootnotesItemNode,
    FootnotesNode,
    TocItemNode,
    TocNode,
)
from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_footnotes_node_empty():
    node = FootnotesNode()

    expected = {
        "_type": "footnotes",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "footnotes": [],
        "labels": {},
    }

    check_visit_node(node, expected)


def test_footnotes_node():
    footnotes_items = [
        FootnotesItemNode(footnote=FootnoteNode("somename1")),
        FootnotesItemNode(footnote=FootnoteNode("somename2")),
    ]

    node = FootnotesNode(footnotes=footnotes_items)

    expected = {
        "_type": "footnotes",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "footnotes": [
            {
                "_type": "footnotes-item",
                "_parent_info": {},
                "_info": NodeInfo.empty().asdict(),
                "footnote": {
                    "_type": "footnote",
                    "_parent_info": {},
                    "_info": NodeInfo.empty().asdict(),
                    "name": "somename1",
                    "public_id": None,
                    "internal_id": None,
                    "content": [],
                },
            },
            {
                "_type": "footnotes-item",
                "_parent_info": {},
                "_info": NodeInfo.empty().asdict(),
                "footnote": {
                    "_type": "footnote",
                    "_parent_info": {},
                    "_info": NodeInfo.empty().asdict(),
                    "name": "somename2",
                    "public_id": None,
                    "internal_id": None,
                    "content": [],
                },
            },
        ],
        "labels": {},
    }

    check_visit_node(node, expected)


def test_toc_item_node_without_entries():
    node = TocItemNode(
        header=HeaderNode(level=1),
        entries=[],
    )

    expected = {
        "_type": "toc-item",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "entries": [],
        "header": {
            "_type": "header",
            "_parent_info": {},
            "_info": NodeInfo.empty().asdict(),
            "level": 1,
            "internal_id": None,
            "name": None,
            "labels": {},
            "content": [],
        },
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
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "entries": [
            {
                "_type": "toc-item",
                "_parent_info": {},
                "_info": NodeInfo.empty().asdict(),
                "entries": [],
                "header": {
                    "_type": "header",
                    "_parent_info": {},
                    "_info": NodeInfo.empty().asdict(),
                    "level": 2,
                    "internal_id": None,
                    "name": None,
                    "labels": {},
                    "content": [],
                },
            }
        ],
        "header": {
            "_type": "header",
            "_parent_info": {},
            "_info": NodeInfo.empty().asdict(),
            "level": 1,
            "internal_id": None,
            "name": None,
            "labels": {},
            "content": [],
        },
    }

    check_visit_node(node, expected)


def test_toc_node():
    node = TocNode()

    expected = {
        "_type": "toc",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "plain_entries": [],
        "nested_entries": [],
        "labels": {},
    }

    check_visit_node(node, expected)


def test_block_group_node_empty():
    node = BlockGroupNode("somename")

    expected = {
        "_type": "block-group",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "name": "somename",
        "blocks": {},
        "labels": {},
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
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "name": "somename",
        "labels": {},
        "blocks": {
            "position1": {
                "_type": "block",
                "_parent_info": {},
                "_info": NodeInfo.empty().asdict(),
                "classes": [],
                "content": [],
                "labels": {},
            },
            "position2": {
                "_type": "block",
                "_parent_info": {},
                "_info": NodeInfo.empty().asdict(),
                "classes": [],
                "content": [],
                "labels": {},
            },
        },
    }

    check_visit_node(node, expected)
