from mau.nodes.block import BlockNode, RawContentLineNode, RawContentNode
from mau.nodes.node import NodeInfo
from mau.test_helpers import check_visit_node


def test_block_node():
    node = BlockNode()

    expected = {
        "_type": "block",
        "classes": [],
        "engine": None,
        "labels": {},
        "content": [],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_raw_content_line_node():
    node = RawContentLineNode("somevalue")

    expected = {
        "_type": "raw-content-line",
        "value": "somevalue",
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_raw_content_node():
    line1 = RawContentLineNode("somevalue1")
    line2 = RawContentLineNode("somevalue2")
    node = RawContentNode(lines=[line1, line2])

    expected = {
        "_type": "raw-content",
        "lines": [
            {
                "_type": "raw-content-line",
                "value": "somevalue1",
                "_info": NodeInfo.empty().asdict(),
            },
            {
                "_type": "raw-content-line",
                "value": "somevalue2",
                "_info": NodeInfo.empty().asdict(),
            },
        ],
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
