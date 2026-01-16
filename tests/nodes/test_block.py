from mau.nodes.block import BlockNode


def test_block_node_data():
    node = BlockNode()

    assert node.type == "block"
    assert node.asdict() == {
        "type": "block",
        "custom": {
            "classes": [],
            "engine": None,
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
    }
