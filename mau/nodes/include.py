from collections.abc import Sequence, Mapping
from mau.nodes.node import Node, NodeInfo, NodeLabelsMixin

INCLUDE_HELP = """
Syntax:

([URI+, ARGS])?
(@CONTROL)?
(. LABEL)*
<< TYPE(:URI+, ARGS)?

The include operator `<<` includes content of type TYPE using the provided ARGS.
The ARGS must contain at least one unnamed URI.
"""

INCLUDE_IMAGE_HELP = """
Syntax:

([URI, ALT_TEXT, CLASSES, ARGS])?
(@CONTROL)?
(. LABEL)*
<< image(:URI, ALT_TEXT, CLASSES, ARGS)?

The include operator `<< image` includes an image using the provided URI.
"""


class IncludeNode(Node, NodeLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include"
    long_help = INCLUDE_HELP

    def __init__(
        self,
        content_type: str,
        uris: Sequence[str],
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.content_type = content_type
        self.uris = uris


class IncludeImageNode(Node, NodeLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include-image"
    long_help = INCLUDE_IMAGE_HELP

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        classes: Sequence[str] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.uri = uri
        self.alt_text = alt_text
        self.classes = classes or []
