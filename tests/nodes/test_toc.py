from mau.nodes.toc import TocNodeContent


def test_toc_node_content():
    node_content = TocNodeContent()

    assert node_content.type == "toc"
    assert list(node_content.allowed_keys.keys()) == ["nested_entries", "plain_entries"]
    assert node_content.asdict() == {
        "type": "toc",
    }


# TODO test TocItemnodecontent
