from mau.nodes.node import NodeContent


class ParagraphNodeContent(NodeContent):
    """A non-recursive container node.

    This node represents the content of a paragraph in a document.
    Its content is a list of lines (ParagraphLineNodeContent)
    """

    type = "paragraph"
    allowed_keys = {
        "content": "The lines contained in this paragraph.",
    }


class ParagraphLineNodeContent(NodeContent):
    """
    This node represents the content of a line of a paragraph.
    """

    type = "paragraph-line"
    allowed_keys = {
        "content": "The text contained in this line.",
    }
