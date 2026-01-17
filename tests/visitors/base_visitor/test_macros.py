from mau.nodes.footnotes import FootnoteNode
from mau.nodes.headers import HeaderNode
from mau.nodes.macros import (
    MacroClassNode,
    MacroFootnoteNode,
    MacroHeaderNode,
    MacroImageNode,
    MacroLinkNode,
    MacroNode,
)
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_node_with_content, check_visit_node
from mau.text_buffer import Context


def test_macro_node():
    node = MacroNode("somename")

    expected = {
        "_type": "macro",
        "name": "somename",
        "unnamed_args": [],
        "named_args": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_node_args():
    node = MacroNode("somename", unnamed_args=["arg1"], named_args={"key1": "value1"})

    expected = {
        "_type": "macro",
        "name": "somename",
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_class_node_without_content():
    node = MacroClassNode(["class1", "class2"])

    expected = {
        "_type": "macro.class",
        "classes": ["class1", "class2"],
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_class_node_with_content():
    node = MacroClassNode(["class1", "class2"])
    check_node_with_content(node)


def test_macro_link_node_without_content():
    node = MacroLinkNode("sometarget")

    expected = {
        "_type": "macro.link",
        "target": "sometarget",
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_link_node_with_content():
    node = MacroLinkNode("sometarget")
    check_node_with_content(node)


def test_macro_image_node():
    node = MacroImageNode("someuri")

    expected = {
        "_type": "macro.image",
        "uri": "someuri",
        "alt_text": None,
        "width": None,
        "height": None,
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_image_node_parameters():
    node = MacroImageNode("someuri", "alt_text", "width", "height")

    expected = {
        "_type": "macro.image",
        "uri": "someuri",
        "alt_text": "alt_text",
        "width": "width",
        "height": "height",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_header_node():
    node = MacroHeaderNode("someid")

    expected = {
        "_type": "macro.header",
        "target_alias": "someid",
        "target_id": None,
        "content": [],
        "header": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_header_node_with_header():
    node = MacroHeaderNode("someid", header=HeaderNode(level=1))

    expected = {
        "_type": "macro.header",
        "target_alias": "someid",
        "target_id": None,
        "content": [],
        "header": {
            "_type": "header",
            "alias": None,
            "internal_id": None,
            "level": 1,
            "labels": {},
            "content": [],
            "_info": {
                "context": Context.empty().asdict(),
                "unnamed_args": [],
                "named_args": {},
                "tags": [],
                "subtype": None,
            },
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_header_node_parameters():
    node = MacroHeaderNode("someid", target_id="targetid")

    expected = {
        "_type": "macro.header",
        "target_alias": "someid",
        "target_id": "targetid",
        "content": [],
        "header": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_macro_footnote_node_parameters():
    node = MacroFootnoteNode(footnote=FootnoteNode(name="somename"))

    expected = {
        "_type": "macro.footnote",
        "footnote": {
            "_type": "footnote",
            "name": "somename",
            "public_id": None,
            "private_id": None,
            "content": [],
            "_info": NodeInfo.empty().asdict(),
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
