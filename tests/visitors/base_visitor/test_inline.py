from mau.nodes.inline import (
    StyleNode,
    TextNode,
    VerbatimNode,
    WordNode,
)
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_node_with_content, check_visit_node


def test_word_node():
    node = WordNode("somevalue")

    expected = {
        "_type": "word",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "somevalue",
    }

    check_visit_node(node, expected)


def test_text_node():
    node = TextNode("somevalue")

    expected = {
        "_type": "text",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "somevalue",
    }

    check_visit_node(node, expected)


def test_verbatim_node():
    node = VerbatimNode("somevalue")

    expected = {
        "_type": "verbatim",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "somevalue",
    }

    check_visit_node(node, expected)


def test_style_node_without_content():
    node = StyleNode("mystyle")

    expected = {
        "_type": "style",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "style": "mystyle",
        "content": [],
    }

    check_visit_node(node, expected)


def test_style_node_with_content():
    node = StyleNode("mystyle")

    check_node_with_content(node)
