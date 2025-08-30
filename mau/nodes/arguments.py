from mau.nodes.node import NodeContent, ValueNodeContent


class UnnamedArgumentNodeContent(ValueNodeContent):
    """
    This node contains an unnamed argument.
    """

    type = "unnamed_argument"


class NamedArgumentNodeContent(NodeContent):
    """
    This node contains a named argument.
    """

    type = "named_argument"

    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def asdict(self):
        base = super().asdict()
        base.update({"key": self.key, "value": self.value})

        return base
