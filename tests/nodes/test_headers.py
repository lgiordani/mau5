
from mau.nodes.headers import HeaderNodeData
from mau.nodes.inline import TextNodeData
from mau.nodes.node import Node


def test_header_node_data_without_content():
    node_data = HeaderNodeData(
        level=42,
        internal_id="some_internal_id",
        alias="some_alias",
    )

    assert node_data.type == "header"
    assert node_data.level == 42
    assert node_data.internal_id == "some_internal_id"
    assert node_data.alias == "some_alias"
    assert node_data.asdict() == {
        "type": "header",
        "custom": {
            "level": 42,
            "internal_id": "some_internal_id",
            "alias": "some_alias",
            "labels": {},
            "content": [],
        },
    }


def test_header_node_data_with_content():
    node_data = HeaderNodeData(
        level=42,
        internal_id="some_internal_id",
        alias="some_alias",
        content=[
            Node(data=TextNodeData("Some")),
            Node(data=TextNodeData("nodes")),
        ],
    )

    assert node_data.asdict() == {
        "type": "header",
        "custom": {
            "level": 42,
            "internal_id": "some_internal_id",
            "alias": "some_alias",
            "labels": {},
            "content": [
                {
                    "data": {
                        "type": "text",
                        "custom": {
                            "value": "Some",
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
                },
                {
                    "data": {
                        "type": "text",
                        "custom": {
                            "value": "nodes",
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
                },
            ],
        },
    }
