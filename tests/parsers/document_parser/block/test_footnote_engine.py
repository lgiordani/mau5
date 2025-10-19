from unittest.mock import patch

from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.footnotes import FootnotesItemNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphNodeContent
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_node,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


@patch("mau.parsers.managers.footnotes_manager.default_footnote_unique_id")
def test_footnote_engine_records_footnote_blocks(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    source = """
    [somename, engine=footnote]
    ----
    Some text.
    ----
    """

    parser = runner(source)

    footnote_content_node = parser.footnotes_manager.data["somename"]

    compare_node(
        footnote_content_node,
        Node(
            content=FootnotesItemNodeContent("somename"),
            info=NodeInfo(context=generate_context(2, 0, 4, 4)),
            children={
                "content": [
                    Node(
                        content=ParagraphNodeContent(),
                        info=NodeInfo(context=generate_context(3, 0, 3, 10)),
                        children={
                            "content": [
                                Node(
                                    content=TextNodeContent("Some text."),
                                    info=NodeInfo(
                                        context=generate_context(3, 0, 3, 10)
                                    ),
                                )
                            ]
                        },
                    )
                ],
            },
        ),
    )
