from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser.buffers.children_buffer import ChildrenBuffer
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_title_buffer():
    tb = ChildrenBuffer()

    assert tb.pop() == {}


def test_title_buffer_push_and_pop():
    tb = ChildrenBuffer()
    test_title = "Some title"

    tb.push("title", test_title, generate_context(0, 1, 0, 1), Environment())

    children = tb.pop()

    assert list(children.keys()) == ["title"]

    compare_nodes(
        children["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(0, 1, 0, 11)),
            )
        ],
    )

    assert tb.pop() == {}


def test_title_buffer_push_multiple_children():
    tb = ChildrenBuffer()
    test_title = "Some title"
    test_source = "Some source"

    tb.push("title", test_title, generate_context(0, 0, 0, 10), Environment())
    tb.push("source", test_source, generate_context(1, 0, 1, 11), Environment())

    children = tb.pop()

    assert list(children.keys()) == ["title", "source"]

    compare_nodes(
        children["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(0, 0, 0, 10)),
            )
        ],
    )

    compare_nodes(
        children["source"],
        [
            Node(
                content=TextNodeContent("Some source"),
                info=NodeInfo(context=generate_context(1, 0, 1, 11)),
            )
        ],
    )

    assert tb.pop() == {}


def test_title_buffer_push_twice_the_same_position():
    tb = ChildrenBuffer()
    test_title = "Some title"
    test_title2 = "Some title 2"

    tb.push("title", test_title, generate_context(0, 0, 0, 10), Environment())
    tb.push("title", test_title2, generate_context(1, 0, 1, 12), Environment())

    children = tb.pop()

    assert list(children.keys()) == ["title"]

    compare_nodes(
        children["title"],
        [
            Node(
                content=TextNodeContent("Some title 2"),
                info=NodeInfo(context=generate_context(1, 0, 1, 12)),
            )
        ],
    )

    assert tb.pop() == {}
