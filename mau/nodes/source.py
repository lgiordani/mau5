from mau.nodes.node import Node, NodeInfo, NodeContentMixin, ValueNode, NodeLabelsMixin


class SourceMarkerNode(ValueNode):
    # This is a marker near a source code line

    type = "source-marker"


class SourceLineNode(Node):
    """A line of verbatim text or source code."""

    type = "source-line"

    def __init__(
        self,
        line_number: str,
        line_content: str,
        highlight_style: str | None = None,
        marker: SourceMarkerNode | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.line_number = line_number
        self.line_content = line_content
        self.highlight_style = highlight_style
        self.marker = marker

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "line_number": self.line_number,
            "line_content": self.line_content,
            "highlight_style": self.highlight_style,
        }

        if self.marker:
            base["custom"]["marker"] = self.marker.asdict()

        return base


class SourceNode(Node, NodeContentMixin, NodeLabelsMixin):
    """A block of verbatim text or source code.

    This node contains verbatim text or source code.
    """

    type = "source"

    def __init__(
        self,
        language: str,
        content: list[Node] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)
        self.language = language

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "language": self.language,
        }

        NodeContentMixin.content_asdict(self, base)
        NodeLabelsMixin.content_asdict(self, base)

        return base
