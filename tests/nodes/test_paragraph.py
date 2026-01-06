from mau.nodes.paragraph import ParagraphLineNodeData, ParagraphNodeData
from mau.test_helpers import check_node_data_with_content


def test_paragraph_node_data_without_content():
    node_data = ParagraphNodeData()

    assert node_data.type == "paragraph"
    assert node_data.content == []
    assert node_data.asdict() == {
        "type": "paragraph",
        "custom": {
            "content": [],
        },
    }


def test_paragraph_node_data_with_content():
    check_node_data_with_content(ParagraphNodeData)


def test_paragraph_line_node_data_without_content():
    node_data = ParagraphLineNodeData()

    assert node_data.type == "paragraph-line"
    assert node_data.content == []
    assert node_data.asdict() == {
        "type": "paragraph-line",
        "custom": {
            "content": [],
        },
    }


def test_paragraph_line_node_data_with_content():
    check_node_data_with_content(ParagraphLineNodeData)
