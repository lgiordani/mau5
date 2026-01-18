from collections.abc import Sequence, Mapping
from mau.nodes.node import Node, NodeContentMixin, NodeInfo, NodeLabelsMixin, ValueNode


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


class SourceNode(Node, NodeContentMixin, NodeLabelsMixin):
    """A block of verbatim text or source code.

    This node contains verbatim text or source code.
    """

    type = "source"

    def __init__(
        self,
        language: str,
        content: Sequence[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.language = language
