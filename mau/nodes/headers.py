from mau.nodes.node import Node, NodeData, NodeDataContentMixin, WrapperNodeData

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
        text: Node[WrapperNodeData] | None = None,
        source_text: str | None = None,
    ):
        super().__init__()
        self.level = level
        self.internal_id = internal_id

        # This is an alias for this header,
        # used to link it internally.
        # Headers with an alias will still
        # receive a programmatic ID.
        self.alias = alias

        # The text of the header.
        self.text = text

        # The source text of the header.
        # This is the unparsed text
        # that will be used to generate
        # the unique id.
        self.source_text = source_text

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "level": self.level,
            "internal_id": self.internal_id,
            "alias": self.alias,
        }

        if self.text:
            base["custom"]["text"] = self.text.asdict()

        return base
