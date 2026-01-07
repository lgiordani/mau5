from mau.nodes.node import Node, NodeData, NodeDataContentMixin, WrapperNodeData


class ParagraphNodeData(WrapperNodeData):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    Its content is a list of lines (ParagraphLineNodeData)
    """

    type = "paragraph"


class ParagraphLineNodeData(WrapperNodeData):
    """
    This node represents the content of a line of a paragraph.
    """

    type = "paragraph-line"
