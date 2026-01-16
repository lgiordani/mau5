from mau.nodes.node import Node
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.text_buffer import Context


def test_paragraph_node_without_content():
    node = ParagraphNode()

    assert node.type == "paragraph"
    assert node.content == []
    assert node.asdict() == {
        "type": "paragraph",
        "custom": {
            "content": [],
            "labels": {},
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_paragraph_node_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphNode(content=nodes, labels=labels)
    assert node.asdict() == {
        "type": "paragraph",
        "custom": {
            "content": [
                {
                    "type": "none",
                    "custom": {},
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
                {
                    "type": "none",
                    "custom": {},
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
            ],
            "labels": {
                "somelabel": [
                    {
                        "type": "none",
                        "custom": {},
                        "info": {
                            "context": {
                                "end_column": 0,
                                "end_line": 0,
                                "source": None,
                                "start_column": 0,
                                "start_line": 0,
                            },
                            "named_args": {},
                            "subtype": None,
                            "tags": [],
                            "unnamed_args": [],
                        },
                    }
                ],
            },
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }


def test_paragraph_line_node_without_content():
    node = ParagraphLineNode()

    assert node.type == "paragraph-line"
    assert node.content == []
    assert node.asdict() == {
        "type": "paragraph-line",
        "custom": {
            "content": [],
            "labels": {},
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_paragraph_line_node_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node = ParagraphLineNode(content=nodes, labels=labels)
    assert node.asdict() == {
        "type": "paragraph-line",
        "custom": {
            "content": [
                {
                    "type": "none",
                    "custom": {},
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
                {
                    "type": "none",
                    "custom": {},
                    "info": {
                        "context": {
                            "end_column": 0,
                            "end_line": 0,
                            "source": None,
                            "start_column": 0,
                            "start_line": 0,
                        },
                        "named_args": {},
                        "subtype": None,
                        "tags": [],
                        "unnamed_args": [],
                    },
                },
            ],
            "labels": {
                "somelabel": [
                    {
                        "type": "none",
                        "custom": {},
                        "info": {
                            "context": {
                                "end_column": 0,
                                "end_line": 0,
                                "source": None,
                                "start_column": 0,
                                "start_line": 0,
                            },
                            "named_args": {},
                            "subtype": None,
                            "tags": [],
                            "unnamed_args": [],
                        },
                    }
                ],
            },
        },
        "info": {
            "context": {
                "end_column": 0,
                "end_line": 0,
                "source": None,
                "start_column": 0,
                "start_line": 0,
            },
            "named_args": {},
            "subtype": None,
            "tags": [],
            "unnamed_args": [],
        },
    }
