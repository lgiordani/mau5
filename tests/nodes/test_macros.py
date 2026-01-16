
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
from mau.test_helpers import check_node_with_content
from mau.text_buffer import Context


def test_macro_node():
    node = MacroNode("somename")

    assert node.type == "macro"
    assert node.name == "somename"
    assert node.unnamed_args == []
    assert node.named_args == {}
    assert node.asdict() == {
        "type": "macro",
        "custom": {
            "name": "somename",
            "unnamed_args": [],
            "named_args": {},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_node_args():
    node = MacroNode("somename", unnamed_args=["arg1"], named_args={"key1": "value1"})

    assert node.type == "macro"
    assert node.name == "somename"
    assert node.unnamed_args == ["arg1"]
    assert node.named_args == {"key1": "value1"}
    assert node.asdict() == {
        "type": "macro",
        "custom": {
            "name": "somename",
            "unnamed_args": ["arg1"],
            "named_args": {"key1": "value1"},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_class_node_without_content():
    node = MacroClassNode(["class1", "class2"])

    assert node.type == "macro.class"
    assert node.classes == ["class1", "class2"]
    assert node.content == []
    assert node.asdict() == {
        "type": "macro.class",
        "custom": {
            "classes": ["class1", "class2"],
            "content": [],
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_class_node_with_content():
    node = MacroClassNode(["class1", "class2"])
    check_node_with_content(node)


def test_macro_link_node_without_content():
    node = MacroLinkNode("sometarget")

    assert node.type == "macro.link"
    assert node.target == "sometarget"
    assert node.asdict() == {
        "type": "macro.link",
        "custom": {
            "target": "sometarget",
            "content": [],
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_link_node_with_content():
    node = MacroLinkNode("sometarget")
    check_node_with_content(node)


def test_macro_image_node():
    node = MacroImageNode("someuri")

    assert node.type == "macro.image"
    assert node.uri == "someuri"
    assert node.alt_text is None
    assert node.width is None
    assert node.height is None

    assert node.asdict() == {
        "type": "macro.image",
        "custom": {
            "uri": "someuri",
            "alt_text": None,
            "width": None,
            "height": None,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_image_node_parameters():
    node = MacroImageNode("someuri", "alt_text", "width", "height")

    assert node.type == "macro.image"
    assert node.uri == "someuri"
    assert node.alt_text == "alt_text"
    assert node.width == "width"
    assert node.height == "height"

    assert node.asdict() == {
        "type": "macro.image",
        "custom": {
            "uri": "someuri",
            "alt_text": "alt_text",
            "width": "width",
            "height": "height",
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_header_node():
    node = MacroHeaderNode("someid")

    assert node.type == "macro.header"
    assert node.target_alias == "someid"
    assert node.target_id is None

    assert node.asdict() == {
        "type": "macro.header",
        "custom": {
            "target_alias": "someid",
            "target_id": None,
            "content": [],
            "header": None,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_header_node_with_header():
    node = MacroHeaderNode("someid", header=HeaderNode(level=1))

    assert node.type == "macro.header"
    assert node.target_alias == "someid"
    assert node.target_id is None

    assert node.asdict() == {
        "type": "macro.header",
        "custom": {
            "target_alias": "someid",
            "target_id": None,
            "content": [],
            "header": {
                "type": "header",
                "custom": {
                    "alias": None,
                    "internal_id": None,
                    "level": 1,
                    "labels": {},
                    "content": [],
                },
                "info": {
                    "context": Context.empty().asdict(),
                    "unnamed_args": [],
                    "named_args": {},
                    "tags": [],
                    "subtype": None,
                },
            },
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_header_node_parameters():
    node = MacroHeaderNode("someid", target_id="targetid")

    assert node.type == "macro.header"
    assert node.target_alias == "someid"
    assert node.target_id == "targetid"

    assert node.asdict() == {
        "type": "macro.header",
        "custom": {
            "target_alias": "someid",
            "target_id": "targetid",
            "content": [],
            "header": None,
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_macro_footnote_node_parameters():
    node = MacroFootnoteNode(footnote=FootnoteNode(name="somename"))

    assert node.type == "macro.footnote"

    assert node.asdict() == {
        "type": "macro.footnote",
        "custom": {
            "footnote": {
                "type": "footnote",
                "custom": {
                    "name": "somename",
                    "public_id": None,
                    "private_id": None,
                    "content": [],
                },
                "info": {
                    "context": Context.empty().asdict(),
                    "unnamed_args": [],
                    "named_args": {},
                    "tags": [],
                    "subtype": None,
                },
            }
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }
