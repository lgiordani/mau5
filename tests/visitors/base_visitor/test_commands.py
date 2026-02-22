from mau.nodes.block import BlockNode
from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.include import (
    BlockGroupNode,
    FootnotesItemNode,
    FootnotesNode,
    TocItemNode,
    TocNode,
)
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_footnotes_node_empty():
    node = FootnotesNode()

    expected = {
        "_context": Context.empty().asdict(),
        "_type": "footnotes",
        "footnotes": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_footnotes_node():
    footnotes_items = [
        FootnotesItemNode(footnote=FootnoteNode("somename1")),
        FootnotesItemNode(footnote=FootnoteNode("somename2")),
    ]

    node = FootnotesNode(footnotes=footnotes_items)

    expected = {
        "_context": Context.empty().asdict(),
        "_type": "footnotes",
        "footnotes": [
            {
                "_type": "footnotes-item",
                "_context": Context.empty().asdict(),
                "footnote": {
                    "_context": Context.empty().asdict(),
                    "_type": "footnote",
                    "content": [],
                    "internal_id": None,
                    "name": "somename1",
                    "named_args": {},
                    "parent": {},
                    "public_id": None,
                    "subtype": None,
                    "tags": [],
                    "internal_tags": [],
                    "unnamed_args": [],
                },
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
            {
                "_type": "footnotes-item",
                "_context": Context.empty().asdict(),
                "footnote": {
                    "_context": Context.empty().asdict(),
                    "_type": "footnote",
                    "content": [],
                    "internal_id": None,
                    "name": "somename2",
                    "named_args": {},
                    "parent": {},
                    "public_id": None,
                    "subtype": None,
                    "tags": [],
                    "internal_tags": [],
                    "unnamed_args": [],
                },
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
        ],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_toc_item_node_without_entries():
    node = TocItemNode(
        header=HeaderNode(level=1),
        entries=[],
    )

    expected = {
        "_type": "toc-item",
        "_context": Context.empty().asdict(),
        "entries": [],
        "header": {
            "_type": "header",
            "_context": Context.empty().asdict(),
            "level": 1,
            "internal_id": None,
            "name": None,
            "labels": {},
            "content": [],
            "named_args": {},
            "parent": {},
            "subtype": None,
            "tags": [],
            "internal_tags": [],
            "unnamed_args": [],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
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
        "_context": Context.empty().asdict(),
        "entries": [
            {
                "_type": "toc-item",
                "_context": Context.empty().asdict(),
                "entries": [],
                "header": {
                    "_type": "header",
                    "_context": Context.empty().asdict(),
                    "level": 2,
                    "internal_id": None,
                    "name": None,
                    "labels": {},
                    "content": [],
                    "named_args": {},
                    "parent": {},
                    "subtype": None,
                    "tags": [],
                    "internal_tags": [],
                    "unnamed_args": [],
                },
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            }
        ],
        "header": {
            "_type": "header",
            "_context": Context.empty().asdict(),
            "level": 1,
            "internal_id": None,
            "name": None,
            "labels": {},
            "content": [],
            "named_args": {},
            "parent": {},
            "subtype": None,
            "tags": [],
            "internal_tags": [],
            "unnamed_args": [],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_toc_node():
    node = TocNode()

    expected = {
        "_type": "toc",
        "_context": Context.empty().asdict(),
        "plain_entries": [],
        "nested_entries": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_block_group_node_empty():
    node = BlockGroupNode("somename")

    expected = {
        "_type": "blockgroup",
        "_context": Context.empty().asdict(),
        "name": "somename",
        "blocks": {},
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_block_group_node_with_blocks():
    block_node1 = BlockNode()
    block_node2 = BlockNode()

    node = BlockGroupNode(
        "somename", blocks={"position1": block_node1, "position2": block_node2}
    )

    expected = {
        "_type": "blockgroup",
        "_context": Context.empty().asdict(),
        "name": "somename",
        "labels": {},
        "blocks": {
            "position1": {
                "_type": "block",
                "_context": Context.empty().asdict(),
                "classes": [],
                "content": [],
                "labels": {},
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
            "position2": {
                "_type": "block",
                "_context": Context.empty().asdict(),
                "classes": [],
                "content": [],
                "labels": {},
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
