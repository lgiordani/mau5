from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser.parser import DocumentParser
from mau.parsers.document_parser.processors.child import child_processor
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_child():
    source = ". Some title"

    parser: DocumentParser = init_parser(source)
    child_processor(parser)

    compare_nodes(
        parser.children_buffer.pop()["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )


def test_child_with_spaces():
    source = ".   Some title"

    parser: DocumentParser = init_parser(source)
    child_processor(parser)

    compare_nodes(
        parser.children_buffer.pop()["title"],
        [
            Node(
                content=TextNodeContent("Some title"),
                info=NodeInfo(context=generate_context(0, 0)),
            )
        ],
    )
