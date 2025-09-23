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
        unique_id: str | None = None,
    ):
        self.level = level
        self.unique_id = unique_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "unique_id": self.unique_id,
            }
        )

        return base
