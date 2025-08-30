from mau.nodes.arguments import NamedArgumentNodeContent, UnnamedArgumentNodeContent


def test_unnamed_argument_node_value():
    node_content = UnnamedArgumentNodeContent("somevalue")

    assert node_content.type == "unnamed_argument"
    assert node_content.value == "somevalue"
    assert node_content.asdict() == {"type": "unnamed_argument", "value": "somevalue"}


def test_named_argument_node_value():
    node = NamedArgumentNodeContent("somekey", "somevalue")

    assert node.type == "named_argument"
    assert node.key == "somekey"
    assert node.value == "somevalue"
    assert node.asdict() == {
        "key": "somekey",
        "value": "somevalue",
        "type": "named_argument",
    }
