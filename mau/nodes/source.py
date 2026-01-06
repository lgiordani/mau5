# from mau.nodes.node import NodeData, ValueNodeData


# class SourceNodeData(NodeData):
#     """A block of verbatim text or source code.

#     This node contains verbatim text or source code.
#     """

#     type = "source"
#     allowed_keys = {"code": "A list of code lines"}

#     def __init__(
#         self,
#         language: str,
#     ):
#         self.language = language

#     def asdict(self):
#         base = super().asdict()
#         base.update(
#             {
#                 "language": self.language,
#             }
#         )

#         return base


# class SourceLineNodeData(NodeData):
#     """A line of verbatim text or source code."""

#     type = "source-line"
#     allowed_keys = {"marker": "The marker attached to this line"}

#     def __init__(
#         self,
#         line_number: str,
#         line_content: str,
#         highlight_style: str | None = None,
#     ):
#         self.line_number = line_number
#         self.line_content = line_content
#         self.highlight_style = highlight_style

#     def asdict(self):
#         base = super().asdict()
#         base.update(
#             {
#                 "line_number": self.line_number,
#                 "line_content": self.line_content,
#                 "highlight_style": self.highlight_style,
#             }
#         )

#         return base


# class SourceMarkerNodeContext(ValueNodeData):
#     # This is a marker near a source code line

#     type = "source-marker"
