from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.node import NodeInfo
from mau.nodes.raw import RawLineNode, RawNode
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_nodes_sequence,
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

    compare_nodes_sequence(
        parser.nodes,
        [
            RawNode(
                classes=[],
                content=[
                    RawLineNode(
                        "Raw content",
                        info=NodeInfo(context=generate_context(3, 0, 3, 11)),
                    ),
                    RawLineNode(
                        "on multiple lines",
                        info=NodeInfo(context=generate_context(4, 0, 4, 17)),
                    ),
                ],
                info=NodeInfo(context=generate_context(2, 0, 5, 4)),
            ),
        ],
    )
