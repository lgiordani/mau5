from mau.nodes.block import BlockNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_block_node():
    node = BlockNode()

    expected = {
        "_type": "block",
        "_info": NodeInfo.empty().asdict(),
        "_parent_info": {},
        "classes": [],
        "labels": {},
        "content": [],
    }

    check_visit_node(node, expected)
