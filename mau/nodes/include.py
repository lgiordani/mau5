from mau.nodes.node import NodeContent

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


class IncludeNodeContent(NodeContent):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include"
    allowed_keys = {}
    long_help = INCLUDE_HELP

    def __init__(
        self,
        content_type: str,
        uris: list[str],
    ):
        self.content_type = content_type
        self.uris = uris

    @property
    def custom_attributes(self) -> list[str]:
        return [self.content_type]

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "content_type": self.content_type,
                "uris": self.uris,
            }
        )

        return base


class IncludeImageNodeContent(NodeContent):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include-image"
    allowed_keys = {}
    long_help = INCLUDE_IMAGE_HELP

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        classes: list[str] | None = None,
    ):
        self.uri = uri
        self.alt_text = alt_text
        self.classes = classes or []

    @property
    def custom_attributes(self) -> list[str]:
        result = super().custom_attributes
        result.extend(self.classes)
        return result

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "uri": self.uri,
                "alt_text": self.alt_text,
                "classes": self.classes,
            }
        )

        return base
