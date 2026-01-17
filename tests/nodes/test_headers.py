# from mau.visitors.base_visitor import BaseVisitor
# from mau.nodes.node import Node
# from mau.nodes.headers import HeaderNode
# from mau.test_helpers import check_node_with_content
# from mau.text_buffer import Context
# from mau.visitors.base_visitor import BaseVisitor


# def test_header_node_without_content():
#     node = HeaderNode(
#         level=42,
#         internal_id="some_internal_id",
#         alias="some_alias",
#     )

#     assert node.type == "header"
#     assert node.level == 42
#     assert node.internal_id == "some_internal_id"
#     assert node.alias == "some_alias"


# def test_header_node_with_content():
#     content = [Node(), Node()]

#     node = HeaderNode(
#         level=42,
#         internal_id="some_internal_id",
#         alias="some_alias",
#         content=content,
#     )

#     assert node.content == content
