from mau.nodes.node import NodeContent


class HeaderNodeContent(NodeContent):
    """A header."""

    type = "header"
    allowed_keys = {
        "text": "The text of the header.",
        # "entries": "All headers nested under this in the ToC.",
    }

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
