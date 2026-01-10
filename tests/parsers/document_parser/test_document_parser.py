from mau.lexers.document_lexer import DocumentLexer
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_list,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_parse_discards_empty_lines():
    source = "\n\n\n\n"

    parser = runner(source)

    compare_asdict_list(parser.nodes, [])


def test_parse_output():
    source = ""

    assert runner(source).output == {
        "document": None,
        "nested_toc": None,
        "plain_toc": None,
    }


# def test_parse_output_custom_content_container():
#     source = "text"

#     environment = Environment()
#     document = DocumentNode()
#     environment.setvar("mau.parser.content_wrapper", document)

#     assert runner(source, environment).output == {
#         "content": document,
#         "toc": ContainerNode(children=[TocNode()]),
#     }


# def test_parse_output_custom_toc_container():
#     source = ""

#     environment = Environment()
#     document = DocumentNode(children=[TocNode()])
#     environment.setvar("mau.parser.toc_wrapper", document)

#     assert runner(source, environment).output == {
#         "content": ContainerNode(children=[]),
#         "toc": document,
#     }


# def test_command():
#     source = "::somecommand:arg1, arg2, name1=value1, name2=value2"

#     assert runner(source).nodes == []


# def test_command_without_arguments():
#     source = "::somecommand:"

#     assert runner(source).nodes == []


# def test_style_underscore():
#     source = """
#     This is _underscore_ text
#     """

#     assert runner(source).nodes == [
#         ParagraphNode(
#             children=[
#                 TextNode("This is "),
#                 StyleNode(
#                     value="underscore",
#                     children=[
#                         TextNode("underscore"),
#                     ],
#                 ),
#                 TextNode(" text"),
#             ],
#         )
#     ]


# def test_style_at_beginning():
#     source = """
#     *This is star text*
#     """

#     assert runner(source).nodes == [
#         ParagraphNode(
#             children=[
#                 StyleNode(
#                     value="star",
#                     children=[
#                         TextNode("This is star text"),
#                     ],
#                 ),
#             ],
#         )
#     ]


# def test_style_not_closed():
#     source = r"""
#     This ` is a backtick and this _an underscore
#     """

#     assert runner(source).nodes == [
#         ParagraphNode(
#             children=[
#                 TextNode("This ` is a backtick and this _an underscore"),
#             ],
#         )
#     ]


# def test_style_escape_markers():
#     source = r"""
#     This is \_underscore\_ and this is \`verbatim\`
#     """

#     assert runner(source).nodes == [
#         ParagraphNode(
#             children=[
#                 TextNode("This is _underscore_ and this is `verbatim`"),
#             ],
#         )
#     ]
