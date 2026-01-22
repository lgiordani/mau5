from collections.abc import Sequence

from mau.nodes.node import Node, NodeContentMixin, NodeInfo


class FootnoteNode(Node, NodeContentMixin):
    """The content of a footnote."""

    type = "footnote"

    def __init__(
        self,
        # The unique internal name of the
        # referenced footnote content.
        # This name is used to link a
        # footnote macro (mention) with its
        # block (definition).
        name: str,
        # The unique public ID assigned to this footnote
        # (typically a progressive number).
        # This ID can be displayed on the rendered text.
        public_id: str | None = None,
        # The unique ID assigned to this footnote
        # that can be used to create references in
        # the rendered text.
        internal_id: str | None = None,
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)

        self.name = name
        self.public_id = public_id
        self.internal_id = internal_id
