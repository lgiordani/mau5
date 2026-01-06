from mau.nodes.node import Node, NodeData, NodeDataContentMixin


class FootnoteNodeData(NodeData, NodeDataContentMixin):
    """The content of a footnote."""

    type = "footnote"

    def __init__(
        self,
        # The unique internal name of the
        # referenced footnote content.
        name: str,
        # The public ID assigned to this footnote
        # (typically a progressive number).
        public_id: str | None = None,
        # The private unique ID assigned to this footnote
        # that can be used as reference (e.g. for links).
        private_id: str | None = None,
        content: list[Node] | None = None,
    ):
        self.name = name
        self.public_id = public_id
        self.private_id = private_id

        NodeDataContentMixin.__init__(self, content)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "name": self.name,
            "public_id": self.public_id,
            "private_id": self.private_id,
        }

        NodeDataContentMixin.content_asdict(self, base)

        return base
