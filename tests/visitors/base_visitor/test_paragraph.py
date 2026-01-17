from mau.nodes.node import Node, NodeInfo
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.test_helpers import check_visit_node


def test_paragraph_line_node_without_content():
    node = ParagraphLineNode()

    expected = {
        "_type": "paragraph-line",
        "content": [],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_paragraph_line_node_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphLineNode(content=nodes, labels=labels)

    expected = {
        "_type": "paragraph-line",
        "content": [
            {
                "_type": "none",
                "_info": NodeInfo.empty().asdict(),
            },
            {
                "_type": "none",
                "_info": NodeInfo.empty().asdict(),
            },
        ],
        "labels": {
            "somelabel": [
                {
                    "_type": "none",
                    "_info": NodeInfo.empty().asdict(),
                }
            ],
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_paragraph_node_without_content():
    node = ParagraphNode()

    expected = {
        "_type": "paragraph",
        "lines": [],
        "labels": {},
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)


def test_paragraph_node_with_content():
    lines: list[ParagraphLineNode] = [ParagraphLineNode(), ParagraphLineNode()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphNode(lines=lines, labels=labels)

    expected = {
        "_type": "paragraph",
        "lines": [
            {
                "_type": "paragraph-line",
                "content": [],
                "labels": {},
                "_info": NodeInfo.empty().asdict(),
            },
            {
                "_type": "paragraph-line",
                "content": [],
                "labels": {},
                "_info": NodeInfo.empty().asdict(),
            },
        ],
        "labels": {
            "somelabel": [
                {
                    "_type": "none",
                    "_info": NodeInfo.empty().asdict(),
                }
            ],
        },
        "_info": NodeInfo.empty().asdict(),
    }

    check_visit_node(node, expected)
