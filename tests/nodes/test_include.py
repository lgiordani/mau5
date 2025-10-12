from mau.nodes.include import IncludeImageNodeContent, IncludeNodeContent


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


def test_include_image_node_content():
    node_content = IncludeImageNodeContent("uri")

    assert node_content.type == "include-image"
    assert node_content.uri == "uri"
    assert node_content.alt_text is None
    assert node_content.classes == []
    assert list(node_content.allowed_keys.keys()) == ["title"]
    assert node_content.asdict() == {
        "type": "include-image",
        "uri": "uri",
        "alt_text": None,
        "classes": [],
    }


def test_include_image_node_content_alt_text_classes():
    node_content = IncludeImageNodeContent("uri", "alt_text", ["class1", "class2"])

    assert node_content.type == "include-image"
    assert node_content.uri == "uri"
    assert node_content.alt_text == "alt_text"
    assert node_content.classes == ["class1", "class2"]
    assert list(node_content.allowed_keys.keys()) == ["title"]
    assert node_content.asdict() == {
        "type": "include-image",
        "uri": "uri",
        "alt_text": "alt_text",
        "classes": ["class1", "class2"],
    }
