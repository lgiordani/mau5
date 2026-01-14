# from mau.nodes.node import (
#     Node,
#     NodeData,
#     NodeDataContentMixin,
#     NodeDataLabelsMixin,
# )
# 
# HEADER_HELP = """
# Syntax:
# 
# ([ARGS])?
# (@CONTROL)?
# (=)+ HEADER
# 
# The header prefix `=` can be repeated multiple times to create a
# header on a deeper level.
# """
# 
# 
# class HeaderNodeData(NodeData, NodeDataLabelsMixin, NodeDataContentMixin):
#     """A header."""
# 
#     type = "header"
# 
#     def __init__(
#         self,
#         level: int,
#         internal_id: str | None = None,
#         alias: str | None = None,
#         content: list[Node] | None = None,
#         labels: dict[str, list[Node]] | None = None,
#         source_text: str | None = None,
#     ):
#         super().__init__()
#         self.level = level
#         self.internal_id = internal_id
# 
#         # This is an alias for this header,
#         # used to link it internally.
#         # Headers with an alias will still
#         # receive a programmatic ID.
#         self.alias = alias
# 
#         # The source text of the header.
#         # This is the unparsed text
#         # that will be used to generate
#         # the unique id.
#         self.source_text = source_text
# 
#         NodeDataContentMixin.__init__(self, content)
#         NodeDataLabelsMixin.__init__(self, labels)
# 
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {
#             "level": self.level,
#             "internal_id": self.internal_id,
#             "alias": self.alias,
#         }
# 
#         NodeDataLabelsMixin.content_asdict(self, base)
#         NodeDataContentMixin.content_asdict(self, base)
# 
#         return base
