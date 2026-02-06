from mau.nodes.block import BlockNode
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_block_node():
    node = BlockNode()

    expected = {
        "_type": "block",
        "_context": Context.empty().asdict(),
        "parent": {},
        "classes": [],
        "labels": {},
        "content": [],
        "unnamed_args": [],
        "named_args": {},
        "tags": [],
        "internal_tags": [],
        "subtype": None,
    }

    check_visit_node(node, expected)
