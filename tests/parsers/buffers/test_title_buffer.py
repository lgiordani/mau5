from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser.buffers.title_buffer import TitleBuffer
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
    tb = TitleBuffer()

    assert tb.pop() == []


def test_title_buffer_push_and_pop():
    tb = TitleBuffer()
    test_title = "Some title"

    tb.push(test_title, generate_context(42, 24), Environment())

    compare_nodes(
        tb.pop(),
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(42, 24)),
            )
        ],
    )

    assert tb.pop() == []


def test_title_buffer_push_twice():
    tb = TitleBuffer()
    test_title1 = "Some title 1"
    test_title2 = "Some title 2"

    tb.push(test_title1, generate_context(42, 24), Environment())
    tb.push(test_title2, generate_context(42, 24), Environment())

    compare_nodes(
        tb.pop(),
        [
            Node(
                content=TextNodeContent("Some title 2"),
                info=NodeInfo(context=generate_context(42, 24)),
            )
        ],
    )

    assert tb.pop() == []
