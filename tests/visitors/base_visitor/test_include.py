from mau.nodes.include import IncludeImageNode, IncludeNode
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_include_node():
    node = IncludeNode("ctype", ["uri1", "uri2"])

    expected = {
        "_type": "include",
        "_context": Context.empty().asdict(),
        "content_type": "ctype",
        "uris": ["uri1", "uri2"],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_include_image_node():
    node = IncludeImageNode("uri")

    expected = {
        "_type": "include-image",
        "_context": Context.empty().asdict(),
        "uri": "uri",
        "alt_text": None,
        "classes": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_include_image_node_alt_text_classes():
    node = IncludeImageNode("uri", "alt_text", ["class1", "class2"])

    expected = {
        "_type": "include-image",
        "_context": Context.empty().asdict(),
        "uri": "uri",
        "alt_text": "alt_text",
        "classes": ["class1", "class2"],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
