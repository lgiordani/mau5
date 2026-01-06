# # Page nodes can be found at top level in a page

# from mau.nodes.node import NodeData

# HORIZONTAL_RULE_HELP = """
# Syntax:

# ([ARGS])?
# ---

# The horizontal rule marks a separation between text sections
# in the same document.
# """


# class HorizontalRuleNodeData(NodeData):
#     """A horizontal rule."""

#     type = "horizontal_rule"


# class WrapperNodeData(NodeData):
#     type = "wrapper"
#     allowed_keys = {"content": "The nodes inside the wrapper"}


# class DocumentNodeData(WrapperNodeData):
#     """A document.

#     This node represents the full document.

#     Arguments:
#         content: the content of the document
#     """

#     type = "document"


# class ContainerNodeData(WrapperNodeData):
#     type = "container"

#     def __init__(self, label: str):
#         self.label = label

#     def asdict(self):
#         base = super().asdict()
#         base.update({"label": self.label})

#         return base
