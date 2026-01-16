from mau.nodes.include import IncludeImageNode, IncludeNode
from mau.text_buffer import Context


def test_include_node():
    node = IncludeNode("ctype", ["uri1", "uri2"])

    assert node.type == "include"
    assert node.content_type == "ctype"
    assert node.uris == ["uri1", "uri2"]
    assert node.asdict() == {
        "type": "include",
        "custom": {
            "content_type": "ctype",
            "uris": ["uri1", "uri2"],
            "labels": {},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_include_image_node():
    node = IncludeImageNode("uri")

    assert node.type == "include-image"
    assert node.uri == "uri"
    assert node.alt_text is None
    assert node.classes == []
    assert node.asdict() == {
        "type": "include-image",
        "custom": {
            "uri": "uri",
            "alt_text": None,
            "classes": [],
            "labels": {},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_include_image_node_alt_text_classes():
    node = IncludeImageNode("uri", "alt_text", ["class1", "class2"])

    assert node.type == "include-image"
    assert node.uri == "uri"
    assert node.alt_text == "alt_text"
    assert node.classes == ["class1", "class2"]
    assert node.asdict() == {
        "type": "include-image",
        "custom": {
            "uri": "uri",
            "alt_text": "alt_text",
            "classes": ["class1", "class2"],
            "labels": {},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }
