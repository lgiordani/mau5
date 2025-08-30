from __future__ import annotations

from abc import ABC

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
    ):
        self.position = position
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}
        # self.subtype = subtype
        # self.tags = tags or []
        self.context = context

    def set_position(self, position: str) -> NodeInfo:
        self.position = position

        return self

    def asdict(self):
        return {
            "position": self.position,
            "unnamed_args": self.unnamed_args,
            "named_args": self.named_args,
        }


class NodeContent(ABC):
    type = "none"

    def asdict(self):
        return {"type": self.type}


class Node:
    def __init__(
        self,
        content: NodeContent | None = None,
        parent: Node | None = None,
        children: list[Node] | None = None,
        info: NodeInfo | None = None,
    ):
        self.content: NodeContent = content or NodeContent()

        self.parent: Node | None = None
        if parent:
            self.set_parent(parent)

        self.children: list[Node] = []
        if children:
            self.set_children(children)

        self.info: NodeInfo = info or NodeInfo()

    #     self,
    #     parent=None,
    #     parent_position=None,
    #     children=None,
    #     subtype=None,
    #     args=None,
    #     kwargs=None,
    #     tags=None,
    #     context=None,
    # ):
    # self.parent = parent
    # self.parent_position = parent_position
    # self.subtype = subtype
    # self.children = children or []
    # self.args = args or []
    # self.kwargs = kwargs or {}
    # self.tags = tags or []
    # self.context = context

    def set_parent(self, parent: Node) -> Node:
        # Set the parent of this node.
        self.parent = parent

        return self

    def set_children(self, children: list[Node]) -> Node:
        # Set the children nodes.
        self.children = children

        # Add this node as parent of each of them.
        for child in children:
            child.parent = self

        return self

    def add_children(self, children: list[Node]) -> Node:
        # Add the children nodes to the list.
        self.children.extend(children)

        # Add this node as parent of each of them.
        for child in children:
            child.parent = self

        return self

    def asdict(self):
        return {
            # Parent is excluded to avoid
            # having to deal with recursion
            "children": [i.asdict() for i in self.children],
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
