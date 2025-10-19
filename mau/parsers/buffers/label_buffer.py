from __future__ import annotations

from mau.nodes.node import Node, NodeContent


class LabelBuffer:
    """A buffer that stores a dictionary
    of labels that will be added to another
    node as children."""

    def __init__(self):
        # This is where the buffer keeps the
        # stored children.
        self.labels: dict[str, list[Node[NodeContent]]] = {}

    def push(
        self,
        role: str,
        children: list[Node[NodeContent]],
    ):
        # Store the given children.
        self.labels[role] = children

    def pop(self) -> dict[str, list[Node[NodeContent]]]:
        # Retrieve the stored arguments
        # and reset the internal slot.
        nodes = self.labels

        self.labels = {}

        return nodes
