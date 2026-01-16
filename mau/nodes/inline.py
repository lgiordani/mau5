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


class RawNode(ValueNode):
    """This contains plain text but the content
    should be treated as raw data and left untouched.
    E.g. it shouldn't be escaped.
    """

    type = "raw"


class VerbatimNode(ValueNode):
    """This node contains verbatim text."""

    type = "verbatim"


class StyleNode(Node, NodeContentMixin):
    """Describes the style applied to a node."""

    type = "style"

    def __init__(
        self,
        style: str,
        content: list[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)

        self.style = style

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "style": self.style,
        }

        NodeContentMixin.content_asdict(self, base)

        return base
