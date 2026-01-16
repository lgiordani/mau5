from mau.nodes.node import Node, NodeInfo


class UnnamedArgumentNode(Node):
    """
    This node contains an unnamed argument.
    """

    type = "unnamed_argument"

    def __init__(
        self,
        value: str,
        content: list[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.value = value

    def asdict(self):
        base = super().asdict()
        base["custom"] = {"value": self.value}

        return base


class NamedArgumentNode(Node):
    """
    This node contains a named argument.
    """

    type = "named_argument"

    def __init__(
        self,
        key: str,
        value: str,
        content: list[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.key = key
        self.value = value

    def asdict(self):
        base = super().asdict()
        base["custom"] = {"key": self.key, "value": self.value}

        return base
