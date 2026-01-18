from collections.abc import Sequence, Mapping
from mau.nodes.node import Node, NodeContentMixin, NodeInfo


class FootnoteNode(Node, NodeContentMixin):
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
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)

        self.name = name
        self.public_id = public_id
        self.private_id = private_id
