from mau.nodes.node import NodeContent, ValueNodeContent


class SourceNodeContent(NodeContent):
    """A block of verbatim text or source code.

    This node contains verbatim text or source code.

    Arguments:
        language: the language of the code contained in this block
        callouts: a list of callout CalloutEntryNode objects
        code: content of the block
        title: title of this block
        kwargs: named arguments
    """

    type = "source"
    allowed_keys = {"code": "A list of code lines"}

    def __init__(
        self,
        language: str,
    ):
        self.language = language

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "language": self.language,
            }
        )

        return base


class SourceLineNodeContent(NodeContent):
    """A line of verbatim text or source code.

    This node contains a single line of verbatim text or source code.

    Arguments:
        value: the verbatim content
        marker: the marker attached to this line
        kwargs: named arguments
    """

    type = "source-line"
    allowed_keys = {"marker": "The marker attached to this line"}

    def __init__(
        self,
        line_number: str,
        line_content: str,
        highlight_style: str | None = None,
    ):
        self.line_number = line_number
        self.line_content = line_content
        self.highlight_style = highlight_style

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "line_number": self.line_number,
                "line_content": self.line_content,
                "highlight_style": self.highlight_style,
            }
        )

        return base


class SourceMarkerNodeContext(ValueNodeContent):
    # This is a marker near a source code line

    type = "source-marker"
