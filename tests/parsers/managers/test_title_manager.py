from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser.managers.title_buffer import TitleBuffer
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_title_manager():
    am = TitleBuffer()

    assert am.pop() is None


def test_title_manager_push_and_pop():
    am = TitleBuffer()
    test_title = "Some title"

    am.push(test_title, generate_context(42, 24), Environment())

    compare_node(
        am.pop(),
        Node(
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(42, 24)),
            children={
                "content": [
                    Node(
                        content=TextNodeContent("Some title"),
                        info=NodeInfo(context=generate_context(42, 24)),
                    )
                ]
            },
        ),
    )

    assert am.pop() is None


def test_title_manager_push_twice():
    am = TitleBuffer()
    test_title1 = "Some title 1"
    test_title2 = "Some title 2"

    am.push(test_title1, generate_context(42, 24), Environment())
    am.push(test_title2, generate_context(42, 24), Environment())

    compare_node(
        am.pop(),
        Node(
            content=SentenceNodeContent(),
            info=NodeInfo(context=generate_context(42, 24)),
            children={
                "content": [
                    Node(
                        content=TextNodeContent("Some title 2"),
                        info=NodeInfo(context=generate_context(42, 24)),
                    )
                ]
            },
        ),
    )

    assert am.pop() is None
