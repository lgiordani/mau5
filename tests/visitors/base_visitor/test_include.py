from mau.nodes.include import IncludeImageNode, IncludeNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_include_node():
    node = IncludeNode("ctype", ["uri1", "uri2"])

    expected = {
        "_type": "include",
        "content_type": "ctype",
        "uris": ["uri1", "uri2"],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_include_image_node():
    node = IncludeImageNode("uri")

    expected = {
        "_type": "include-image",
        "uri": "uri",
        "alt_text": None,
        "classes": [],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_include_image_node_alt_text_classes():
    node = IncludeImageNode("uri", "alt_text", ["class1", "class2"])

    expected = {
        "_type": "include-image",
        "uri": "uri",
        "alt_text": "alt_text",
        "classes": ["class1", "class2"],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
