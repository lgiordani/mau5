
from mau.nodes.node import Node, NodeInfo
from mau.nodes.node_arguments import NodeArguments


class ConditionNode(Node):
    type = "condition"

    def __init__(
        self,
        variable: str,
        comparison: str,
        value: str,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)

        self.variable = variable
        self.comparison = comparison
        self.value = value
