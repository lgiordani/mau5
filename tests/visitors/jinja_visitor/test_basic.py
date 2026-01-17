# import pytest
# from mau.environment.environment import Environment
# from mau.nodes.inline import StyleNode, TextNode, VerbatimNode
# from mau.visitors.base_visitor import MauVisitorException
# from mau.visitors.jinja_visitor import JinjaVisitor, MissingTemplateException
# from mau.test_helpers import TestNode


# EXPECTED_DEFAULT_TEMPLATES = {
#     "document": {
#         "j2": "{{ content }}",
#     },
#     "paragraph": {
#         "j2": "{{ content }}",
#     },
#     "text": {
#         "j2": "{{ value }}",
#     },
# }


# def test_default_values():
#     visitor = JinjaVisitor(Environment())

#     assert visitor.default_templates.asdict() == EXPECTED_DEFAULT_TEMPLATES
#     assert visitor.jinja_environment_options == {}
#     assert visitor.extension == "j2"
#     assert visitor.templates.asdict() == EXPECTED_DEFAULT_TEMPLATES


# def test_custom_templates():
#     templates = {
#         "key": {
#             "j2": "value",
#         },
#     }

#     environment = Environment()
#     environment.dupdate(templates, "mau.visitor.templates.custom")

#     expected_result = {}
#     expected_result.update(EXPECTED_DEFAULT_TEMPLATES)
#     expected_result.update(templates)

#     visitor = JinjaVisitor(environment)

#     assert visitor.templates.asdict() == expected_result


# def test_no_templates():
#     visitor = JinjaVisitor(Environment())
#     visitor.default_templates = Environment()

#     node = TestNode("Just some text.")

#     with pytest.raises(MissingTemplateException):
#         visitor.visit(node)
