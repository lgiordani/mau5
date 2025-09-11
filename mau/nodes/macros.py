from mau.nodes.node import NodeContent, ValueNodeContent


class MacroNodeContent(NodeContent):
    """This node contains a macro, with a name and arguments."""

    type = "macro"

    def __init__(
        self,
        name: str,
        unnamed_args: list[str] | None = None,
        named_args: dict[str, str] | None = None,
    ):
        self.name = name
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
                "unnamed_args": self.unnamed_args,
                "named_args": self.named_args,
            }
        )

        return base


class MacroClassNodeContent(NodeContent):
    """Text with one or more classes."""

    type = "macro.class"
    allowed_keys = {"text": "The text that is marked with the given classes."}

    def __init__(self, classes: list[str]):
        self.classes = classes

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "classes": self.classes,
            }
        )

        return base


class MacroLinkNodeContent(ValueNodeContent):
    """This node contains a link."""

    type = "macro.link"
    value_key = "target"
    allowed_keys = {"text": "The text linked to the target."}


class MacroImageNodeContent(NodeContent):
    """This node contains an inline image."""

    type = "macro.image"

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        width: str | None = None,
        height: str | None = None,
    ):
        self.uri = uri
        self.alt_text = alt_text
        self.width = width
        self.height = height

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "uri": self.uri,
                "alt_text": self.alt_text,
                "width": self.width,
                "height": self.height,
            }
        )

        return base


class MacroHeaderNodeContent(ValueNodeContent):
    """This node contains a link to a header node."""

    type = "macro.header"
    value_key = "id"
    allowed_keys = {
        "text": "The text linked to the header.",
        "header": "The anchor of the linked header.",
    }
