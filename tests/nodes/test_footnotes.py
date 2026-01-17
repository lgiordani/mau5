# from mau.nodes.footnotes import FootnoteNode
# from mau.text_buffer import Context


# def test_macro_footnote_node_parameters():
#     node = FootnoteNode("somename")

#     assert node.type == "footnote"
#     assert node.name == "somename"
#     assert node.public_id is None
#     assert node.private_id is None

#     assert node.asdict() == {
#         "type": "footnote",
#         "custom": {
#             "name": "somename",
#             "public_id": None,
#             "private_id": None,
#             "content": [],
#         },
#         "info": {
#             "context": Context.empty().asdict(),
#             "unnamed_args": [],
#             "named_args": {},
#             "tags": [],
#             "subtype": None,
#         },
#     }
