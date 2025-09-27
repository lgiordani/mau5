from __future__ import annotations

from abc import ABC
from collections import defaultdict
from collections.abc import Iterable, MutableMapping
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

    def set_context(self, context: Context) -> NodeInfo:
        self.context = context

        return self

    def asdict(self):
        return {
            "context": self.context,
            "unnamed_args": self.unnamed_args,
            "named_args": self.named_args,
            "tags": self.tags,
            "subtype": self.subtype,
        }


class NodeContent(ABC):
    type: str = "none"

    # When a node contains content,
    # the node itself can have children.
    # Children are recorded in a dictionary
    # under a key that is the position of
    # the children in the parent.
    # Each node content allows only
    # certain positions, which are listed
    # in this dictionary as keys.
    # The value of each key is the description
    # of the position for self-documentation
    # purposes.
    allowed_keys: dict[str, str] = {}

    def asdict(self):
        return {"type": self.type}


Content_co = TypeVar("Content_co", bound=NodeContent, covariant=True)


class Node(Generic[Content_co]):
    def __init__(
        self,
        content: Content_co | None = None,
        parent: Node[NodeContent] | None = None,
        children: MutableMapping[str, Iterable[Node[NodeContent]]] | None = None,
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
        self.children: MutableMapping[str, Iterable[Node[NodeContent]]] = defaultdict(
            list
        )
        if children:
            self.add_children(children)

        self.info: NodeInfo = info or NodeInfo()

        # Get a copy of the class allowed_keys
        # in case we need to modify it for this
        # node only (dynamic children, e.g.
        # block groups).
        self.allowed_keys = {}
        self.allowed_keys.update(self.content.allowed_keys)

    def set_parent(self, parent: Node) -> Node:
        # Set the parent of this node.
        self.parent = parent

        return self

    def add_children_at_position(self, position, children: Iterable[Node[NodeContent]]):
        # Add the children nodes to the list at the given position.
        self.children[position].extend(children)

        # Add this node as parent of each element.
        for child in children:
            child.set_parent(self)

    def add_children(
        self, children: MutableMapping[str, Iterable[Node[NodeContent]]]
    ) -> Node:
        for position, elements in children.items():
            self.add_children_at_position(position, elements)

        return self

    def add_children_at_position_and_allow(
        self, position, children: Iterable[Node[NodeContent]]
    ):
        # Add the children nodes to the list at the given position.
        self.children[position].extend(children)

        # Allow this specific position.
        self.allowed_keys[position] = "Dynamic children"

        # Add this node as parent of each element.
        for child in children:
            child.set_parent(self)

    def check_children(self) -> set[str]:
        children_keys = set(self.children.keys())
        allowed_keys = set(self.allowed_keys.keys())

        if not children_keys.issubset(allowed_keys):
            return children_keys - allowed_keys

        return set()

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
