import pytest

from mau.nodes.headers import HeaderNodeContent
from mau.nodes.inline import TextNodeContent
from mau.nodes.macros import MacroHeaderNodeContent
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException
from mau.parsers.managers.header_links_manager import HeaderLinksManager

# from mau.parsers.document_parser import DocumentParser
from mau.test_helpers import (
    generate_context,
    # init_parser_factory,
    # parser_runner_factory,
)

# init_parser = init_parser_factory(DocumentLexer, DocumentParser)

# runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_header_links_manager():
    ilm = HeaderLinksManager()

    header_node = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(
            named_args={"id": "someheader"}, context=generate_context(0, 0, 0, 0)
        ),
        children={
            "content": [
                Node(
                    content=TextNodeContent("Header"),
                )
            ]
        },
    )

    link_node = Node(
        content=MacroHeaderNodeContent("someheader"),
    )

    ilm.add_header("someheader", header_node)
    ilm.add_links([link_node])

    ilm.process()

    assert link_node.children["header"] == [header_node]
    assert link_node.content.target_id == header_node.content.internal_id


def test_header_links_manager_no_link():
    ilm = HeaderLinksManager()

    header_node = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(
            named_args={"id": "someheader"}, context=generate_context(0, 0, 0, 0)
        ),
        children={
            "content": [
                Node(
                    content=TextNodeContent("Header"),
                )
            ]
        },
    )

    ilm.add_header("someheader", header_node)

    ilm.process()


def test_header_links_manager_no_header():
    ilm = HeaderLinksManager()

    link_node = Node(
        content=MacroHeaderNodeContent("someheader"),
    )

    ilm.add_links([link_node])

    with pytest.raises(MauParserException) as exc:
        ilm.process()

    assert exc.value.context is link_node.info.context


def test_header_links_manager_duplicate_header():
    ilm = HeaderLinksManager()

    header_node1 = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(
            named_args={"id": "someheader"}, context=generate_context(0, 0, 0, 0)
        ),
    )

    header_node2 = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(
            named_args={"id": "someheader"}, context=generate_context(0, 0, 0, 0)
        ),
    )

    ilm.add_header("someheader", header_node1)

    with pytest.raises(MauParserException) as exc:
        ilm.add_header("someheader", header_node2)

    assert exc.value.context is header_node2.info.context


def test_header_links_manager_update():
    ilm_src = HeaderLinksManager()
    ilm_dst = HeaderLinksManager()

    header_node = Node(
        content=HeaderNodeContent(2, "XXXXXX"),
        info=NodeInfo(
            named_args={"id": "someheader"}, context=generate_context(0, 0, 0, 0)
        ),
        children={
            "content": [
                Node(
                    content=TextNodeContent("Header"),
                )
            ]
        },
    )

    link_node = Node(
        content=MacroHeaderNodeContent("someheader"),
    )

    ilm_src.add_header("someheader", header_node)
    ilm_src.add_links([link_node])

    ilm_dst.update(ilm_src)
    ilm_dst.process()

    assert link_node.children["header"] == [header_node]
