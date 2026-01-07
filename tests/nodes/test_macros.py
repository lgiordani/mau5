from functools import partial

from mau.nodes.headers import HeaderNodeData
from mau.nodes.footnotes import FootnoteNodeData
from mau.nodes.macros import (
    MacroClassNodeData,
    MacroFootnoteNodeData,
    MacroHeaderNodeData,
    MacroImageNodeData,
    MacroLinkNodeData,
    MacroNodeData,
)
from mau.test_helpers import check_node_data_with_content


def test_macro_node_data():
    node_data = MacroNodeData("somename")

    assert node_data.type == "macro"
    assert node_data.name == "somename"
    assert node_data.unnamed_args == []
    assert node_data.named_args == {}
    assert node_data.asdict() == {
        "type": "macro",
        "custom": {
            "name": "somename",
            "unnamed_args": [],
            "named_args": {},
        },
    }


def test_macro_node_data_args():
    node_data = MacroNodeData(
        "somename", unnamed_args=["arg1"], named_args={"key1": "value1"}
    )

    assert node_data.type == "macro"
    assert node_data.name == "somename"
    assert node_data.unnamed_args == ["arg1"]
    assert node_data.named_args == {"key1": "value1"}
    assert node_data.asdict() == {
        "type": "macro",
        "custom": {
            "name": "somename",
            "unnamed_args": ["arg1"],
            "named_args": {"key1": "value1"},
        },
    }


def test_macro_class_node_data_without_content():
    node_data = MacroClassNodeData(["class1", "class2"])

    assert node_data.type == "macro.class"
    assert node_data.classes == ["class1", "class2"]
    assert node_data.content == []
    assert node_data.asdict() == {
        "type": "macro.class",
        "custom": {
            "classes": ["class1", "class2"],
            "content": [],
        },
    }


def test_macro_class_node_data_with_content():
    node_data_class = partial(MacroClassNodeData, ["class1", "class2"])
    check_node_data_with_content(node_data_class)


def test_macro_link_node_data_without_content():
    node_data = MacroLinkNodeData("sometarget")

    assert node_data.type == "macro.link"
    assert node_data.target == "sometarget"
    assert node_data.asdict() == {
        "type": "macro.link",
        "custom": {
            "target": "sometarget",
            "content": [],
        },
    }


def test_macro_link_node_data_with_content():
    node_data_class = partial(MacroLinkNodeData, "sometarget")
    check_node_data_with_content(node_data_class)


def test_macro_image_node_data():
    node_data = MacroImageNodeData("someuri")

    assert node_data.type == "macro.image"
    assert node_data.uri == "someuri"
    assert node_data.alt_text is None
    assert node_data.width is None
    assert node_data.height is None

    assert node_data.asdict() == {
        "type": "macro.image",
        "custom": {
            "uri": "someuri",
            "alt_text": None,
            "width": None,
            "height": None,
        },
    }


def test_macro_image_node_data_parameters():
    node_data = MacroImageNodeData("someuri", "alt_text", "width", "height")

    assert node_data.type == "macro.image"
    assert node_data.uri == "someuri"
    assert node_data.alt_text == "alt_text"
    assert node_data.width == "width"
    assert node_data.height == "height"

    assert node_data.asdict() == {
        "type": "macro.image",
        "custom": {
            "uri": "someuri",
            "alt_text": "alt_text",
            "width": "width",
            "height": "height",
        },
    }


def test_macro_header_node_data():
    node_data = MacroHeaderNodeData("someid")

    assert node_data.type == "macro.header"
    assert node_data.target_alias == "someid"
    assert node_data.target_id is None

    assert node_data.asdict() == {
        "type": "macro.header",
        "custom": {
            "target_alias": "someid",
            "target_id": None,
            "content": [],
            "header": None,
        },
    }


def test_macro_header_node_data_with_header():
    node_data = MacroHeaderNodeData("someid", header=HeaderNodeData(level=1))

    assert node_data.type == "macro.header"
    assert node_data.target_alias == "someid"
    assert node_data.target_id is None

    assert node_data.asdict() == {
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
                },
            },
        },
    }


def test_macro_header_node_data_parameters():
    node_data = MacroHeaderNodeData("someid", target_id="targetid")

    assert node_data.type == "macro.header"
    assert node_data.target_alias == "someid"
    assert node_data.target_id == "targetid"

    assert node_data.asdict() == {
        "type": "macro.header",
        "custom": {
            "target_alias": "someid",
            "target_id": "targetid",
            "content": [],
            "header": None,
        },
    }


def test_macro_footnote_node_data_parameters():
    node_data = MacroFootnoteNodeData(footnote=FootnoteNodeData(name="somename"))

    assert node_data.type == "macro.footnote"

    assert node_data.asdict() == {
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
            }
        },
    }
