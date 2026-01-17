from mau.nodes.inline import (
    RawNode,
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
        "value": "somevalue",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_text_node():
    node = TextNode("somevalue")

    expected = {
        "_type": "text",
        "value": "somevalue",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_raw_node():
    node = RawNode("somevalue")

    expected = {
        "_type": "raw",
        "value": "somevalue",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_verbatim_node():
    node = VerbatimNode("somevalue")

    expected = {
        "_type": "verbatim",
        "value": "somevalue",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_style_node_without_content():
    node = StyleNode("mystyle")

    expected = {
        "_type": "style",
        "style": "mystyle",
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_style_node_with_content():
    node = StyleNode("mystyle")

    check_node_with_content(node)
