from mau.nodes.command import TocItemNodeContent, TocNodeContent


def test_toc_node_content():
    node_content = TocNodeContent()

    assert node_content.type == "toc"
    assert list(node_content.allowed_keys.keys()) == ["nested_entries", "plain_entries"]
    assert node_content.asdict() == {
        "type": "toc",
    }


def test_toc_item_node_content():
    node_content = TocItemNodeContent(level=1, internal_id="someid")

    assert node_content.type == "toc-item"
    assert list(node_content.allowed_keys.keys()) == ["text", "entries"]
    assert node_content.level == 1
    assert node_content.internal_id == "someid"
    assert node_content.asdict() == {
        "type": "toc-item",
        "level": 1,
        "internal_id": "someid",
    }
