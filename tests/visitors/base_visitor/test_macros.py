from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.macro import (
    MacroClassNode,
    MacroFootnoteNode,
    MacroHeaderNode,
    MacroImageNode,
    MacroLinkNode,
    MacroNode,
    MacroRawNode,
    MacroUnicodeNode,
)
from mau.nodes.node_arguments import NodeArguments
from mau.test_helpers import check_node_with_content, check_visit_node
from mau.text_buffer import Context


def test_macro_node():
    node = MacroNode("somename")

    expected = {
        "_type": "macro",
        "_context": Context.empty().asdict(),
        "name": "somename",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_node_args():
    node = MacroNode(
        "somename",
        arguments=NodeArguments(
            unnamed_args=["arg1"],
            named_args={"key1": "value1"},
            tags=["tag1"],
            subtype="subtype1",
        ),
    )

    expected = {
        "_type": "macro",
        "_context": Context.empty().asdict(),
        "name": "somename",
        "parent": {},
        "subtype": "subtype1",
        "tags": ["tag1"],
        "internal_tags": [],
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
    }

    check_visit_node(node, expected)


def test_macro_class_node_without_content():
    node = MacroClassNode(["class1", "class2"])

    expected = {
        "_type": "macro-class",
        "_context": Context.empty().asdict(),
        "classes": ["class1", "class2"],
        "content": [],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_class_node_with_content():
    node = MacroClassNode(["class1", "class2"])
    check_node_with_content(node)


def test_macro_link_node_without_content():
    node = MacroLinkNode("sometarget")

    expected = {
        "_type": "macro-link",
        "_context": Context.empty().asdict(),
        "target": "sometarget",
        "content": [],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_link_node_with_content():
    node = MacroLinkNode("sometarget")
    check_node_with_content(node)


def test_macro_image_node():
    node = MacroImageNode("someuri")

    expected = {
        "_type": "macro-image",
        "_context": Context.empty().asdict(),
        "uri": "someuri",
        "alt_text": None,
        "width": None,
        "height": None,
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_image_node_parameters():
    node = MacroImageNode("someuri", "alt_text", "width", "height")

    expected = {
        "_type": "macro-image",
        "_context": Context.empty().asdict(),
        "uri": "someuri",
        "alt_text": "alt_text",
        "width": "width",
        "height": "height",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_header_node():
    node = MacroHeaderNode("someid")

    expected = {
        "_type": "macro-header",
        "_context": Context.empty().asdict(),
        "target_name": "someid",
        "content": [],
        "header": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_header_node_with_header():
    node = MacroHeaderNode("someid", header=HeaderNode(level=1))

    expected = {
        "_type": "macro-header",
        "_context": Context.empty().asdict(),
        "target_name": "someid",
        "content": [],
        "header": {
            "_type": "header",
            "_context": Context.empty().asdict(),
            "name": None,
            "internal_id": None,
            "level": 1,
            "labels": {},
            "content": [],
            "named_args": {},
            "parent": {},
            "subtype": None,
            "tags": [],
            "internal_tags": [],
            "unnamed_args": [],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_header_node_parameters():
    node = MacroHeaderNode(target_name="somename")

    expected = {
        "_type": "macro-header",
        "_context": Context.empty().asdict(),
        "target_name": "somename",
        "content": [],
        "header": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_footnote_node_parameters():
    node = MacroFootnoteNode(name="somename", footnote=FootnoteNode(name="somename"))

    expected = {
        "_type": "macro-footnote",
        "_context": Context.empty().asdict(),
        "footnote": {
            "_type": "footnote",
            "_context": Context.empty().asdict(),
            "name": "somename",
            "public_id": None,
            "internal_id": None,
            "content": [],
            "named_args": {},
            "parent": {},
            "subtype": None,
            "tags": [],
            "internal_tags": [],
            "unnamed_args": [],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_unicode():
    node = MacroUnicodeNode("1F30B")

    expected = {
        "_type": "macro-unicode",
        "_context": Context.empty().asdict(),
        "value": "1F30B",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_macro_raw():
    node = MacroRawNode("somevalue")

    expected = {
        "_type": "macro-raw",
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
