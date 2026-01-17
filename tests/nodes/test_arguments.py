# from mau.nodes.arguments import NamedArgumentNode, UnnamedArgumentNode
# from mau.text_buffer import Context


# def test_unnamed_argument_node():
#     node = UnnamedArgumentNode("somevalue")

#     assert node.type == "unnamed_argument"
#     assert node.value == "somevalue"
#     assert node.asdict() == {
#         "type": "unnamed_argument",
#         "custom": {
#             "value": "somevalue",
#         },
#         "info": {
#             "context": Context.empty().asdict(),
#             "unnamed_args": [],
#             "named_args": {},
#             "tags": [],
#             "subtype": None,
#         },
#     }


# def test_named_argument_node():
#     node = NamedArgumentNode("somekey", "somevalue")

#     assert node.type == "named_argument"
#     assert node.key == "somekey"
#     assert node.value == "somevalue"
#     assert node.asdict() == {
#         "custom": {
#             "key": "somekey",
#             "value": "somevalue",
#         },
#         "type": "named_argument",
#         "info": {
#             "context": Context.empty().asdict(),
#             "unnamed_args": [],
#             "named_args": {},
#             "tags": [],
#             "subtype": None,
#         },
#     }
