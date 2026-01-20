import pytest

from mau.nodes.header import HeaderNode
from mau.nodes.inline import TextNode
from mau.nodes.macro import MacroHeaderNode
from mau.parsers.managers.header_links_manager import HeaderLinksManager


def test_header_links_manager():
    ilm = HeaderLinksManager()

    header_node = HeaderNode(
        2,
        "XXXXXX",
        content=[
            TextNode(
                "Header",
            )
        ],
    )

    link_node = MacroHeaderNode("someheader")

    ilm.add_header("someheader", header_node)
    ilm.add_links([link_node])

    assert link_node.header is None
    assert link_node.target_id is None

    ilm.process()

    assert link_node.header == header_node
    assert link_node.target_id == header_node.internal_id


def test_header_links_manager_no_link():
    ilm = HeaderLinksManager()

    header_node = HeaderNode(
        2,
        "XXXXXX",
        content=[
            TextNode(
                "Header",
            )
        ],
    )

    ilm.add_header("someheader", header_node)

    ilm.process()


def test_header_links_manager_no_header():
    ilm = HeaderLinksManager()

    link_node = MacroHeaderNode("someheader")

    ilm.add_links([link_node])

    with pytest.raises(ValueError):
        ilm.process()


def test_header_links_manager_duplicate_header():
    ilm = HeaderLinksManager()

    header_node1 = HeaderNode(2, "XXXXXX")

    header_node2 = HeaderNode(2, "XXXXXX")

    ilm.add_header("someheader", header_node1)

    with pytest.raises(ValueError):
        ilm.add_header("someheader", header_node2)


def test_header_links_manager_update():
    ilm_src = HeaderLinksManager()
    ilm_dst = HeaderLinksManager()

    header_node = HeaderNode(
        2,
        "XXXXXX",
        content=[
            TextNode(
                "Header",
            )
        ],
    )

    link_node = MacroHeaderNode("someheader")

    ilm_src.add_header("someheader", header_node)
    ilm_src.add_links([link_node])

    ilm_dst.update(ilm_src)
    ilm_dst.process()

    assert link_node.header == header_node
