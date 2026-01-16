from mau.nodes.headers import HeaderNode
from mau.test_helpers import check_node_with_content
from mau.text_buffer import Context


def test_header_node_without_content():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        alias="some_alias",
    )

    assert node.type == "header"
    assert node.level == 42
    assert node.internal_id == "some_internal_id"
    assert node.alias == "some_alias"
    assert node.asdict() == {
        "type": "header",
        "custom": {
            "level": 42,
            "internal_id": "some_internal_id",
            "alias": "some_alias",
            "labels": {},
            "content": [],
        },
        "info": {
            "context": Context.empty().asdict(),
            "unnamed_args": [],
            "named_args": {},
            "tags": [],
            "subtype": None,
        },
    }


def test_header_node_with_content():
    node = HeaderNode(
        level=42,
        internal_id="some_internal_id",
        alias="some_alias",
    )
    check_node_with_content(node)
