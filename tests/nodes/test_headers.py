from mau.nodes.headers import HeaderNodeContent


def test_header_node_content():
    node_content = HeaderNodeContent(level=42, unique_id="someuniqueid")

    assert node_content.type == "header"
    assert node_content.level == 42
    assert node_content.unique_id == "someuniqueid"
    assert node_content.asdict() == {
        "type": "header",
        "level": 42,
        "unique_id": "someuniqueid",
    }
