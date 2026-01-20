from collections.abc import Sequence

from mau.nodes.node import Node, NodeContentMixin, NodeInfo, ValueNode


class WordNode(ValueNode):
    """This is a single word, it's used internally
    and eventually packed together with others into
    a TextNode
    """

    type = "word"


class TextNode(ValueNode):
    """This contains plain text and is created
    as a collation of multiple WordNode objects
    """

    type = "text"


class VerbatimNode(ValueNode):
    """This node contains verbatim text."""

    type = "verbatim"


class StyleNode(Node, NodeContentMixin):
    """Describes the style applied to a node."""

    type = "style"

    def __init__(
        self,
        style: str,
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)

        self.style = style

    @property
    def custom_attributes(self) -> list[str]:
        return [self.style]
