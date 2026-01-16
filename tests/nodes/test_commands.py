from mau.nodes.node import Node
from mau.nodes.block import BlockNode
from mau.nodes.commands import FootnotesNode, TocItemNode, TocNode
from mau.nodes.footnotes import FootnoteNode
from mau.nodes.headers import HeaderNode
from mau.nodes.commands import BlockGroupNode


def test_footnotes_node_empty():
    node = FootnotesNode()

    assert node.type == "footnotes"
    assert node.footnotes == []

    assert node.asdict() == {
        "type": "footnotes",
        "custom": {"footnotes": [], "labels": {}},
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_footnotes_node():
    footnotes = [
        FootnoteNode("somename1"),
        FootnoteNode("somename2"),
    ]
    node = FootnotesNode(footnotes=footnotes)

    assert node.type == "footnotes"
    assert node.footnotes == footnotes

    assert node.asdict() == {
        "type": "footnotes",
        "custom": {
            "footnotes": [
                {
                    "type": "footnote",
                    "custom": {
                        "name": "somename1",
                        "public_id": None,
                        "private_id": None,
                        "content": [],
                    },
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
                {
                    "type": "footnote",
                    "custom": {
                        "name": "somename2",
                        "public_id": None,
                        "private_id": None,
                        "content": [],
                    },
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
            ],
            "labels": {},
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_toc_item_node_without_entries():
    toc_item = TocItemNode(
        header=HeaderNode(level=1),
        entries=[],
    )

    assert toc_item.type == "toc.item"
    assert toc_item.entries == []

    assert toc_item.asdict() == {
        "type": "toc.item",
        "custom": {
            "entries": [],
            "header": {
                "type": "header",
                "custom": {
                    "level": 1,
                    "internal_id": None,
                    "alias": None,
                    "labels": {},
                    "content": [],
                },
                "info": {
                    "context": {
                        "end_column": 0,
                        "end_line": 0,
                        "source": None,
                        "start_column": 0,
                        "start_line": 0,
                    },
                    "named_args": {},
                    "subtype": None,
                    "tags": [],
                    "unnamed_args": [],
                },
            },
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_toc_item_node_with_entries():
    toc_item_child = TocItemNode(
        header=HeaderNode(level=2),
        entries=[],
    )

    toc_item = TocItemNode(
        header=HeaderNode(level=1),
        entries=[toc_item_child],
    )

    assert toc_item.type == "toc.item"
    assert toc_item.entries == [toc_item_child]

    assert toc_item.asdict() == {
        "type": "toc.item",
        "custom": {
            "entries": [
                {
                    "type": "toc.item",
                    "custom": {
                        "entries": [],
                        "header": {
                            "type": "header",
                            "custom": {
                                "level": 2,
                                "internal_id": None,
                                "alias": None,
                                "labels": {},
                                "content": [],
                            },
                            "info": {
                                "context": {
                                    "end_column": 0,
                                    "end_line": 0,
                                    "source": None,
                                    "start_column": 0,
                                    "start_line": 0,
                                },
                                "named_args": {},
                                "subtype": None,
                                "tags": [],
                                "unnamed_args": [],
                            },
                        },
                    },
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                }
            ],
            "header": {
                "type": "header",
                "custom": {
                    "level": 1,
                    "internal_id": None,
                    "alias": None,
                    "labels": {},
                    "content": [],
                },
                "info": {
                    "context": {
                        "end_column": 0,
                        "end_line": 0,
                        "source": None,
                        "start_column": 0,
                        "start_line": 0,
                    },
                    "named_args": {},
                    "subtype": None,
                    "tags": [],
                    "unnamed_args": [],
                },
            },
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_block_group_node_empty():
    node = BlockGroupNode("somename")

    assert node.type == "block-group"
    assert node.asdict() == {
        "type": "block-group",
        "custom": {
            "name": "somename",
            "blocks": {},
            "labels": {},
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_block_group_node_with_blocks():
    block_node1 = BlockNode()
    block_node2 = BlockNode()

    node = BlockGroupNode(
        "somename", blocks={"position1": block_node1, "position2": block_node2}
    )

    assert node.type == "block-group"
    assert node.asdict() == {
        "type": "block-group",
        "custom": {
            "name": "somename",
            "labels": {},
            "blocks": {
                "position1": {
                    "type": "block",
                    "custom": {
                        "classes": [],
                        "content": [],
                        "engine": None,
                        "labels": {},
                    },
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
                "position2": {
                    "type": "block",
                    "custom": {
                        "classes": [],
                        "content": [],
                        "engine": None,
                        "labels": {},
                    },
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
            },
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_toc_node():
    node = TocNode()

    assert node.type == "toc"
    assert node.plain_entries == []
    assert node.nested_entries == []

    assert node.asdict() == {
        "type": "toc",
        "custom": {
            "plain_entries": [],
            "nested_entries": [],
            "labels": {},
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }
