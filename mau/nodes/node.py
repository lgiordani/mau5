from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from mau.text_buffer import Context

if TYPE_CHECKING:
    from mau.visitors.base_visitor import BaseVisitor


class NodeInfo:
    """A class to collect information about a
    node, such as its context and arguments."""

    def __init__(
        self,
        context: Context,
        unnamed_args: list | None = None,
        named_args: dict | None = None,
        tags: list | None = None,
        subtype: str | None = None,
    ):
        self.context = context
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}
        self.tags = tags or []
        self.subtype = subtype

    @classmethod
    def empty(cls) -> NodeInfo:
        return NodeInfo(context=Context.empty())

    def asdict(self):
        return {
            "context": self.context.asdict(),
            "unnamed_args": self.unnamed_args,
            "named_args": self.named_args,
            "tags": self.tags,
            "subtype": self.subtype,
        }


class Node:
    type: str = "none"
    custom_attributes: list[str] = []

    def __init__(
        self,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        # Set the parent of this node.
        self.parent: Node | None = parent

        self.info: NodeInfo = info or NodeInfo.empty()

    def set_parent(self, parent: Node) -> Node:
        # Set the parent of this node.
        self.parent = parent

        return self

    def accept(self, visitor: BaseVisitor, *args, **kwargs) -> dict:
        # Simple implementation of the visitor pattern.
        # Here, the node accepts a visitor and
        # calls one of the visitor's methods according
        # to the node content type.

        # Some node types contain a dot to allow templates
        # to be created in a hierarchy of directories
        # but dots are not allowed in function names
        method_name = f"_visit_{self.type.replace('.', '__').replace('-', '_')}"

        # Try to call the computed method. If not
        # available, call a default method.
        try:
            method = getattr(visitor, method_name)
        except AttributeError:
            method = getattr(visitor, "_visit_default")

        return method(self, *args, **kwargs)


class NodeContentMixin:
    def __init__(
        self,
        content: Sequence[Node] | None = None,
    ):
        self.content = content or []


class NodeLabelsMixin:
    def __init__(
        self,
        labels: Mapping[str, Sequence[Node]] | None = None,
    ):
        self.labels = labels or {}


class ValueNode(Node):
    type = "value"

    def __init__(
        self,
        value: str,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.value = value


class WrapperNode(Node, NodeContentMixin):
    type = "wrapper"

    def __init__(
        self,
        parent: Node | None = None,
        info: NodeInfo | None = None,
        content: Sequence[Node] | None = None,
    ):
        super().__init__(parent=parent, info=info)
        NodeContentMixin.__init__(self, content)
