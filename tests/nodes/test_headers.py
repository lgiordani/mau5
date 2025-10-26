from mau.nodes.headers import HeaderNodeContent


def test_header_node_content():
    node_content = HeaderNodeContent(
        level=42,
        internal_id="some_internal_id",
        external_id="some_external_id",
    )

    assert node_content.type == "header"
    assert node_content.level == 42
    assert node_content.internal_id == "some_internal_id"
    assert node_content.external_id == "some_external_id"
    assert node_content.asdict() == {
        "type": "header",
        "level": 42,
        "internal_id": "some_internal_id",
        "external_id": "some_external_id",
    }
