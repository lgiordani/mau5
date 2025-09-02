from mau.nodes.node import NodeContent, ValueNodeContent


class ParagraphNodeContent(ValueNodeContent):
    """A paragraph."""

    type = "paragraph"

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
