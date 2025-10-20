from mau.nodes.node import NodeContent


class HeaderNodeContent(NodeContent):
    """A header."""

    type = "header"
    allowed_keys = {
        "text": "The text of the header.",
    }

    def __init__(
        self,
        level: int,
        internal_id: str | None = None,
    ):
        self.level = level
        self.internal_id = internal_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "internal_id": self.internal_id,
            }
        )

        return base
