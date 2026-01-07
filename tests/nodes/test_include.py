from mau.nodes.include import IncludeImageNodeData, IncludeNodeData


def test_include_node_content():
    node_content = IncludeNodeData("ctype", ["uri1", "uri2"])

    assert node_content.type == "include"
    assert node_content.content_type == "ctype"
    assert node_content.uris == ["uri1", "uri2"]
    assert node_content.asdict() == {
        "type": "include",
        "custom": {"content_type": "ctype", "uris": ["uri1", "uri2"], "labels": {}},
    }


def test_include_image_node_content():
    node_content = IncludeImageNodeData("uri")

    assert node_content.type == "include-image"
    assert node_content.uri == "uri"
    assert node_content.alt_text is None
    assert node_content.classes == []
    assert node_content.asdict() == {
        "type": "include-image",
        "custom": {"uri": "uri", "alt_text": None, "classes": [], "labels": {}},
    }


def test_include_image_node_content_alt_text_classes():
    node_content = IncludeImageNodeData("uri", "alt_text", ["class1", "class2"])

    assert node_content.type == "include-image"
    assert node_content.uri == "uri"
    assert node_content.alt_text == "alt_text"
    assert node_content.classes == ["class1", "class2"]
    assert node_content.asdict() == {
        "type": "include-image",
        "custom": {
            "uri": "uri",
            "alt_text": "alt_text",
            "classes": ["class1", "class2"],
            "labels": {},
        },
    }
