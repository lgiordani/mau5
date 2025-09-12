
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_command_toc():
#     source = """
#     ::toc:
#     """

#     parser = runner(source)

#     compare_nodes(
#         parser.toc_manager._toc_nodes,
#         [Node(content=TocNodeContent(), children={})],
#     )


# def test_command_toc():
#     source = """
#     [*subtype1, arg1, arg2, #tag1, key1=value1, key2=value2]
#     ::toc:
#     """

#     assert runner(source).nodes == [
#         TocNode(
#             [],
#             subtype="subtype1",
#             args=["arg1", "arg2"],
#             kwargs={"key1": "value1", "key2": "value2"},
#             tags=["tag1"],
#         ),
#     ]


# def test_toc():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     = Header 1
#     == Header 1.1
#     = Header 2

#     ::toc:
#     """

#     parser = runner(source, environment)

#     assert parser.output == {
#         "content": ContainerNode(
#             children=[
#                 HeaderNode(
#                     value=SentenceNode(children=[TextNode("Header 1")]),
#                     level="1",
#                     anchor="Header 1-XXXXXX",
#                 ),
#                 HeaderNode(
#                     value=SentenceNode(children=[TextNode("Header 1.1")]),
#                     level="2",
#                     anchor="Header 1.1-XXXXXX",
#                 ),
#                 HeaderNode(
#                     value=SentenceNode(children=[TextNode("Header 2")]),
#                     level="1",
#                     anchor="Header 2-XXXXXX",
#                 ),
#                 TocNode(
#                     children=[
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             anchor="Header 1-XXXXXX",
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(
#                                         children=[TextNode("Header 1.1")]
#                                     ),
#                                     anchor="Header 1.1-XXXXXX",
#                                     children=[],
#                                 ),
#                             ],
#                         ),
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             anchor="Header 2-XXXXXX",
#                             children=[],
#                         ),
#                     ]
#                 ),
#             ]
#         ),
#         "toc": ContainerNode(
#             children=[
#                 TocNode(
#                     children=[
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             anchor="Header 1-XXXXXX",
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(
#                                         children=[TextNode("Header 1.1")]
#                                     ),
#                                     anchor="Header 1.1-XXXXXX",
#                                     children=[],
#                                 ),
#                             ],
#                         ),
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             anchor="Header 2-XXXXXX",
#                             children=[],
#                         ),
#                     ]
#                 )
#             ]
#         ),
#     }

#     toc_node = parser.output["toc"].children[0]

#     assert toc_node.parent == parser.output["toc"]


# def test_toc_inside_block():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: f"{text}-XXXXXX"
#     )

#     source = """
#     ----
#     = Header 1
#     == Header 1.1
#     = Header 2

#     ::toc:
#     ----
#     """

#     parser = runner(source, environment)

#     assert parser.output == {
#         "content": ContainerNode(
#             children=[
#                 BlockNode(
#                     children=[
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             level="1",
#                             anchor="Header 1-XXXXXX",
#                         ),
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 1.1")]),
#                             level="2",
#                             anchor="Header 1.1-XXXXXX",
#                         ),
#                         HeaderNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             level="1",
#                             anchor="Header 2-XXXXXX",
#                         ),
#                         TocNode(
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(children=[TextNode("Header 1")]),
#                                     anchor="Header 1-XXXXXX",
#                                     children=[
#                                         TocEntryNode(
#                                             value=SentenceNode(
#                                                 children=[TextNode("Header 1.1")]
#                                             ),
#                                             anchor="Header 1.1-XXXXXX",
#                                             children=[],
#                                         ),
#                                     ],
#                                 ),
#                                 TocEntryNode(
#                                     value=SentenceNode(children=[TextNode("Header 2")]),
#                                     anchor="Header 2-XXXXXX",
#                                     children=[],
#                                 ),
#                             ]
#                         ),
#                     ],
#                     preprocessor="none",
#                 )
#             ]
#         ),
#         "toc": ContainerNode(
#             children=[
#                 TocNode(
#                     children=[
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 1")]),
#                             anchor="Header 1-XXXXXX",
#                             children=[
#                                 TocEntryNode(
#                                     value=SentenceNode(
#                                         children=[TextNode("Header 1.1")]
#                                     ),
#                                     anchor="Header 1.1-XXXXXX",
#                                     children=[],
#                                 ),
#                             ],
#                         ),
#                         TocEntryNode(
#                             value=SentenceNode(children=[TextNode("Header 2")]),
#                             anchor="Header 2-XXXXXX",
#                             children=[],
#                         ),
#                     ]
#                 )
#             ]
#         ),
#     }

#     toc_node = parser.output["toc"].children[0]

#     assert toc_node.parent == parser.output["toc"]
