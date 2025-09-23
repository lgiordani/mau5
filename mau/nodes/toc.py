from mau.nodes.node import NodeContent


class TocNodeContent(NodeContent):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc"
    allowed_keys = {
        "nested_entries": "The ToC entries in a tree-like fashion.",
        "plain_entries": "The ToC entries in a plain list without nesting.",
    }


class TocItemNodeContent(NodeContent):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc-item"
    allowed_keys = {
        "text": "The text of the header.",
        "entries": "The ToC entries nested under this entry.",
    }

    def __init__(
        self,
        level: int,
        unique_id: str,
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
