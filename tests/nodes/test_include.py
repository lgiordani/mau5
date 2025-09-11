from mau.nodes.include import IncludeNodeContent


def test_include_node_content():
    node_content = IncludeNodeContent("ctype", ["uri1", "uri2"])

    assert node_content.type == "include"
    assert node_content.content_type == "ctype"
    assert node_content.uris == ["uri1", "uri2"]
    assert list(node_content.allowed_keys.keys()) == ["title"]
    assert node_content.asdict() == {
        "type": "include",
        "content_type": "ctype",
        "uris": ["uri1", "uri2"],
    }
