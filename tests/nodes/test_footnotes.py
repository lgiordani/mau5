from mau.nodes.footnotes import FootnoteNodeData


def test_macro_footnote_node_data_parameters():
    node_data = FootnoteNodeData("somename")

    assert node_data.type == "footnote"
    assert node_data.name == "somename"
    assert node_data.public_id is None
    assert node_data.private_id is None

    assert node_data.asdict() == {
        "type": "footnote",
        "custom": {
            "name": "somename",
            "public_id": None,
            "private_id": None,
            "content": [],
        },
    }
