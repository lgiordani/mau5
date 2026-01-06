from mau.nodes.inline import TextNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.buffers.label_buffer import LabelBuffer
from mau.test_helpers import (
    compare_asdict_list,
    generate_context,
)


def test_title_buffer():
    tb = LabelBuffer()

    assert tb.pop() == {}


def test_title_buffer_push_and_pop():
    tb = LabelBuffer()

    test_node = Node(
        data=TextNodeData("Some title"),
        info=NodeInfo(context=generate_context(0, 1, 0, 11)),
    )

    tb.push("title", [test_node])

    children = tb.pop()

    assert list(children.keys()) == ["title"]

    compare_asdict_list(children["title"], [test_node])

    assert tb.pop() == {}


def test_title_buffer_push_multiple_children():
    tb = LabelBuffer()

    test_node_title = Node(
        data=TextNodeData("Some title"),
        info=NodeInfo(context=generate_context(0, 0, 0, 10)),
    )

    test_node_source = Node(
        data=TextNodeData("Some source"),
        info=NodeInfo(context=generate_context(1, 0, 1, 11)),
    )

    tb.push("title", [test_node_title])
    tb.push("source", [test_node_source])

    children = tb.pop()

    assert list(children.keys()) == ["title", "source"]

    compare_asdict_list(children["title"], [test_node_title])
    compare_asdict_list(children["source"], [test_node_source])

    assert tb.pop() == {}


def test_title_buffer_push_twice_the_same_position():
    tb = LabelBuffer()

    test_node_title = Node(
        data=TextNodeData("Some title"),
        info=NodeInfo(context=generate_context(0, 0, 0, 10)),
    )

    test_node_title2 = Node(
        data=TextNodeData("Some title 2"),
        info=NodeInfo(context=generate_context(0, 0, 0, 10)),
    )

    tb.push("title", [test_node_title])
    tb.push("title", [test_node_title2])

    children = tb.pop()

    assert list(children.keys()) == ["title"]

    compare_asdict_list(children["title"], [test_node_title2])

    assert tb.pop() == {}
