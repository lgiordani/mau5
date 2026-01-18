from __future__ import annotations

from collections.abc import Sequence, Mapping
from mau.nodes.block import BlockNode
from mau.nodes.footnotes import FootnoteNode
from mau.nodes.headers import HeaderNode
from mau.nodes.node import (
    Node,
    NodeInfo,
    NodeLabelsMixin,
)

COMMAND_HELP = """
Syntax:

(. LABEL)*
([ARGS])?
::COMMAND(:ARGS)?

The command operator `::` runs the requested command passing the optional arguments.
"""


class FootnotesItemNode(Node):
    type = "footnotes-item"

    def __init__(
        self,
        footnote: FootnoteNode,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.footnote = footnote


class FootnotesNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "footnotes"

    def __init__(
        self,
        footnotes: Sequence[FootnotesItemNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.footnotes = footnotes or []


class TocItemNode(Node):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc-item"

    def __init__(
        self,
        header: HeaderNode,
        entries: Sequence[TocItemNode] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.header = header
        self.entries = entries or []


class TocNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "toc"

    def __init__(
        self,
        plain_entries: Sequence[HeaderNode] | None = None,
        nested_entries: Sequence[TocItemNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.plain_entries = plain_entries or []
        self.nested_entries = nested_entries or []


class BlockGroupNode(Node, NodeLabelsMixin):
    type = "block-group"

    def __init__(
        self,
        name: str,
        blocks: Mapping[str, BlockNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.name = name
        self.blocks = blocks or {}
