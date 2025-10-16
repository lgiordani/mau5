# import pytest

# from mau.lexers.document_lexer.lexer import DocumentLexer
# from mau.nodes.block import BlockGroupNodeContent, BlockNodeContent
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.base_parser.parser import MauParserException
# from mau.parsers.document_parser.managers.block_group_manager import (
#     BlockGroupManager,
# )
# from mau.parsers.document_parser.parser import DocumentParser
# from mau.test_helpers import (
#     compare_node,
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_block_group_manager():
#     bgm = BlockGroupManager()

#     block_node1 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(1, 2)),
#     )

#     block_node2 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(3, 4)),
#     )

#     block_node3 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(5, 6)),
#     )

#     bgm.add_block("group1", "position1", block_node1)
#     bgm.add_block("group1", "position2", block_node2)
#     bgm.add_block("group2", "position1", block_node3)

#     assert bgm.groups == {
#         "group1": {
#             "position1": block_node1,
#             "position2": block_node2,
#         },
#         "group2": {
#             "position1": block_node3,
#         },
#     }


# def test_block_group_manager_same_position():
#     bgm = BlockGroupManager()

#     block_node1 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(1, 2)),
#     )

#     block_node2 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(3, 4)),
#     )

#     bgm.add_block("group1", "position1", block_node1)

#     with pytest.raises(MauParserException) as exc:
#         bgm.add_block("group1", "position1", block_node2)

#     assert exc.value.context == generate_context(3, 4)


# def test_block_group_manager_create_group_node():
#     bgm = BlockGroupManager()

#     block_node1 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(1, 2)),
#     )

#     block_node2 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(3, 4)),
#     )

#     block_node3 = Node(
#         content=BlockNodeContent(),
#         info=NodeInfo(generate_context(5, 6)),
#     )

#     bgm.add_block("group1", "position1", block_node1)
#     bgm.add_block("group1", "position2", block_node2)
#     bgm.add_block("group2", "position1", block_node3)

#     group_node = bgm.create_group_node("group1", context=generate_context(4, 2))

#     expected_node = Node(
#         content=BlockGroupNodeContent("group1"),
#         info=NodeInfo(context=generate_context(4, 2)),
#         children={"position1": [block_node1], "position2": [block_node2]},
#     )

#     compare_node(group_node, expected_node)


# def test_block_group_manager_create_group_node_group_does_not_exist():
#     bgm = BlockGroupManager()

#     with pytest.raises(MauParserException) as exc:
#         bgm.create_group_node("group1", context=generate_context(4, 2))

#     assert exc.value.message == "The group named group1 does not exist."
#     assert exc.value.context == generate_context(4, 2)
