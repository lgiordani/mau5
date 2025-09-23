from mau.nodes.footnotes import FootnoteNodeContent


def test_footnote_node_content():
    node_content = FootnoteNodeContent("somename")

    assert node_content.type == "footnote"
    assert node_content.name == "somename"
    assert node_content.public_id is None
    assert node_content.private_id is None
    assert node_content.asdict() == {
        "type": "footnote",
        "name": "somename",
        "public_id": None,
        "private_id": None,
    }


def test_footnote_node_content_with_id():
    node_content = FootnoteNodeContent("somename", "some_public_id", "some_private_id")

    assert node_content.type == "footnote"
    assert node_content.name == "somename"
    assert node_content.public_id == "some_public_id"
    assert node_content.private_id == "some_private_id"
    assert node_content.asdict() == {
        "type": "footnote",
        "name": "somename",
        "public_id": "some_public_id",
        "private_id": "some_private_id",
    }
