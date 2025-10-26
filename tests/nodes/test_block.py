from mau.nodes.block import BlockNodeContent
from mau.nodes.command import BlockGroupNodeContent


def test_block_node_content():
    node_content = BlockNodeContent()

    assert node_content.type == "block"
    assert node_content.asdict() == {
        "type": "block",
        "classes": [],
        "engine": None,
        "preprocessor": None,
    }


def test_block_group_node_content():
    node_content = BlockGroupNodeContent("somename")

    assert node_content.type == "block-group"
    assert node_content.asdict() == {
        "type": "block-group",
        "name": "somename",
    }
