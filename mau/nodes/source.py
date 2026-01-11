from mau.nodes.node import Node, NodeData, NodeDataContentMixin, ValueNodeData


class SourceMarkerNodeData(ValueNodeData):
    # This is a marker near a source code line

    type = "source-marker"


class SourceLineNodeData(NodeData):
    """A line of verbatim text or source code."""

    type = "source-line"

    def __init__(
        self,
        line_number: str,
        line_content: str,
        highlight_style: str | None = None,
        marker: Node[SourceMarkerNodeData] | None = None,
    ):
        super().__init__()

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


class SourceNodeData(NodeData, NodeDataContentMixin):
    """A block of verbatim text or source code.

    This node contains verbatim text or source code.
    """

    type = "source"

    def __init__(
        self,
        language: str,
        content: list[Node] | None = None,
    ):
        super().__init__()
        self.language = language

        NodeDataContentMixin.__init__(self, content)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "language": self.language,
        }

        NodeDataContentMixin.content_asdict(self, base)

        return base
