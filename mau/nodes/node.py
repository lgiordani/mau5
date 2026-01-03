from __future__ import annotations

from abc import ABC
from collections import defaultdict
from collections.abc import MutableMapping, MutableSequence
from typing import Generic, TypeVar

from mau.text_buffer import Context


class NodeContentError(ValueError):
    """This exception is used to signal that the node has been given
    content in the wrong form (e.g. a dictionary instead of a string,
    or a dictionary with a missing key)."""


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

    @property
    def custom_attributes(self) -> list[str]:
        return []

    def asdict(self):
        return {"type": self.type}


# This is used to bind the type Node to the content type.
Content_co = TypeVar("Content_co", bound=NodeContent, covariant=True)


class Node(Generic[Content_co]):
    def __init__(
        self,
        content: Content_co | None = None,
        parent: Node[NodeContent] | None = None,
        children: MutableMapping[str, MutableSequence[Node[NodeContent]]] | None = None,
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
        self.children: MutableMapping[str, MutableSequence[Node[NodeContent]]] = (
            defaultdict(list)
        )
        if children:
            self.add_children(children)

        self.info: NodeInfo = info or NodeInfo.empty()

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

    def add_children_at_position(
        self,
        position,
        children: MutableSequence[Node[NodeContent]],
        allow_all: bool = False,
    ):
        # Add the children nodes to the list at the given position.
        self.children[position].extend(children)

        if allow_all:
            # Allow this specific position.
            self.allowed_keys[position] = "Dynamically added children"

        # Add this node as parent of each element.
        for child in children:
            child.set_parent(self)

    def add_children(
        self,
        children: MutableMapping[str, MutableSequence[Node[NodeContent]]],
        allow_all: bool = False,
    ) -> Node:
        # Add the given mapping of children to this node.
        for position, elements in children.items():
            self.add_children_at_position(position, elements, allow_all)

        return self

    def check_children(self) -> set[str]:
        # Check the existing children against
        # the allowed keys and return the
        # set of incorrect keys.

        children_keys = set(self.children.keys())
        allowed_keys = set(self.allowed_keys.keys())

        if not children_keys.issubset(allowed_keys):
            return children_keys - allowed_keys

        return set()

    def asdict(self, recursive=False, include_children=False):
        children = {}

        if recursive:
            for key, value in self.children.items():
                children[key] = [i.asdict(recursive=True) for i in value]

        if not recursive and include_children:
            for key, value in self.children.items():
                children[key] = [i.asdict() for i in value]

        return {
            # Parent is excluded to avoid
            # having to deal with recursion
            "children": children,
            "content": self.content.asdict(),
            "info": self.info.asdict(),
        }

    @property
    def subtype(self):
        return self.info.subtype

    @property
    def tags(self):
        return self.info.tags

    def __eq__(self, other):
        if not isinstance(other, Node):
            return False

        return self.asdict() == other.asdict()

    def __repr__(self):  # pragma: no cover
        return str(self.asdict())


class ValueNodeContent(NodeContent):
    type = "value"
    value_key = "value"

    def __init__(self, value: str):
        self.value = value

    def asdict(self):
        base = super().asdict()
        base.update({self.value_key: self.value})

        return base


def format_node(node: Node, indent: int = 0) -> str:  # pragma: no cover
    # Everything shuld be indented at
    # least at this level.
    prefix = " " * indent

    output_lines = []

    node_type = node.content.type.upper()
    output_lines.append(node_type)

    node_info = f"  INFO: {node.info.context}"
    output_lines.append(node_info)

    node_content = f"  CONTENT: {node.content.asdict()}"
    output_lines.append(node_content)

    node_children = "  CHILDREN:"
    output_lines.append(node_children)

    for key, children in node.children.items():
        output_lines.append(f"    [{key}]")

        for child in children:
            child_output = format_node(child, indent=indent + 6)
            output_lines.append(child_output)

    output_lines = [prefix + line for line in output_lines]
    return "\n".join(output_lines)
