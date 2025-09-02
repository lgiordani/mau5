from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from mau.text_buffer.context import Context


class NodeContentError(ValueError):
    """This exception is used to signal that the node has been given
    content in the wrong form (e.g. a dictionary instead of a string,
    or a dictionary with a missing key)."""


class NodeInfo:
    def __init__(
        self,
        context: Context | None = None,
        position: str | None = None,
        unnamed_args: list | None = None,
        named_args: dict | None = None,
        tags: list | None = None,
        subtype: str | None = None,
    ):
        self.context = context
        self.position = position
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}
        self.tags = tags or []
        self.subtype = subtype

    def set_position(self, position: str) -> NodeInfo:
        self.position = position

        return self

    def set_context(self, context: Context) -> NodeInfo:
        self.context = context

        return self

    def set_attributes(
        self,
        unnamed_args: list | None = None,
        named_args: dict | None = None,
        tags: list | None = None,
        subtype: str | None = None,
    ) -> NodeInfo:
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}
        self.tags = tags or []
        self.subtype = subtype

        return self

    def asdict(self):
        return {
            "context": self.context,
            "position": self.position,
            "unnamed_args": self.unnamed_args,
            "named_args": self.named_args,
        }


class NodeContent(ABC):
    type = "none"

    def asdict(self):
        return {"type": self.type}


Content_co = TypeVar("Content_co", bound=NodeContent, covariant=True)


class Node(Generic[Content_co]):
    def __init__(
        self,
        content: Content_co | None = None,
        parent: Node[NodeContent] | None = None,
        children: dict[str, list[Node[NodeContent]]] | None = None,
        info: NodeInfo | None = None,
    ):
        # If we provided no content just
        # add an empty one.
        self.content: NodeContent = content or NodeContent()

        # Set the parent of this node.
        self.parent: Node[NodeContent] | None = parent

        # Initialise children as an empty list,
        # then set them using the method that
        # adds the current node as parent.
        self.children: dict[str, list[Node[NodeContent]]] = {}
        if children:
            self.set_children(children)

        self.info: NodeInfo = info or NodeInfo()

    def set_parent(self, parent: Node) -> Node:
        # Set the parent of this node.
        self.parent = parent

        return self

    def set_children(self, children: dict[str, list[Node[NodeContent]]]) -> Node:
        # Set the children nodes.
        self.children = children

        # Add this node as parent of each of them.
        for value in children.values():
            for child in value:
                child.set_parent(self)

        return self

    def add_children(self, children: dict[str, list[Node[NodeContent]]]) -> Node:
        # Add the children nodes to the list.
        self.children.update(children)

        # Add this node as parent of each of them.
        for value in children.values():
            for child in value:
                child.set_parent(self)

        return self

    def asdict(self):
        children = {}
        for key, value in self.children.items():
            children[key] = [i.asdict() for i in value]

        return {
            # Parent is excluded to avoid
            # having to deal with recursion
            "children": children,
            "content": self.content.asdict(),
            "info": self.info.asdict(),
        }

    # def accept(self, visitor, *args, **kwargs):
    #     # Some node types contain a dot to allow templates
    #     # to be created in a hierarchy of directories
    #     # but dots are not allowed in function names
    #     method_name = f"_visit_{self.node_type.replace('.', '__')}"

    #     try:
    #         method = getattr(visitor, method_name)
    #     except AttributeError:
    #         method = getattr(visitor, "_visit_default")

    #     return method(self, *args, **kwargs)

    def __eq__(self, other):
        try:
            return self.asdict() == other.asdict()
        except AttributeError:  # pragma: no cover
            return False

    def __repr__(self):  # pragma: no cover
        return str(self.asdict())

    # def hash(self):  # pragma: no cover
    #     return hashlib.md5(str(self).encode("utf-8")).hexdigest()[:8]


class ValueNodeContent(NodeContent):
    type = "value"
    value_key = "value"

    def __init__(self, value: str):
        self.value = value

    def asdict(self):
        base = super().asdict()
        base.update({self.value_key: self.value})

        return base
