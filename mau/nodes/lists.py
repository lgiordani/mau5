from mau.nodes.node import NodeContent, ValueNodeContent


class ListItemNodeContent(ValueNodeContent):
    """An entry in a list."""

    type = "list_item"
    value_key = "level"
    allowed_keys = {"text": "The text of this list item"}


class ListNodeContent(NodeContent):
    """A list."""

    type = "list"
    allowed_keys = {"nodes": "The item nodes contained in this list. "}

    def __init__(
        self,
        ordered,
        main_node=False,
        start=1,
    ):
        self.ordered = ordered
        self.main_node = main_node
        self.start = start

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "ordered": self.ordered,
                "main_node": self.main_node,
                "start": self.start,
            }
        )

        return base
