from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from mau.text_buffer import Context

from .node_arguments import NodeArguments

if TYPE_CHECKING:
    from mau.visitors.base_visitor import BaseVisitor


class NodeInfo:
    """A class to collect information about a
    node, such as its context and arguments."""

    def __init__(
        self,
        context: Context,
    ):
        self.context = context

    @classmethod
    def empty(cls) -> NodeInfo:
        return NodeInfo(context=Context.empty())

    def asdict(self):
        return {
            "context": self.context.asdict(),
        }

    def __eq__(self, other: NodeInfo):
        if not isinstance(other, NodeInfo):
            return NotImplemented

        return self.asdict() == other.asdict()

    def __repr__(self):
        return f"{self.asdict()}"


class Node:
    type: str = "none"

    def __init__(
        self,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        # Set the parent of this node.
        self.parent: Node | None = parent

        self.arguments: NodeArguments = arguments or NodeArguments()
        self.info: NodeInfo = info or NodeInfo.empty()

    def set_parent(self, parent: Node) -> Node:
        # Set the parent of this node.
        self.parent = parent

        return self

    @property
    def template_type(self) -> str:
        # Return the type of this node
        # that should be used to find
        # templates.
        return self.type

    def accept(self, visitor: BaseVisitor, *args, **kwargs) -> dict:
        # Simple implementation of the visitor pattern.
        # Here, the node accepts a visitor and
        # calls one of the visitor's methods according
        # to the node content type.

        # Some node types contain a dot to allow templates
        # to be created in a hierarchy of directories
        # but dots are not allowed in function names
        method_name = f"_visit_{self.type.replace('-', '_')}"

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
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)

        self.value = value


class WrapperNode(Node, NodeContentMixin):
    type = "wrapper"

    def __init__(
        self,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
        content: Sequence[Node] | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeContentMixin.__init__(self, content)
