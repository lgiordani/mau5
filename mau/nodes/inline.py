from mau.nodes.node import NodeContent, ValueNodeContent


class WordNodeContent(ValueNodeContent):
    """This is a single word, it's used internally
    and eventually packed together with others into
    a TextNode
    """

    type = "word"


class TextNodeContent(ValueNodeContent):
    """This contains plain text and is created
    as a collation of multiple WordNode objects
    """

    type = "text"


class RawNodeContent(ValueNodeContent):
    """This contains plain text but the content
    should be treated as raw data and left untouched.
    E.g. it shouldn't be escaped.
    """

    type = "raw"


class VerbatimNodeContent(ValueNodeContent):
    """This node contains verbatim text."""

    type = "verbatim"


class SentenceNodeContent(NodeContent):
    """A recursive container node.

    This node represents the content of a paragraph, but it is recursive,
    while ParagraphNode is not.
    """

    type = "sentence"
    allowed_keys = {"content": "The text nodes contained into this node."}


class StyleNodeContent(ValueNodeContent):
    """Describes the style applied to a node."""

    type = "style"
    allowed_keys = {"content": "The text nodes contained into this node."}
