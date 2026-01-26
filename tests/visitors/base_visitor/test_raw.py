from mau.nodes.node import NodeInfo
from mau.nodes.raw import RawLineNode, RawNode
from mau.test_helpers import check_visit_node


def test_raw_content_line_node():
    node = RawLineNode("somevalue")

    expected = {
        "_type": "raw-line",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "value": "somevalue",
    }

    check_visit_node(node, expected)


def test_raw_content_node():
    line1 = RawLineNode("somevalue1")
    line2 = RawLineNode("somevalue2")
    node = RawNode(content=[line1, line2])

    expected = {
        "_type": "raw",
        "_parent_info": {},
        "_info": NodeInfo.empty().asdict(),
        "classes": [],
        "labels": {},
        "content": [
            {
                "_info": NodeInfo.empty().asdict(),
                "_type": "raw-line",
                "_parent_info": {},
                "value": "somevalue1",
            },
            {
                "_info": NodeInfo.empty().asdict(),
                "_type": "raw-line",
                "value": "somevalue2",
                "_parent_info": {},
            },
        ],
    }

    check_visit_node(node, expected)
