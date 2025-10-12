from mau.nodes.macros import (
    MacroClassNodeContent,
    MacroFootnoteNodeContent,
    MacroHeaderNodeContent,
    MacroImageNodeContent,
    MacroLinkNodeContent,
    MacroNodeContent,
)


def test_macro_node_content():
    node_content = MacroNodeContent("somename")

    assert node_content.type == "macro"
    assert node_content.name == "somename"
    assert node_content.unnamed_args == []
    assert node_content.named_args == {}

    assert node_content.asdict() == {
        "type": "macro",
        "name": "somename",
        "unnamed_args": [],
        "named_args": {},
    }


def test_macro_node_content_args():
    node_content = MacroNodeContent(
        "somename", unnamed_args=["arg1"], named_args={"key1": "value1"}
    )

    assert node_content.type == "macro"
    assert node_content.name == "somename"
    assert node_content.unnamed_args == ["arg1"]
    assert node_content.named_args == {"key1": "value1"}

    assert node_content.asdict() == {
        "type": "macro",
        "name": "somename",
        "unnamed_args": ["arg1"],
        "named_args": {"key1": "value1"},
    }


def test_macro_class_node_content():
    node_content = MacroClassNodeContent(["class1", "class2"])

    assert node_content.type == "macro.class"
    assert list(node_content.allowed_keys.keys()) == ["text"]
    assert node_content.classes == ["class1", "class2"]

    assert node_content.asdict() == {
        "type": "macro.class",
        "classes": ["class1", "class2"],
    }


def test_macro_link_node_content():
    node_content = MacroLinkNodeContent("sometarget")

    assert node_content.type == "macro.link"
    assert list(node_content.allowed_keys.keys()) == ["text"]
    assert node_content.value == "sometarget"

    assert node_content.asdict() == {
        "type": "macro.link",
        "target": "sometarget",
    }


def test_macro_image_node_content():
    node_content = MacroImageNodeContent("someuri")

    assert node_content.type == "macro.image"
    assert node_content.uri == "someuri"
    assert node_content.alt_text is None
    assert node_content.width is None
    assert node_content.height is None

    assert node_content.asdict() == {
        "type": "macro.image",
        "uri": "someuri",
        "alt_text": None,
        "width": None,
        "height": None,
    }


def test_macro_image_node_content_parameters():
    node_content = MacroImageNodeContent("someuri", "alt_text", "width", "height")

    assert node_content.type == "macro.image"
    assert node_content.uri == "someuri"
    assert node_content.alt_text == "alt_text"
    assert node_content.width == "width"
    assert node_content.height == "height"

    assert node_content.asdict() == {
        "type": "macro.image",
        "uri": "someuri",
        "alt_text": "alt_text",
        "width": "width",
        "height": "height",
    }


def test_macro_header_node_content():
    node_content = MacroHeaderNodeContent("someid")

    assert node_content.type == "macro.header"
    assert node_content.value == "someid"

    assert node_content.asdict() == {
        "type": "macro.header",
        "id": "someid",
    }


def test_macro_header_node_content_parameters():
    node_content = MacroHeaderNodeContent("someid")

    assert node_content.type == "macro.header"
    assert node_content.value == "someid"

    assert node_content.asdict() == {
        "type": "macro.header",
        "id": "someid",
    }


def test_macro_footnote_node_content_parameters():
    node_content = MacroFootnoteNodeContent("somename")

    assert node_content.type == "macro.footnote"
    assert node_content.name == "somename"
    assert node_content.public_id is None
    assert node_content.private_id is None

    assert node_content.asdict() == {
        "type": "macro.footnote",
        "name": "somename",
        "public_id": None,
        "private_id": None,
    }
