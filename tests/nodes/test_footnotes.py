from mau.nodes.footnotes import FootnoteNodeContent


def test_footnote_node_content():
    node_content = FootnoteNodeContent("somename")

    assert node_content.type == "footnote"
    assert node_content.name == "somename"
    assert node_content.id is None
    assert node_content.asdict() == {
        "type": "footnote",
        "name": "somename",
        "id": None,
    }


def test_footnote_node_content_with_id():
    node_content = FootnoteNodeContent("somename", "someid")

    assert node_content.type == "footnote"
    assert node_content.name == "somename"
    assert node_content.id == "someid"
    assert node_content.asdict() == {
        "type": "footnote",
        "name": "somename",
        "id": "someid",
    }
