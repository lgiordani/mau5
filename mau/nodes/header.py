from mau.nodes.node import NodeContent


class HeaderNodeContent(NodeContent):
    """A header."""

    type = "header"
    allowed_keys = ["content"]

    def __init__(
        self,
        level: int,
        anchor: str,
    ):
        self.level = level
        self.anchor = anchor

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "anchor": self.anchor,
            }
        )

        return base
