from __future__ import annotations

from mau.nodes.node import Node, NodeData, WrapperNodeData


class LabelBuffer:
    """A buffer that stores a dictionary
    of labels that will be added to another
    node as children."""

    def __init__(self):
        # This is where the buffer keeps the
        # stored children.
        self.labels: dict[str, Node[WrapperNodeData]] = {}

    def push(
        self,
        role: str,
        node: Node[WrapperNodeData],
    ):
        # Store the given children.
        self.labels[role] = node

    def pop(self) -> dict[str, Node[WrapperNodeData]]:
        # Retrieve the stored arguments
        # and reset the internal slot.
        labels = self.labels

        self.labels = {}

        return labels
