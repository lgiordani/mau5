# from mau.lexers.document_lexer import DocumentLexer
# from mau.parsers.buffers.control_buffer import (
#     ControlComparisons,
# )
# from mau.parsers.document_parser import DocumentParser
# from mau.test_helpers import (
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )
# 
# init_parser = init_parser_factory(DocumentLexer, DocumentParser)
# 
# runner = parser_runner_factory(DocumentLexer, DocumentParser)
# 
# 
# def test_control():
#     source = """
#     @if answer==42
#     """
# 
#     parser = runner(source)
# 
#     control = parser.control_buffer.pop()
# 
#     assert control.operator == "if"
#     assert control.variable == "answer"
#     assert control.comparison == ControlComparisons.EQUAL_EQUAL
#     assert control.value == "42"
#     assert control.context == generate_context(1, 0, 1, 14)
# 
# 
# def test_control_with_spaces():
#     source = """
#     @if    answer  ==   42
#     """
# 
#     parser = runner(source)
# 
#     control = parser.control_buffer.pop()
# 
#     assert control.operator == "if"
#     assert control.variable == "answer"
#     assert control.comparison == ControlComparisons.EQUAL_EQUAL
#     assert control.value == "42"
#     assert control.context == generate_context(1, 0, 1, 22)
# 
# 
# def test_control_boolean_is_a_string():
#     source = """
#     @if answer==true
#     """
# 
#     parser = runner(source)
# 
#     control = parser.control_buffer.pop()
# 
#     assert control.operator == "if"
#     assert control.variable == "answer"
#     assert control.comparison == ControlComparisons.EQUAL_EQUAL
#     assert control.value == "true"
#     assert control.context == generate_context(1, 0, 1, 16)
