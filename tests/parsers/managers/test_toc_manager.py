from mau.lexers.document_lexer import DocumentLexer
from mau.nodes.headers import HeaderNodeContent
from mau.nodes.node import Node
from mau.nodes.toc import TocNodeContent
from mau.parsers.document_parser import DocumentParser
from mau.parsers.managers.toc_manager import TocManager, add_nodes_under_level
from mau.test_helpers import (
    init_parser_factory,
    parser_runner_factory,
)

init_parser = init_parser_factory(DocumentLexer, DocumentParser)

runner = parser_runner_factory(DocumentLexer, DocumentParser)


def test_add_nodes_under_level():
    node_a = Node(content=HeaderNodeContent(1, "A"))
    node_b = Node(content=HeaderNodeContent(2, "B"))
    node_c = Node(content=HeaderNodeContent(3, "C"))
    node_d = Node(content=HeaderNodeContent(2, "D"))
    node_e = Node(content=HeaderNodeContent(2, "E"))
    node_f = Node(content=HeaderNodeContent(1, "F"))
    node_g = Node(content=HeaderNodeContent(3, "G"))

    nodes = [
        node_a,
        node_b,
        node_c,
        node_d,
        node_e,
        node_f,
        node_g,
    ]

    children: list[Node[HeaderNodeContent]] = []

    idx = add_nodes_under_level(0, nodes, 0, children)

    assert idx == len(nodes)

    assert children == [node_a, node_f]
    assert node_a.children["entries"] == [node_b, node_d, node_e]
    assert node_b.children["entries"] == [node_c]
    assert node_f.children["entries"] == [node_g]


def test_add_nodes_under_level_starts_with_any():
    node_a = Node(content=HeaderNodeContent(3, "A"))
    node_b = Node(content=HeaderNodeContent(2, "B"))
    node_c = Node(content=HeaderNodeContent(3, "C"))

    nodes = [
        node_a,
        node_b,
        node_c,
    ]

    children: list[Node[HeaderNodeContent]] = []

    add_nodes_under_level(0, nodes, 0, children)

    assert children == [node_a, node_b]
    assert node_a.children["entries"] == []
    assert node_b.children["entries"] == [node_c]


def test_add_nodes_under_level_can_terminate_with_single_node():
    node_a = Node(content=HeaderNodeContent(3, "A"))
    node_b = Node(content=HeaderNodeContent(2, "B"))
    node_c = Node(content=HeaderNodeContent(1, "C"))

    nodes = [
        node_a,
        node_b,
        node_c,
    ]

    children: list[Node[HeaderNodeContent]] = []

    add_nodes_under_level(0, nodes, 0, children)

    assert children == [node_a, node_b, node_c]
    assert node_a.children["entries"] == []
    assert node_b.children["entries"] == []
    assert node_c.children["entries"] == []


def test_toc_manager():
    tm = TocManager()
    node_a = Node(content=HeaderNodeContent(1, "A"))
    node_b = Node(content=HeaderNodeContent(2, "B"))
    toc_a = Node(content=TocNodeContent())

    tm.add_header(node_a)
    tm.add_header(node_b)
    tm.add_toc_node(toc_a)

    tm.process()

    assert toc_a.children["nested_entries"] == [node_a]
    assert toc_a.children["plain_entries"] == [node_a, node_b]
    assert node_a.children["entries"] == [node_b]
