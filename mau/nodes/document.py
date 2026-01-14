# # Page nodes can be found at top level in a page
# 
# from mau.nodes.node import Node, NodeData, NodeDataLabelsMixin, WrapperNodeData
# 
# HORIZONTAL_RULE_HELP = """
# Syntax:
# 
# ([ARGS])?
# ---
# 
# The horizontal rule marks a separation between text sections
# in the same document.
# """
# 
# 
# class HorizontalRuleNodeData(NodeData, NodeDataLabelsMixin):
#     """A horizontal rule."""
# 
#     type = "horizontal_rule"
# 
#     def __init__(
#         self,
#         labels: dict[str, list[Node]] | None = None,
#     ):
#         super().__init__()
#         NodeDataLabelsMixin.__init__(self, labels)
# 
#     def asdict(self):
#         base = super().asdict()
#         NodeDataLabelsMixin.content_asdict(self, base)
# 
#         return base
# 
# 
# class DocumentNodeData(WrapperNodeData):
#     """A document.
# 
#     This node represents the full document.
# 
#     Arguments:
#         content: the content of the document
#     """
# 
#     type = "document"
