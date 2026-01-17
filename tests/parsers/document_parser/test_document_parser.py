from mau.environment.environment import Environment
from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.document import DocumentNode
from mau.nodes.inline import TextNode
from mau.nodes.node import NodeInfo
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    compare_asdict_list,
    compare_asdict_object,
    generate_context,
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


def test_parse_output_custom_content_container():
    source = "text"

    class CustomDocumentNode(DocumentNode):
        type = "custom-document"

    environment = Environment()
    environment["mau.parser.document_wrapper"] = CustomDocumentNode

    compare_asdict_object(
        runner(source, environment).output["document"],
        CustomDocumentNode(
            content=[
                ParagraphNode(
                    lines=[
                        ParagraphLineNode(
                            content=[
                                TextNode(
                                    "text",
                                    info=NodeInfo(context=generate_context(0, 0, 0, 4)),
                                )
                            ],
                            info=NodeInfo(context=generate_context(0, 0, 0, 4)),
                        )
                    ],
                    info=NodeInfo(context=generate_context(0, 0, 0, 4)),
                )
            ],
            info=NodeInfo(context=generate_context(0, 0, 0, 4)),
        ),
    )
