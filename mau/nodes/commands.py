from __future__ import annotations

from mau.nodes.footnotes import FootnoteNode
from mau.nodes.headers import HeaderNode
from mau.nodes.block import BlockNode
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


class FootnotesNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "footnotes"

    def __init__(
        self,
        footnotes: list[FootnoteNode] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.footnotes = footnotes or []

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "footnotes": [i.asdict() for i in self.footnotes],
        }

        NodeLabelsMixin.content_asdict(self, base)

        return base


class TocItemNode(Node):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc.item"

    def __init__(
        self,
        header: HeaderNode,
        entries: list[TocItemNode] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.header = header
        self.entries = entries or []

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "header": self.header.asdict(),
            "entries": [i.asdict() for i in self.entries],
        }

        return base


class TocNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "toc"

    def __init__(
        self,
        plain_entries: list[HeaderNode] | None = None,
        nested_entries: list[TocItemNode] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.plain_entries = plain_entries or []
        self.nested_entries = nested_entries or []

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "plain_entries": [i.asdict() for i in self.plain_entries],
            "nested_entries": [i.asdict() for i in self.nested_entries],
        }

        NodeLabelsMixin.content_asdict(self, base)

        return base


class BlockGroupNode(Node, NodeLabelsMixin):
    type = "block-group"

    def __init__(
        self,
        name: str,
        blocks: dict[str, Node[BlockNode]] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.name = name
        self.blocks = blocks or {}

    def asdict(self):
        base = super().asdict()

        base["custom"] = {
            "name": self.name,
            "blocks": {k: v.asdict() for k, v in self.blocks.items()},
        }

        NodeLabelsMixin.content_asdict(self, base)

        return base
