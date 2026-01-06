import pytest
from mau.parsers.managers.header_links_manager import HeaderLinksManager

from mau.nodes.headers import HeaderNodeData
from mau.nodes.inline import TextNodeData
from mau.nodes.macros import MacroHeaderNodeData
from mau.nodes.node import Node, NodeInfo
from mau.parsers.base_parser import MauParserException

from mau.test_helpers import (
    generate_context,
)


def test_header_links_manager():
    ilm = HeaderLinksManager()

    header_data = HeaderNodeData(
        2,
        "XXXXXX",
        content=[
            Node(
                data=TextNodeData("Header"),
            )
        ],
    )

    link_data = MacroHeaderNodeData("someheader")

    ilm.add_header("someheader", header_data)
    ilm.add_links([link_data])

    assert link_data.header is None
    assert link_data.target_id is None

    ilm.process()

    assert link_data.header == header_data
    assert link_data.target_id == header_data.internal_id


def test_header_links_manager_no_link():
    ilm = HeaderLinksManager()

    header_data = HeaderNodeData(
        2,
        "XXXXXX",
        content=[
            Node(
                data=TextNodeData("Header"),
            )
        ],
    )

    ilm.add_header("someheader", header_data)

    ilm.process()


def test_header_links_manager_no_header():
    ilm = HeaderLinksManager()

    link_data = MacroHeaderNodeData("someheader")

    ilm.add_links([link_data])

    with pytest.raises(ValueError):
        ilm.process()


def test_header_links_manager_duplicate_header():
    ilm = HeaderLinksManager()

    header_data1 = HeaderNodeData(2, "XXXXXX")

    header_data2 = HeaderNodeData(2, "XXXXXX")

    ilm.add_header("someheader", header_data1)

    with pytest.raises(ValueError):
        ilm.add_header("someheader", header_data2)


def test_header_links_manager_update():
    ilm_src = HeaderLinksManager()
    ilm_dst = HeaderLinksManager()

    header_data = HeaderNodeData(
        2,
        "XXXXXX",
        content=[
            Node(
                data=TextNodeData("Header"),
            )
        ],
    )

    link_data = MacroHeaderNodeData("someheader")

    ilm_src.add_header("someheader", header_data)
    ilm_src.add_links([link_data])

    ilm_dst.update(ilm_src)
    ilm_dst.process()

    assert link_data.header == header_data
