from mau.nodes.source import (
    SourceLineNode,
    SourceMarkerNode,
    SourceNode,
)
from mau.test_helpers import check_visit_node
from mau.text_buffer import Context


def test_source_line_marker_node():
    node = SourceMarkerNode("somemarker")

    expected = {
        "_type": "source-marker",
        "_context": Context.empty().asdict(),
        "value": "somemarker",
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_source_line_node():
    node = SourceLineNode("42", "somecontent")

    expected = {
        "_type": "source-line",
        "_context": Context.empty().asdict(),
        "line_number": "42",
        "line_content": "somecontent",
        "highlight_style": None,
        "marker": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_source_line_node_with_marker():
    marker_node = SourceMarkerNode("somemarker")
    node = SourceLineNode("42", "somecontent", marker=marker_node)

    expected = {
        "_type": "source-line",
        "_context": Context.empty().asdict(),
        "line_number": "42",
        "line_content": "somecontent",
        "highlight_style": None,
        "marker": {
            "_type": "source-marker",
            "_context": Context.empty().asdict(),
            "value": "somemarker",
            "named_args": {},
            "parent": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)


def test_source_node():
    node = SourceNode("somelanguage")

    expected = {
        "_type": "source",
        "_context": Context.empty().asdict(),
        "language": "somelanguage",
        "classes": [],
        "content": [],
        "labels": {},
        "named_args": {},
        "parent": {},
        "subtype": None,
        "tags": [],
        "unnamed_args": [],
    }

    check_visit_node(node, expected)
