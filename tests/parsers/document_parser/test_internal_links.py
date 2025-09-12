import pytest

from mau.environment.environment import Environment
from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import SentenceNodeContent, TextNodeContent
from mau.nodes.macros import MacroHeaderNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    compare_nodes,
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_internal_link():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: "XXXXXX"
    )

    source = """
    This is a paragraph with an internal link [header](someid, link text).

    [id=someid]
    == Header
    """

    parser = runner(source, environment)

    header_node = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(context=generate_context(4, 0), named_args={"id": "someid"}),
        children={
            "entries": [],
            "text": [
                Node(
                    content=SentenceNodeContent(),
                    info=NodeInfo(context=generate_context(4, 3)),
                    children={
                        "content": [
                            Node(
                                content=TextNodeContent("Header"),
                                info=NodeInfo(context=generate_context(4, 3)),
                            )
                        ]
                    },
                )
            ],
        },
    )

    link_node = Node(
        content=MacroHeaderNodeContent("someid"),
        info=NodeInfo(context=generate_context(1, 42)),
        children={
            "header": [header_node],
            "text": [
                Node(
                    content=TextNodeContent("link text"),
                    info=NodeInfo(context=generate_context(1, 59)),
                )
            ],
        },
    )

    compare_nodes([parser.internal_links_manager._headers["someid"]], [header_node])
    compare_nodes(parser.internal_links_manager._links, [link_node])


def test_internal_link_no_header():
    environment = Environment()
    environment.setvar(
        "mau.parser.header_anchor_function", lambda text, level: "XXXXXX"
    )

    source = """
    This is a paragraph with an internal link [header](someotherid, link text).

    [id=someid]
    == Header
    """

    with pytest.raises(MauParserException) as exc:
        runner(source, environment)

    assert exc.value.context == generate_context(1, 42)


# def test_internal_link_header_in_block():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: "XXXXXX"
#     )

#     source = """
#     This is a paragraph with an internal link [header](someid, text).

#     ====
#     [id=someid]
#     == Header
#     ====
#     """

#     parser = runner(textwrap.dedent(source), environment)
#     parser.finalise()

#     header_node = HeaderNode(
#         value=SentenceNode(children=[TextNode("Header")]),
#         level="2",
#         anchor="XXXXXX",
#         kwargs={"id": "someid"},
#     )

#     assert parser.internal_links_manager.links == [
#         MacroHeaderNode(
#             header_id="someid", header=header_node, children=[TextNode("text")]
#         )
#     ]
#     assert parser.internal_links_manager.headers == {"someid": header_node}


# def test_internal_link_link_in_block():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: "XXXXXX"
#     )

#     source = """
#     ====
#     This is a paragraph with an internal link [header](someid, text).
#     ====

#     [id=someid]
#     == Header
#     """

#     parser = runner(textwrap.dedent(source), environment)
#     parser.finalise()

#     header_node = HeaderNode(
#         value=SentenceNode(children=[TextNode("Header")]),
#         level="2",
#         anchor="XXXXXX",
#         kwargs={"id": "someid"},
#     )

#     assert parser.internal_links_manager.links == [
#         MacroHeaderNode(
#             header_id="someid", header=header_node, children=[TextNode("text")]
#         )
#     ]
#     assert parser.internal_links_manager.headers == {"someid": header_node}


# def test_internal_link_link_and_header_in_block():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.header_anchor_function", lambda text, level: "XXXXXX"
#     )

#     source = """
#     ====
#     This is a paragraph with an internal link [header](someid, text).

#     [id=someid]
#     == Header
#     ====
#     """

#     parser = runner(textwrap.dedent(source), environment)
#     parser.finalise()

#     header_node = HeaderNode(
#         value=SentenceNode(children=[TextNode("Header")]),
#         level="2",
#         anchor="XXXXXX",
#         kwargs={"id": "someid"},
#     )

#     assert parser.internal_links_manager.links == [
#         MacroHeaderNode(
#             header_id="someid", header=header_node, children=[TextNode("text")]
#         )
#     ]
#     assert parser.internal_links_manager.headers == {"someid": header_node}
