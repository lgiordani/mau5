# Page nodes can be found at top level in a page

from mau.nodes.node import NodeContent


class HorizontalRuleNodeContent(NodeContent):
    """A horizontal rule."""

    type = "horizontal_rule"


# class ContainerNode(Node):
#     node_type = "container"

#     def clone(self):
#         return self.__class__(
#             parent=self.parent,
#             parent_position=self.parent_position,
#             children=self.children,
#             subtype=self.subtype,
#             args=self.args,
#             kwargs=self.kwargs,
#             tags=self.tags,
#             context=self.context,
#         )


# class DocumentNode(ContainerNode):
#     """A document.

#     This node represents the full document.

#     Arguments:
#         content: the content of the document
#     """

#     node_type = "document"
