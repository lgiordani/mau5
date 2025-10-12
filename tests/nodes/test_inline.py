from mau.nodes.inline import (
    RawNodeContent,
    StyleNodeContent,
    TextNodeContent,
    VerbatimNodeContent,
    WordNodeContent,
)


def test_word_node():
    node_content = WordNodeContent("somevalue")

    assert node_content.type == "word"
    assert node_content.value == "somevalue"
    assert node_content.asdict() == {"type": "word", "value": "somevalue"}


def test_text_node():
    node_content = TextNodeContent("somevalue")

    assert node_content.type == "text"
    assert node_content.value == "somevalue"
    assert node_content.asdict() == {"type": "text", "value": "somevalue"}


def test_raw_node():
    node_content = RawNodeContent("somevalue")

    assert node_content.type == "raw"
    assert node_content.value == "somevalue"
    assert node_content.asdict() == {"type": "raw", "value": "somevalue"}


def test_verbatim_node():
    node_content = VerbatimNodeContent("somevalue")

    assert node_content.type == "verbatim"
    assert node_content.value == "somevalue"
    assert node_content.asdict() == {"type": "verbatim", "value": "somevalue"}


def test_style_node():
    node_content = StyleNodeContent("mystyle")

    assert node_content.type == "style"
    assert list(node_content.allowed_keys.keys()) == ["content"]
    assert node_content.value == "mystyle"
    assert node_content.asdict() == {"type": "style", "value": "mystyle"}
