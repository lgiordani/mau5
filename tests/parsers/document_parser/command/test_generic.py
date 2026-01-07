# import pytest

# from mau.lexers.document_lexer import DocumentLexer
# from mau.parsers.base_parser import MauParserException
# from mau.parsers.document_parser import DocumentParser
# from mau.test_helpers import (
#     compare_asdict_list,
#     generate_context,
#     init_parser_factory,
#     parser_runner_factory,
# )

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_command_boxed_and_inline_arguments_are_forbidden():
#     source = """
#     [arg1, #tag1, *subtype1, key1=value1]
#     ::cmd:arg2
#     """

#     with pytest.raises(MauParserException) as exc:
#         runner(source)

#     assert (
#         exc.value.message
#         == "Syntax error. You cannot specify both boxed and inline arguments."
#     )
#     assert exc.value.context == generate_context(2, 0, 2, 5)


# def test_command_colon_after_command_requires_arguments():
#     source = """
#     ::cmd:
#     """

#     with pytest.raises(MauParserException) as exc:
#         runner(source)

#     assert (
#         exc.value.message
#         == "Syntax error. If you use the colon after cmd you need to specify arguments."
#     )
#     assert exc.value.context == generate_context(1, 0, 1, 5)


# def test_command_control():
#     source = """
#     :answer:44

#     @if answer==42
#     [arg1, arg2]
#     . Some title
#     ::cmd
#     """

#     parser = runner(source)

#     compare_asdict_list(parser.nodes, [])

#     assert parser.arguments_buffer.arguments is None
#     assert parser.label_buffer.labels == {}
#     assert parser.control_buffer.control is None
