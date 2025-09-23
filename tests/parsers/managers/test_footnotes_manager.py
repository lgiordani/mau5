from unittest.mock import patch

import pytest

from mau.lexers.document_lexer.lexer import DocumentLexer
from mau.nodes.footnotes import FootnoteNodeContent
from mau.nodes.macros import MacroFootnoteNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser.parser import MauParserException
from mau.parsers.document_parser.managers.footnotes_manager import FootnotesManager
from mau.parsers.document_parser.parser import DocumentParser
from mau.test_helpers import (
    generate_context,
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_footnotes_manager_init():
    fnm = FootnotesManager()

    assert fnm.mentions == []
    assert fnm.data == {}


def test_footnotes_manager_add_mention():
    fnm = FootnotesManager()

    footnote_macro_node = Node(content=MacroFootnoteNodeContent("footnote_name"))

    fnm.add_mention(footnote_macro_node)

    assert fnm.mentions == [footnote_macro_node]
    assert fnm.data == {}


def test_footnotes_manager_add_data():
    fnm = FootnotesManager()

    footnote_name = "footnote_name"
    footnote_node = Node(
        content=FootnoteNodeContent(footnote_name), children={"content": []}
    )

    fnm.add_data(footnote_node)

    assert fnm.mentions == []
    assert fnm.data == {"footnote_name": footnote_node}


def test_footnotes_manager_add_data_duplicate_name():
    fnm = FootnotesManager()

    context1 = generate_context(1, 1)
    context2 = generate_context(2, 2)

    footnote_name = "footnote_name"
    footnote_node1 = Node(
        content=FootnoteNodeContent(footnote_name),
        children={"content": []},
        info=NodeInfo(context=context1),
    )
    footnote_node2 = Node(
        content=FootnoteNodeContent(footnote_name),
        children={"content": []},
        info=NodeInfo(context=context2),
    )

    fnm.add_data(footnote_node1)

    with pytest.raises(MauParserException) as exc:
        fnm.add_data(footnote_node2)

    assert fnm.mentions == []
    assert fnm.data == {"footnote_name": footnote_node1}
    assert exc.value.context == context2


@patch(
    "mau.parsers.document_parser.managers.footnotes_manager.default_footnote_unique_id"
)
def test_footnotes_manager_process(mock_footnote_unique_id):
    mock_footnote_unique_id.return_value = "XXYY"

    fnm = FootnotesManager()

    footnote_name1 = "footnote_name1"
    footnote_name2 = "footnote_name2"

    footnote_macro_node1 = Node(content=MacroFootnoteNodeContent(footnote_name1))
    fnm.add_mention(footnote_macro_node1)

    footnote_macro_node2 = Node(content=MacroFootnoteNodeContent(footnote_name2))
    fnm.add_mention(footnote_macro_node2)

    footnote_node1 = Node(
        content=FootnoteNodeContent(footnote_name1), children={"content": []}
    )
    fnm.add_data(footnote_node1)

    footnote_node2 = Node(
        content=FootnoteNodeContent(footnote_name2), children={"content": []}
    )
    fnm.add_data(footnote_node2)

    fnm.process()

    assert footnote_macro_node1.content.public_id == "1"
    assert footnote_node1.content.public_id == "1"
    assert footnote_macro_node1.content.private_id == "XXYY"
    assert footnote_node1.content.private_id == "XXYY"

    assert footnote_macro_node2.content.public_id == "2"
    assert footnote_node2.content.public_id == "2"
    assert footnote_macro_node2.content.private_id == "XXYY"
    assert footnote_node2.content.private_id == "XXYY"

    assert footnote_macro_node1.children["footnote"] == [footnote_node1]
    assert footnote_macro_node2.children["footnote"] == [footnote_node2]


# def test_footnotes_manager_full_parse():
#     environment = Environment()
#     environment.setvar(
#         "mau.parser.footnote_unique_id_function",
#         lambda node: "XXXXYY",
#     )

#     source = """
#     This is a paragraph with a footnote [footnote](someid).

#     [id=someid]
#     == Header
#     """

#     parser = runner(source, environment)
