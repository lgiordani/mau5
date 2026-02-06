from mau.nodes.inline import (
    StyleNode,
    TextNode,
    VerbatimNode,
    WordNode,
)
from mau.test_helpers import check_node_with_content, check_visit_node
from mau.text_buffer import Context


def test_word_node():
    node = WordNode("somevalue")

    expected = {
        "_type": "word",
        "_context": Context.empty().asdict(),
        "value": "somevalue",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_text_node():
    node = TextNode("somevalue")

    expected = {
        "_type": "text",
        "_context": Context.empty().asdict(),
        "value": "somevalue",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_verbatim_node():
    node = VerbatimNode("somevalue")

    expected = {
        "_type": "verbatim",
        "_context": Context.empty().asdict(),
        "value": "somevalue",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_style_node_without_content():
    node = StyleNode("mystyle")

    expected = {
        "_type": "style",
        "_context": Context.empty().asdict(),
        "style": "mystyle",
        "content": [],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_style_node_with_content():
    node = StyleNode("mystyle")

    check_node_with_content(node)
