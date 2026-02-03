from mau.nodes.raw import RawLineNode, RawNode
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_raw_content_line_node():
    node = RawLineNode("somevalue")

    expected = {
        "_type": "raw-line",
        "_context": Context.empty().asdict(),
        "value": "somevalue",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_raw_content_node():
    line1 = RawLineNode("somevalue1")
    line2 = RawLineNode("somevalue2")
    node = RawNode(content=[line1, line2])

    expected = {
        "_type": "raw",
        "_context": Context.empty().asdict(),
        "classes": [],
        "labels": {},
        "content": [
            {
                "_context": Context.empty().asdict(),
                "_type": "raw-line",
                "value": "somevalue1",
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "unnamed_args": [],
            },
            {
                "_context": Context.empty().asdict(),
                "_type": "raw-line",
                "value": "somevalue2",
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "unnamed_args": [],
            },
        ],
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
