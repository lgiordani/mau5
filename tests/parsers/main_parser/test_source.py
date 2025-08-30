# import pytest
# from mau.errors import MauErrorException
# from mau.lexers.main_lexer import MainLexer
# from mau.nodes.inline import RawNode, SentenceNode, TextNode
# from mau.nodes.source import CalloutsEntryNode, SourceNode, SourceLineNode, MarkerNode
# from mau.parsers.main_parser import MainParser

# from mau.test_helpers import init_parser_factory, parser_runner_factory, assert_asdict

# init_parser = init_parser_factory(MainLexer, MainParser)

# runner = parser_runner_factory(MainLexer, MainParser)


# def test_source_empty_block():
#     source = """
#     [*source]
#     ----
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(subtype=None, code=[]),
#         ],
#     )


# def test_source_language():
#     source = """
#     [*source, python]
#     ----
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(code=[], language="python"),
#         ],
#     )


# def test_source_contains_mau():
#     source = """
#     [*source]
#     ----
#     // A comment
#     @@@@
#     A block
#     @@@@
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("// A comment")),
#                     SourceLineNode(number=2, value=RawNode("@@@@")),
#                     SourceLineNode(number=3, value=RawNode("A block")),
#                     SourceLineNode(number=4, value=RawNode("@@@@")),
#                 ],
#             ),
#         ],
#     )


# def test_source_removes_escape_from_directive_like_text():
#     source = r"""
#     [*source]
#     ----
#     \::#looks like a directive
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 code=[
#                     SourceLineNode(
#                         number=1, value=RawNode("::#looks like a directive")
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_with_code():
#     source = """
#     [*source]
#     ----
#     import os

#     print(os.environ["HOME"])
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("import os")),
#                     SourceLineNode(number=2, value=RawNode("")),
#                     SourceLineNode(
#                         number=3, value=RawNode('print(os.environ["HOME"])')
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_explicit_engine():
#     source = """
#     [*myblock, engine=source, language=somelang]
#     ----
#     import os

#     print(os.environ["HOME"])
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 subtype="myblock",
#                 language="somelang",
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("import os")),
#                     SourceLineNode(number=2, value=RawNode("")),
#                     SourceLineNode(
#                         number=3, value=RawNode('print(os.environ["HOME"])')
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_with_title():
#     source = """
#     . Title
#     [*source, somelang]
#     ----
#     import os

#     print(os.environ["HOME"])
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("import os")),
#                     SourceLineNode(number=2, value=RawNode("")),
#                     SourceLineNode(
#                         number=3, value=RawNode('print(os.environ["HOME"])')
#                     ),
#                 ],
#                 title=SentenceNode(children=[TextNode("Title")]),
#             ),
#         ],
#     )


# def test_source_ignores_mau_syntax():
#     source = """
#     [*source]
#     ----
#     :answer:42
#     The answer is {answer}
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 code=[
#                     SourceLineNode(number=1, value=RawNode(":answer:42")),
#                     SourceLineNode(number=2, value=RawNode("The answer is {answer}")),
#                 ],
#             ),
#         ],
#     )


# def test_source_respects_spaces_and_indentation():
#     source = """
#     [*source]
#     ----
#       //    This is a comment
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 code=[
#                     SourceLineNode(
#                         number=1, value=RawNode("  //    This is a comment")
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_callouts():
#     source = """
#     [*source, somelang, marker_delimiter=":"]
#     ----
#     import sys
#     import os:imp:

#     print(os.environ["HOME"]):env:
#     ----
#     imp: This is an import
#     env: Environment variables are paramount
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("import sys")),
#                     SourceLineNode(
#                         number=2, value=RawNode("import os"), marker=MarkerNode("imp")
#                     ),
#                     SourceLineNode(number=3, value=RawNode("")),
#                     SourceLineNode(
#                         number=4,
#                         value=RawNode('print(os.environ["HOME"])'),
#                         marker=MarkerNode("env"),
#                     ),
#                 ],
#                 callouts=[
#                     CalloutsEntryNode("imp", "This is an import"),
#                     CalloutsEntryNode("env", "Environment variables are paramount"),
#                 ],
#             ),
#         ],
#     )


# def test_source_callouts_possible_clash():
#     source = """
#     [*source, somelang, marker_delimiter=":"]
#     ----
#     import: os:imp:
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(
#                         number=1, value=RawNode("import: os"), marker=MarkerNode("imp")
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_callouts_one_single_marker_is_skipped():
#     source = """
#     [*source, somelang, marker_delimiter=":"]
#     ----
#     def something:
#         print("AAA")
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("def something:")),
#                     SourceLineNode(number=2, value=RawNode('    print("AAA")')),
#                 ],
#                 callouts=[],
#             ),
#         ],
#     )


# def test_source_callouts_custom_delimiter():
#     source = """
#     [*source, language=somelang, marker_delimiter="|"]
#     ----
#     import os|imp|
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(
#                         number=1, value=RawNode("import os"), marker=MarkerNode("imp")
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_callout_are_not_checked():
#     source = """
#     [*source, language=somelang, marker_delimiter=":"]
#     ----
#     import sys
#     ----
#     3: This is an import
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(number=1, value=RawNode("import sys")),
#                 ],
#                 callouts=[CalloutsEntryNode(marker="3", value="This is an import")],
#             ),
#         ],
#     )


# def test_source_callout_wrong_format():
#     # This is testing that all callouts in the secondary
#     # content have the right format "label: content"

#     source = """
#     [*source, language=somelang, marker_delimiter=":"]
#     ----
#     import sys
#     ----
#     3 This is an import
#     """

#     with pytest.raises(MauErrorException):
#         runner(source)


# def test_source_highlight_marker_is_special():
#     source = """
#     [*source, language=somelang]
#     ----
#     import os:@:
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(
#                         number=1,
#                         value=RawNode("import os"),
#                         highlight=True,
#                         highlight_style=None,
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_highlight_style_is_captured():
#     source = """
#     [*source, language=somelang]
#     ----
#     import os:@green:
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(
#                         number=1,
#                         value=RawNode("import os"),
#                         highlight=True,
#                         highlight_style="green",
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_source_highlights_custom_marker():
#     source = """
#     [*source, language=somelang, highlight_prefix="#"]
#     ----
#     import os:#:
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="somelang",
#                 code=[
#                     SourceLineNode(
#                         number=1,
#                         value=RawNode("import os"),
#                         highlight=True,
#                         highlight_style=None,
#                     ),
#                 ],
#             ),
#         ],
#     )


# def test_engine_source_language_is_reset():
#     source = """
#     [*source, python]
#     ----
#     ----

#     [*source]
#     ----
#     ----
#     """

#     assert_asdict(
#         runner(source).nodes,
#         [
#             SourceNode(
#                 language="python",
#                 code=[],
#             ),
#             SourceNode(
#                 language="text",
#                 code=[],
#             ),
#         ],
#     )
