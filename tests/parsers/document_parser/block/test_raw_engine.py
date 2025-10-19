from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import RawNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_raw_engine():
    source = """
    [engine=raw]
    ----
    Raw content
    on multiple lines
    ----
    """

    parser = runner(source)

    compare_nodes(
        parser.nodes,
        [
            Node(
                content=BlockNodeContent(
                    classes=[],
                    engine="raw",
                    preprocessor=None,
                ),
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
                children={
                    "content": [
                        Node(
                            content=RawNodeContent("Raw content"),
                            info=NodeInfo(context=generate_context(3, 0, 3, 11)),
                        ),
                        Node(
                            content=RawNodeContent("on multiple lines"),
                            info=NodeInfo(context=generate_context(4, 0, 4, 17)),
                        ),
                    ]
                },
            ),
        ],
    )
