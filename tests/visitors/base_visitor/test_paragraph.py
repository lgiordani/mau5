from mau.nodes.node import Node
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_paragraph_line_node_without_content():
    node = ParagraphLineNode()

    expected = {
        "_type": "paragraph-line",
        "_context": Context.empty().asdict(),
        "content": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_paragraph_line_node_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphLineNode(content=nodes, labels=labels)

    expected = {
        "_type": "paragraph-line",
        "_context": Context.empty().asdict(),
        "content": [
            {
                "_type": "none",
                "_context": Context.empty().asdict(),
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
            {
                "_type": "none",
                "_context": Context.empty().asdict(),
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
        ],
        "labels": {
            "somelabel": [
                {
                    "_type": "none",
                    "_context": Context.empty().asdict(),
                    "named_args": {},
                    "parent": {},
                    "subtype": None,
                    "tags": [],
                    "internal_tags": [],
                    "unnamed_args": [],
                }
            ],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_paragraph_node_without_content():
    node = ParagraphNode()

    expected = {
        "_type": "paragraph",
        "_context": Context.empty().asdict(),
        "lines": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_paragraph_node_with_content():
    lines: list[ParagraphLineNode] = [ParagraphLineNode(), ParagraphLineNode()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphNode(lines=lines, labels=labels)

    expected = {
        "_type": "paragraph",
        "_context": Context.empty().asdict(),
        "lines": [
            {
                "_type": "paragraph-line",
                "_context": Context.empty().asdict(),
                "content": [],
                "labels": {},
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
            {
                "_type": "paragraph-line",
                "_context": Context.empty().asdict(),
                "content": [],
                "labels": {},
                "named_args": {},
                "parent": {},
                "subtype": None,
                "tags": [],
                "internal_tags": [],
                "unnamed_args": [],
            },
        ],
        "labels": {
            "somelabel": [
                {
                    "_type": "none",
                    "_context": Context.empty().asdict(),
                    "named_args": {},
                    "parent": {},
                    "subtype": None,
                    "tags": [],
                    "internal_tags": [],
                    "unnamed_args": [],
                }
            ],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "internal_tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
