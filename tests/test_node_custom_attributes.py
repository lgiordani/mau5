import pytest

from mau.nodes.block import BlockNode
from mau.nodes.condition import ConditionNode
from mau.nodes.document import DocumentNode, HorizontalRuleNode
from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.include import (
    BlockGroupNode,
    FootnotesItemNode,
    FootnotesNode,
    IncludeImageNode,
    IncludeMauNode,
    IncludeNode,
    TocItemNode,
    TocNode,
)
from mau.nodes.inline import StyleNode, TextNode, VerbatimNode, WordNode
from mau.nodes.list import ListItemNode, ListNode
from mau.nodes.macro import (
    MacroClassNode,
    MacroFootnoteNode,
    MacroHeaderNode,
    MacroImageNode,
    MacroLinkNode,
    MacroNode,
    MacroRawNode,
    MacroUnicodeNode,
)
from mau.nodes.node import Node, ValueNode, WrapperNode
from mau.nodes.paragraph import ParagraphLineNode, ParagraphNode
from mau.nodes.raw import RawLineNode, RawNode
from mau.nodes.source import SourceLineNode, SourceMarkerNode, SourceNode

CASES = [
    (Node(), []),
    (ValueNode("value"), []),
    (WrapperNode(), []),
    (BlockNode(classes=["alpha", "beta"]), ["alpha", "beta"]),
    (FootnotesItemNode(footnote=FootnoteNode(name="fn1")), []),
    (FootnotesNode(), []),
    (TocItemNode(header=HeaderNode(level=1)), []),
    (TocNode(), []),
    (BlockGroupNode(name="group"), []),
    (ConditionNode(variable="var", comparison="==", value="1"), []),
    (HorizontalRuleNode(), []),
    (DocumentNode(), []),
    (FootnoteNode(name="fn2"), []),
    (HeaderNode(level=2), ["level2"]),
    (IncludeNode(content_type="mau"), ["mau"]),
    (IncludeImageNode(uri="image.png"), []),
    (IncludeMauNode(uri="doc.mau"), []),
    (WordNode("word"), []),
    (TextNode("text"), []),
    (VerbatimNode("verbatim"), []),
    (StyleNode(style="bold"), ["bold"]),
    (ListItemNode(level=1), []),
    (ListNode(ordered=True), []),
    (MacroNode(name="note"), ["note"]),
    (MacroClassNode(classes=["classy"]), []),
    (MacroLinkNode(target="https://example.com"), []),
    (MacroImageNode(uri="image.png"), []),
    (MacroHeaderNode(target_name="section"), []),
    (MacroFootnoteNode(name="fn3"), []),
    (MacroUnicodeNode("1f600"), []),
    (MacroRawNode("raw"), []),
    (ParagraphLineNode(), []),
    (ParagraphNode(), []),
    (RawLineNode("raw"), []),
    (RawNode(), []),
    (SourceMarkerNode("marker"), []),
    (SourceLineNode(line_number="1", line_content="code"), []),
    (SourceNode(), []),
]


def _id_from_node(node):
    t = getattr(node, "type", None)
    return str(t) if t is not None else node.__class__.__name__


IDS = [_id_from_node(node) for node, _expected in CASES]


@pytest.mark.parametrize(("node", "expected"), CASES, ids=IDS)
def test_custom_attributes_for_nodes(node, expected):
    assert node.custom_attributes == expected
