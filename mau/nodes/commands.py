from __future__ import annotations

from mau.nodes.footnotes import FootnoteNodeData
from mau.nodes.headers import HeaderNodeData
from mau.nodes.node import (
    Node,
    NodeData,
    NodeDataLabelsMixin,
)

COMMAND_HELP = """
Syntax:

(. LABEL)*
([ARGS])?
::COMMAND(:ARGS)?

The command operator `::` runs the requested command passing the optional arguments.
"""


class FootnotesNodeData(NodeData, NodeDataLabelsMixin):
    """The list of footnotes."""

    type = "footnotes"

    def __init__(
        self,
        footnotes: list[FootnoteNodeData] | None = None,
        labels: dict[str, list[Node]] | None = None,
    ):
        self.footnotes = footnotes or []

        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "footnotes": [i.asdict() for i in self.footnotes],
        }

        NodeDataLabelsMixin.content_asdict(self, base)

        return base


class TocItemNodeData(NodeData):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc.item"

    def __init__(
        self,
        header: HeaderNodeData,
        entries: list[TocItemNodeData] | None = None,
    ):
        self.header = header
        self.entries = entries or []

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "header": self.header.asdict(),
            "entries": [i.asdict() for i in self.entries],
        }

        return base


class TocNodeData(NodeData, NodeDataLabelsMixin):
    """The list of footnotes."""

    type = "toc"

    def __init__(
        self,
        plain_entries: list[HeaderNodeData] | None = None,
        nested_entries: list[TocItemNodeData] | None = None,
        labels: dict[str, list[Node]] | None = None,
    ):
        self.plain_entries = plain_entries or []
        self.nested_entries = nested_entries or []

        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "plain_entries": [i.asdict() for i in self.plain_entries],
            "nested_entries": [i.asdict() for i in self.nested_entries],
        }

        NodeDataLabelsMixin.content_asdict(self, base)

        return base


# class BlockGroupNodeData(NodeData):
#     type = "block-group"

#     def __init__(self, name: str, groups: dict[str, Node] | None = None):
#         super().__init__()
#         self.name = name
#         self.groups = groups or {}

#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {
#             "name": self.name,
#             "groups": {k: v.asdict() for k, v in self.groups.items()},
#         }

#         return base
