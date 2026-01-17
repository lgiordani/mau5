# from mau.environment.environment import Environment
# from mau.nodes.node import NodeInfo
# from mau.nodes.block import BlockNode
# from mau.nodes.inline import TextNode
# from mau.nodes.paragraph import ParagraphNode
# from mau.visitors.jinja_visitor import JinjaVisitor
# from mau.test_helpers import generate_context


# def test_page_paragraph_node():
#     templates = {
#         # "text.j2": "{{ value }}",
#         # "sentence.j2": "{{ content }}",
#         # "paragraph.j2": (
#         #     "{{ content }} - {{ title }} - {{ args | join(',') }} - "
#         #     "{% for key, value in kwargs|items %}{{ key }}:{{ value }}{% endfor %} - "
#         #     "{{ tags | join(',') }}"
#         # ),
#     }

#     environment = Environment()
#     environment.dupdate(templates, "mau.visitor.templates.custom")
#     visitor = JinjaVisitor(environment)

#     unnamed_args = ["arg1", "arg2"]
#     named_args = {"key1": "value1"}
#     tags = ["tag1", "tag2"]

#     node = ParagraphNode(
#         labels={"title": [TextNode("sometitle")]},
#         content=[TextNode("Just some text")],
#         info=NodeInfo(
#             context=generate_context(0, 0, 0, 0),
#             unnamed_args=unnamed_args,
#             named_args=named_args,
#             tags=tags,
#             subtype="subtype1",
#         ),
#     )

#     result = visitor.visit(node)

#     assert result == "Just some text - sometitle - arg1,arg2 - key1:value1 - tag1,tag2"


# def test_page_paragraph_node_inside_block():
#     templates = {
#         "block.j2": "{{ content }}",
#         "text.j2": "{{ value }}",
#         "paragraph.j2": (
#             "{{ content }} - {{ args | join(',') }} - "
#             "{% for key, value in kwargs|items %}{{ key }}:{{ value }}{% endfor %} - "
#             "{{ tags | join(',') }}"
#         ),
#     }

#     environment = Environment()
#     environment.update(templates, "mau.visitor.custom_templates")
#     visitor = JinjaVisitor(environment)

#     node = BlockNode(
#         subtype="section",
#         children=[
#             ParagraphNode(
#                 children=[TextNode("Just some text")],
#                 args=["arg1", "arg2"],
#                 kwargs={"key1": "value1"},
#                 tags=["tag1", "tag2"],
#             ),
#         ],
#     )

#     result = visitor.visit(node)

#     assert result == "Just some text - arg1,arg2 - key1:value1 - tag1,tag2"
