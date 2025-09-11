from mau.nodes.node import NodeContent


class ParagraphNodeContent(NodeContent):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    """

    type = "paragraph"
    allowed_keys = {
        "content": "The text contained in this paragraph.",
        "title": "The title of this paragraph.",
    }
