# import pytest

# from mau.lexers.document_lexer.lexer import DocumentLexer
# from mau.nodes.block import BlockGroupNodeContent, BlockNodeContent
# from mau.nodes.inline import TextNodeContent
# from mau.nodes.node import Node, NodeInfo
# from mau.nodes.paragraph import ParagraphNodeContent
# from mau.parsers.base_parser.parser import MauParserException
# from mau.parsers.document_parser.parser import DocumentParser
# from mau.test_helpers import (
#     compare_nodes,
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_group_engine():
#     source = """
#     [group1, position1, engine=group]
#     ----
#     Some text 1.
#     ----

#     [group1, position2, engine=group]
#     ----
#     Some text 2.
#     ----

#     ::blockgroup:group1
#     """

#     parser = runner(source)

#     block_node1 = Node(
#         content=BlockNodeContent(engine="group"),
#         info=NodeInfo(context=generate_context(2, 0, 4, 4)),
#         children={
#             "content": [
#                 Node(
#                     content=ParagraphNodeContent(),
#                     info=NodeInfo(context=generate_context(3, 0, 3, 12)),
#                     children={
#                         "content": [
#                             Node(
#                                 content=TextNodeContent("Some text 1."),
#                                 info=NodeInfo(context=generate_context(3, 0, 3, 12)),
#                             )
#                         ]
#                     },
#                 )
#             ],
#         },
#     )

#     block_node2 = Node(
#         content=BlockNodeContent(engine="group"),
#         info=NodeInfo(context=generate_context(7, 0, 9, 4)),
#         children={
#             "content": [
#                 Node(
#                     content=ParagraphNodeContent(),
#                     info=NodeInfo(context=generate_context(8, 0, 8, 12)),
#                     children={
#                         "content": [
#                             Node(
#                                 content=TextNodeContent("Some text 2."),
#                                 info=NodeInfo(context=generate_context(8, 0, 8, 12)),
#                             )
#                         ]
#                     },
#                 )
#             ],
#         },
#     )

#     compare_nodes(
#         parser.nodes,
#         [
#             Node(
#                 content=BlockGroupNodeContent("group1"),
#                 info=NodeInfo(context=generate_context(11, 0, 11, 12)),
#                 children={"position1": [block_node1], "position2": [block_node2]},
#             )
#         ],
#     )


# def test_group_engine_wrong_group():
#     source = """
#     [group1, position1, engine=group]
#     ----
#     Some text 1.
#     ----

#     [group1, position2, engine=group]
#     ----
#     Some text 2.
#     ----

#     ::blockgroup:group2
#     """

#     with pytest.raises(MauParserException) as exc:
#         runner(source)

#     assert exc.value.context == generate_context(11, 0, 11, 12)
