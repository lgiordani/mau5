from mau.nodes.node import Node, NodeData, NodeDataContentMixin

HEADER_HELP = """
Syntax:

([ARGS])?
(@CONTROL)?
(=)+ HEADER

The header prefix `=` can be repeated multiple times to create a
header on a deeper level.
"""


class HeaderNodeData(NodeData, NodeDataContentMixin):
    """A header."""

    type = "header"

    def __init__(
        self,
        level: int,
        internal_id: str | None = None,
        alias: str | None = None,
        content: list[Node] | None = None,
    ):
        super().__init__()
        self.level = level
        self.internal_id = internal_id

        # This is an alias for this header,
        # used to link it internally.
        # Headers with an alias will still
        # receive a programmatic ID.
        self.alias = alias

        NodeDataContentMixin.__init__(self, content)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "level": self.level,
            "internal_id": self.internal_id,
            "alias": self.alias,
        }

        NodeDataContentMixin.content_asdict(self, base)

        return base
