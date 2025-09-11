from mau.nodes.footnotes import FootnoteNodeContent


def test_footnote_node_content():
    node_content = FootnoteNodeContent()

    assert node_content.type == "footnote"
    assert node_content.asdict() == {"type": "footnote"}
