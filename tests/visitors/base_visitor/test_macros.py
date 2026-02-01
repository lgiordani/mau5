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
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_node_with_content, check_visit_node


def test_macro_node():
    node = MacroNode("somename")

    expected = {
        "_type": "macro",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "name": "somename",
        "unnamed_args": [],
        "named_args": {},
    }

    check_visit_node(node, expected)


def test_macro_node_args():
    node = MacroNode("somename", unnamed_args=["arg1"], named_args={"key1": "value1"})

    expected = {
        "_type": "macro",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "name": "somename",
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
    }

    check_visit_node(node, expected)


def test_macro_class_node_without_content():
    node = MacroClassNode(["class1", "class2"])

    expected = {
        "_type": "macro.class",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "classes": ["class1", "class2"],
        "content": [],
    }

    check_visit_node(node, expected)


def test_macro_class_node_with_content():
    node = MacroClassNode(["class1", "class2"])
    check_node_with_content(node)


def test_macro_link_node_without_content():
    node = MacroLinkNode("sometarget")

    expected = {
        "_type": "macro.link",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "target": "sometarget",
        "content": [],
    }

    check_visit_node(node, expected)


def test_macro_link_node_with_content():
    node = MacroLinkNode("sometarget")
    check_node_with_content(node)


def test_macro_image_node():
    node = MacroImageNode("someuri")

    expected = {
        "_type": "macro.image",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "uri": "someuri",
        "alt_text": None,
        "width": None,
        "height": None,
    }

    check_visit_node(node, expected)


def test_macro_image_node_parameters():
    node = MacroImageNode("someuri", "alt_text", "width", "height")

    expected = {
        "_type": "macro.image",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "uri": "someuri",
        "alt_text": "alt_text",
        "width": "width",
        "height": "height",
    }

    check_visit_node(node, expected)


def test_macro_header_node():
    node = MacroHeaderNode("someid")

    expected = {
        "_type": "macro.header",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "target_name": "someid",
        "content": [],
        "header": {},
    }

    check_visit_node(node, expected)


def test_macro_header_node_with_header():
    node = MacroHeaderNode("someid", header=HeaderNode(level=1))

    expected = {
        "_type": "macro.header",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "target_name": "someid",
        "content": [],
        "header": {
            "_type": "header",
            "_parent_info": {},
            "_info": NodeInfo.empty().asdict(),
            "name": None,
            "internal_id": None,
            "level": 1,
            "labels": {},
            "content": [],
        },
    }

    check_visit_node(node, expected)


def test_macro_header_node_parameters():
    node = MacroHeaderNode(target_name="somename")

    expected = {
        "_type": "macro.header",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "target_name": "somename",
        "content": [],
        "header": {},
    }

    check_visit_node(node, expected)


def test_macro_footnote_node_parameters():
    node = MacroFootnoteNode(footnote=FootnoteNode(name="somename"))

    expected = {
        "_type": "macro.footnote",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "footnote": {
            "_type": "footnote",
            "_parent_info": {},
            "_info": NodeInfo.empty().asdict(),
            "name": "somename",
            "public_id": None,
            "internal_id": None,
            "content": [],
        },
    }

    check_visit_node(node, expected)


def test_macro_unicode():
    node = MacroUnicodeNode("1F30B")

    expected = {
        "_type": "macro.unicode",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "1F30B",
    }

    check_visit_node(node, expected)


def test_macro_raw():
    node = MacroRawNode("somevalue")

    expected = {
        "_type": "macro.raw",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "somevalue",
    }

    check_visit_node(node, expected)
