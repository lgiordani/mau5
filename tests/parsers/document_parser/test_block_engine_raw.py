# from mau.lexers.document_lexer import DocumentLexer
# from mau.nodes.block import BlockNode
# from mau.nodes.inline import RawNode
# from mau.parsers.document_parser import DocumentParser

# from mau.test_helpers import init_parser_factory, parser_runner_factory

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


# def test_block_raw_engine():
#     source = """
#     [*block, engine=raw]
#     ----
#     Raw content
#     on multiple lines
#     ----
#     Secondary content
#     on multiple lines as well
#     """

#     assert runner(source).nodes == [
#         BlockNode(
#             subtype="block",
#             children=[
#                 RawNode("Raw content"),
#                 RawNode("on multiple lines"),
#             ],
#             secondary_children=[
#                 RawNode("Secondary content"),
#                 RawNode("on multiple lines as well"),
#             ],
#             classes=[],
#             title=None,
#             engine="raw",
#             preprocessor="none",
#             args=[],
#             kwargs={},
#         )
#     ]
