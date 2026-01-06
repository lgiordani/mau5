# import pytest

# from mau.nodes.block import BlockNodeData
# from mau.nodes.commands import BlockGroupNodeData
# from mau.nodes.node import Node, NodeInfo
# from mau.parsers.base_parser import MauParserException
# from mau.parsers.managers.block_group_manager import (
#     BlockGroupManager,
# )
# from mau.test_helpers import (
#     compare_asdict_list,
#     compare_asdict_object,
#     generate_context,
# )


# def test_block_group_manager():
#     bgm = BlockGroupManager()

#     block_node1 = BlockNodeData()
#     block_node2 = BlockNodeData()
#     block_node3 = BlockNodeData()

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

#     block_node1 = BlockNodeData()
#     block_node2 = BlockNodeData()

#     bgm.add_block("group1", "position1", block_node1)

#     with pytest.raises(ValueError):
#         bgm.add_block("group1", "position1", block_node2)


# def test_block_group_manager_add_group_node():
#     bgm = BlockGroupManager()

#     group_node = BlockGroupNodeData("somename")

#     bgm.add_group_node(group_node)

#     assert bgm.group_nodes == [group_node]


# def test_block_group_manager_process():
#     bgm = BlockGroupManager()

#     block_data1 = BlockNodeData()
#     block_node1 = Node(data=block_data1)
#     block_data2 = BlockNodeData()
#     block_node2 = Node(data=block_data2)
#     block_data3 = BlockNodeData()
#     block_node3 = Node(data=block_data3)

#     bgm.add_block("group1", "position1", block_data1)
#     bgm.add_block("group1", "position2", block_data2)
#     bgm.add_block("group2", "position1", block_data3)

#     group_node = BlockGroupNodeData("group1")

#     bgm.add_group_node(group_node)

#     expected_node = BlockGroupNodeData(
#         "group1", groups={"position1": block_node1, "position2": block_node2}
#     )

#     bgm.process()

#     compare_asdict_object(group_node, expected_node)


# def test_block_group_manager_process_group_does_not_exist():
#     bgm = BlockGroupManager()

#     group_node = Node(
#         data=BlockGroupNodeData("group1"),
#         info=NodeInfo(context=generate_context(4, 2, 4, 2)),
#     )
#     bgm.add_group_node(group_node)

#     with pytest.raises(MauParserException) as exc:
#         bgm.process()

#     assert exc.value.message == "The group named group1 does not exist."
#     assert exc.value.context == generate_context(4, 2, 4, 2)
