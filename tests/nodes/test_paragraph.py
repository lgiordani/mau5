from mau.nodes.paragraph import ParagraphLineNodeContent, ParagraphNodeContent


def test_paragraph_node_content():
    node_content = ParagraphNodeContent()

    assert node_content.type == "paragraph"
    assert list(node_content.allowed_keys.keys()) == ["content"]

    assert node_content.asdict() == {
        "type": "paragraph",
    }


def test_paragraph_line_node_content():
    node_content = ParagraphLineNodeContent()

    assert node_content.type == "paragraph-line"
    assert list(node_content.allowed_keys.keys()) == ["content"]

    assert node_content.asdict() == {
        "type": "paragraph-line",
    }
