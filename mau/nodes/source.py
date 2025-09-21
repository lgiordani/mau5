from mau.nodes.node import NodeContent

# class CalloutsEntryNode(Node):
#     # This is an entry in the list of callouts after source code

#     node_type = "callouts_entry"

#     def __init__(
#         self,
#         marker,
#         value,
#         parent=None,
#         parent_position=None,
#         children=None,
#         subtype=None,
#         args=None,
#         kwargs=None,
#         tags=None,
#         context=None,
#     ):
#         super().__init__(
#             parent=parent,
#             parent_position=parent_position,
#             children=children,
#             subtype=subtype,
#             args=args,
#             kwargs=kwargs,
#             tags=tags,
#             context=context,
#         )
#         self.marker = marker
#         self.value = value

#     def _custom_dict(self):
#         return {
#             "value": self.value,
#             "marker": self.marker,
#         }


# class MarkerNode(Node):
#     # This is a marker near a source code line

#     node_type = "marker"

#     def __init__(
#         self,
#         value,
#         parent=None,
#         parent_position=None,
#         children=None,
#         subtype=None,
#         args=None,
#         kwargs=None,
#         tags=None,
#         context=None,
#     ):
#         super().__init__(
#             parent=parent,
#             parent_position=parent_position,
#             children=children,
#             subtype=subtype,
#             args=args,
#             kwargs=kwargs,
#             tags=tags,
#             context=context,
#         )
#         self.value = value

#     def _custom_dict(self):
#         return {
#             "value": self.value,
#         }


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
        # callouts=None,
        # classes=None,
        # title=None,
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

    def __init__(
        self,
        line_number: str,
        line_content: str,
        marker: str | None = None,
        highlight_style: str | None = None,
    ):
        self.line_number = line_number
        self.line_content = line_content
        self.marker = marker
        self.highlight_style = highlight_style

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "line_number": self.line_number,
                "line_content": self.line_content,
                "marker": self.marker,
                "highlight_style": self.highlight_style,
            }
        )

        return base
