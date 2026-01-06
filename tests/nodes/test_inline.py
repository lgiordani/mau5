from functools import partial

from mau.nodes.inline import (
    RawNodeData,
    StyleNodeData,
    TextNodeData,
    VerbatimNodeData,
    WordNodeData,
)
from mau.test_helpers import check_node_data_with_content


def test_word_node_data():
    node_data = WordNodeData("somevalue")

    assert node_data.type == "word"
    assert node_data.value == "somevalue"
    assert node_data.asdict() == {
        "type": "word",
        "custom": {
            "value": "somevalue",
        },
    }


def test_text_node_data():
    node_data = TextNodeData("somevalue")

    assert node_data.type == "text"
    assert node_data.value == "somevalue"
    assert node_data.asdict() == {
        "type": "text",
        "custom": {
            "value": "somevalue",
        },
    }


def test_raw_node_data():
    node_data = RawNodeData("somevalue")

    assert node_data.type == "raw"
    assert node_data.value == "somevalue"
    assert node_data.asdict() == {
        "type": "raw",
        "custom": {
            "value": "somevalue",
        },
    }


def test_verbatim_node_data():
    node_data = VerbatimNodeData("somevalue")

    assert node_data.type == "verbatim"
    assert node_data.value == "somevalue"
    assert node_data.asdict() == {
        "type": "verbatim",
        "custom": {"value": "somevalue"},
    }


def test_style_node_data_without_content():
    node_data = StyleNodeData("mystyle")

    assert node_data.type == "style"
    assert node_data.style == "mystyle"
    assert node_data.asdict() == {
        "type": "style",
        "custom": {
            "style": "mystyle",
            "content": [],
        },
    }


def test_style_node_data_with_content():
    node_data_class = partial(StyleNodeData, "mystyle")
    check_node_data_with_content(node_data_class)
