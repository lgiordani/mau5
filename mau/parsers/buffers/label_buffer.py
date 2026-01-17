from __future__ import annotations

from mau.nodes.node import Node


class LabelBuffer:
    """A buffer that stores a dictionary
    of labels that will be added to another
    node as children."""

    def __init__(self):
        # This is where the buffer keeps the
        # stored children.
        self.labels: dict[str, list[Node]] = {}

    def push(
        self,
        role: str,
        nodes: list[Node],
    ):
        # Store the given children.
        self.labels[role] = nodes

    def pop(self) -> dict[str, list[Node]]:
        # Retrieve the stored arguments
        # and reset the internal slot.
        labels = self.labels

        self.labels = {}

        return labels
