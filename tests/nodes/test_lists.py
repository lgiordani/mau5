from mau.nodes.lists import ListItemNodeContent, ListNodeContent


def test_list_item_node_content():
    node_content = ListItemNodeContent(3)

    assert node_content.type == "list_item"
    assert node_content.value == 3
    assert node_content.asdict() == {"type": "list_item", "level": 3}


def test_list_node_content():
    node_content = ListNodeContent(ordered=True)

    assert node_content.type == "list"
    assert node_content.ordered is True
    assert node_content.main_node is False
    assert node_content.start == 1
    assert node_content.asdict() == {
        "type": "list",
        "ordered": True,
        "main_node": False,
        "start": 1,
    }


def test_list_node_content_unordered():
    node_content = ListNodeContent(ordered=False)

    assert node_content.type == "list"
    assert node_content.ordered is False
    assert node_content.main_node is False
    assert node_content.start == 1
    assert node_content.asdict() == {
        "type": "list",
        "ordered": False,
        "main_node": False,
        "start": 1,
    }


def test_list_node_content_parameters():
    node_content = ListNodeContent(ordered=True, main_node=True, start=42)

    assert node_content.type == "list"
    assert node_content.ordered is True
    assert node_content.main_node is True
    assert node_content.start == 42
    assert node_content.asdict() == {
        "type": "list",
        "ordered": True,
        "main_node": True,
        "start": 42,
    }
