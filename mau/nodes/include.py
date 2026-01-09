from mau.nodes.node import NodeData, NodeDataLabelsMixin, Node, WrapperNodeData

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


class IncludeNodeData(NodeData, NodeDataLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include"
    long_help = INCLUDE_HELP

    def __init__(
        self,
        content_type: str,
        uris: list[str],
        labels: dict[str, Node[WrapperNodeData]] | None = None,
    ):
        super().__init__()
        self.content_type = content_type
        self.uris = uris

        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "content_type": self.content_type,
            "uris": self.uris,
        }

        NodeDataLabelsMixin.content_asdict(self, base)

        return base


class IncludeImageNodeData(NodeData, NodeDataLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include-image"
    long_help = INCLUDE_IMAGE_HELP

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        classes: list[str] | None = None,
        labels: dict[str, Node[WrapperNodeData]] | None = None,
    ):
        self.uri = uri
        self.alt_text = alt_text
        self.classes = classes or []

        NodeDataLabelsMixin.__init__(self, labels)

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "uri": self.uri,
            "alt_text": self.alt_text,
            "classes": self.classes,
        }

        NodeDataLabelsMixin.content_asdict(self, base)

        return base
