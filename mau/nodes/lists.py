from mau.nodes.node import (
    Node,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
    WrapperNode,
)

LIST_HELP = """
Syntax:

([URI+, ARGS])?
(*+|#+) TEXT

The list prefix `*` or `#` creates a list item. The prefix can be
specified multiple times to nest items, e.g.

* Item 1
** Item 1.1
* Item2

The symbol `*` creates an unordered list, while the symbol `#`
creates an ordered one. The two can be mixed, e.g.

# Numbered item 1
** Bullet point 1
** Bullet point 2
** Bullet point 3
# Numbered item 2

Arguments:

* `start` - Can be a positive integer or "auto", defaults to "auto".
            Controls the starting number for the first item of the list.
"""


class ListItemNode(WrapperNode):
    """An entry in a list."""

    type = "list_item"

    def __init__(
        self,
        level: int,
        parent: Node | None = None,
        info: NodeInfo | None = None,
        content: list[Node] | None = None,
    ):
        super().__init__(parent=parent, info=info, content=content)

        self.level = level

    def asdict(self):
        base = super().asdict()
        base["custom"]["level"] = self.level

        return base


class ListNode(Node, NodeContentMixin, NodeLabelsMixin):
    """A list."""

    type = "list"

    def __init__(
        self,
        ordered,
        main_node=False,
        start=1,
        content: list[Node] | None = None,
        labels: dict[str, list[Node]] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.ordered = ordered
        self.main_node = main_node
        self.start = start

    def asdict(self):
        base = super().asdict()
        base["custom"] = {
            "ordered": self.ordered,
            "main_node": self.main_node,
            "start": self.start,
        }

        NodeContentMixin.content_asdict(self, base)
        NodeLabelsMixin.content_asdict(self, base)

        return base
