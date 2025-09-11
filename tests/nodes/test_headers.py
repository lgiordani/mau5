from mau.nodes.headers import HeaderNodeContent


def test_header_node_content():
    node_content = HeaderNodeContent(level=42, anchor="someanchor")

    assert node_content.type == "header"
    assert node_content.level == 42
    assert node_content.anchor == "someanchor"
    assert node_content.asdict() == {
        "type": "header",
        "level": 42,
        "anchor": "someanchor",
    }
