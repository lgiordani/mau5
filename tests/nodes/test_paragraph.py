from mau.nodes.paragraph import ParagraphNodeContent


def test_paragraph_node_content():
    node_content = ParagraphNodeContent()

    assert node_content.type == "paragraph"
    assert list(node_content.allowed_keys.keys()) == ["content"]

    assert node_content.asdict() == {
        "type": "paragraph",
    }
