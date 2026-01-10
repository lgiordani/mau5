from mau.nodes.node import Node
from mau.nodes.paragraph import ParagraphLineNodeData, ParagraphNodeData


def test_paragraph_node_data_without_content():
    node_data = ParagraphNodeData()

    assert node_data.type == "paragraph"
    assert node_data.content == []
    assert node_data.asdict() == {
        "type": "paragraph",
        "custom": {
            "content": [],
            "labels": {},
        },
    }


def test_paragraph_node_data_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node_data = ParagraphNodeData(content=nodes, labels=labels)
    assert node_data.asdict() == {
        "type": "paragraph",
        "custom": {
            "content": [
                {
                    "data": {
                        "custom": {},
                        "type": "none",
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
                },
                {
                    "data": {
                        "custom": {},
                        "type": "none",
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
                },
            ],
            "labels": {
                "somelabel": [
                    {
                        "data": {
                            "custom": {},
                            "type": "none",
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
                ],
            },
        },
    }


def test_paragraph_line_node_data_without_content():
    node_data = ParagraphLineNodeData()

    assert node_data.type == "paragraph-line"
    assert node_data.content == []
    assert node_data.asdict() == {
        "type": "paragraph-line",
        "custom": {
            "content": [],
            "labels": {},
        },
    }


def test_paragraph_line_node_data_with_content():
    nodes: list[Node] = [Node(), Node()]
    labels: dict[str, list[Node]] = {"somelabel": [Node()]}

    node_data = ParagraphLineNodeData(content=nodes, labels=labels)
    assert node_data.asdict() == {
        "type": "paragraph-line",
        "custom": {
            "content": [
                {
                    "data": {
                        "custom": {},
                        "type": "none",
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
                },
                {
                    "data": {
                        "custom": {},
                        "type": "none",
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
                },
            ],
            "labels": {
                "somelabel": [
                    {
                        "data": {
                            "custom": {},
                            "type": "none",
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
                ],
            },
        },
    }
