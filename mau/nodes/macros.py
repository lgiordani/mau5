from mau.nodes.node import NodeContent, ValueNodeContent


class MacroNodeContent(ValueNodeContent):
    """This node contains a macro, with a name and arguments."""

    type = "macro"
    value_key = "name"


class MacroClassNodeContent(NodeContent):
    """Text with one or more classes."""

    type = "macro.class"

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


class MacroHeaderNodeContent(NodeContent):
    """This node contains a link to a header node."""

    type = "macro.header"

    def __init__(self, _id: str, text: str | None = None):
        self.id = _id
        self.text = text

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "id": self.id,
                "text": self.text,
            }
        )

        return base
