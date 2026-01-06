from functools import partial

from mau.nodes.headers import HeaderNodeData
from mau.test_helpers import check_node_data_with_content


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
            "content": [],
        },
    }


def test_header_node_data_with_content():
    node_data_class = partial(
        HeaderNodeData, level=42, internal_id="some_internal_id", alias="some_alias"
    )
    check_node_data_with_content(node_data_class)
