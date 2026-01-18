from collections.abc import Sequence, Mapping
from mau.nodes.node import (
    Node,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
)

HEADER_HELP = """
Syntax:

([ARGS])?
(@CONTROL)?
(=)+ HEADER

The header prefix `=` can be repeated multiple times to create a
header on a deeper level.
"""


class HeaderNode(Node, NodeLabelsMixin, NodeContentMixin):
    """A header."""

    type = "header"

    def __init__(
        self,
        level: int,
        internal_id: str | None = None,
        alias: str | None = None,
        content: list[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        source_text: str | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.level = level

        # This is an internal ID, usually calculated
        # automatically, used to create hyperlinks.
        self.internal_id = internal_id

        # This is an alias for this header,
        # used to link it internally.
        # Headers with an alias will still
        # receive a programmatic ID.
        self.alias = alias

        # The source text of the header.
        # This is the unparsed text
        # that will be used to generate
        # the unique id.
        self.source_text = source_text

        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)
