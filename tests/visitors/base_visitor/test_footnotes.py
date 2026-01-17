from mau.nodes.footnotes import FootnoteNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_macro_footnote_node_parameters():
    node = FootnoteNode("somename")

    expected = {
        "_type": "footnote",
        "name": "somename",
        "public_id": None,
        "private_id": None,
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
