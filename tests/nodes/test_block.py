from mau.nodes.block import BlockNodeData


def test_block_node_data():
    node_data = BlockNodeData()

    assert node_data.type == "block"
    assert node_data.asdict() == {
        "type": "block",
        "custom": {
            "classes": [],
            "engine": None,
            "preprocessor": None,
            "sections": {},
        },
    }
