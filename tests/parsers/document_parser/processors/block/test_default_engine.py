from unittest.mock import patch

import pytest

from mau.nodes.headers import HeaderNodeContent
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.block import BlockNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


# @patch("mau.parsers.document_parser.parser.header_anchor")
# def test_block_default_engine_adds_headers_to_global_toc(mock_header_anchor):
#     mock_header_anchor.return_value = "XXYY"

#     source = """
#     = Global header

#     [*subtype1]
#     ----
#     = Block header
#     ----
#     """

#     parser = runner(source)

#     compare_nodes(
#         parser.nodes,
#         [
#             Node(
#                 content=HeaderNodeContent(1, "XXYY"),
#                 info=NodeInfo(context=generate_context(1, 0)),
#                 children={
#                     "text": [
#                         Node(
#                             content=SentenceNodeContent(),
#                             info=NodeInfo(context=generate_context(1, 2)),
#                             children={
#                                 "content": [
#                                     Node(
#                                         content=TextNodeContent("Global header"),
#                                         info=NodeInfo(context=generate_context(1, 2)),
#                                     )
#                                 ]
#                             },
#                         )
#                     ],
#                 },
#             ),
#             Node(
#                 content=BlockNodeContent(
#                     classes=[],
#                     engine=None,
#                     preprocessor=None,
#                 ),
#                 info=NodeInfo(context=generate_context(4, 0), subtype="subtype1"),
#                 children={
#                     "content": [
#                         Node(
#                             content=HeaderNodeContent(1, "XXYY"),
#                             info=NodeInfo(context=generate_context(5, 0)),
#                             children={
#                                 "text": [
#                                     Node(
#                                         content=SentenceNodeContent(),
#                                         info=NodeInfo(context=generate_context(5, 2)),
#                                         children={
#                                             "content": [
#                                                 Node(
#                                                     content=TextNodeContent(
#                                                         "Block header"
#                                                     ),
#                                                     info=NodeInfo(
#                                                         context=generate_context(5, 2)
#                                                     ),
#                                                 )
#                                             ]
#                                         },
#                                     )
#                                 ],
#                             },
#                         ),
#                     ]
#                 },
#             ),
#         ],
#     )

# assert par.nodes == [
#     HeaderNode(
#         value=SentenceNode(children=[TextNode("Global header")]),
#         level="1",
#         anchor="XXYY",
#     ),
#     BlockNode(
#         subtype="someblock",
#         children=[
#             HeaderNode(
#                 value=SentenceNode(children=[TextNode("Block header")]),
#                 level="1",
#                 anchor="XXYY",
#             ),
#         ],
#         secondary_children=[],
#         classes=[],
#         title=None,
#         engine=None,
#         preprocessor="none",
#         args=[],
#         kwargs={},
#     ),
# ]

# assert par.toc_manager.headers == [
#     HeaderNode(
#         value=SentenceNode(children=[TextNode("Global header")]),
#         level="1",
#         anchor="XXYY",
#     ),
#     HeaderNode(
#         value=SentenceNode(children=[TextNode("Block header")]),
#         level="1",
#         anchor="XXYY",
#     ),
# ]
