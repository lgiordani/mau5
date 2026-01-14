# from __future__ import annotations

# from abc import ABC
# from typing import Generic, TypeVar

# from mau.text_buffer import Context


#
# class NodeInfo:
#     """A class to collect information about a
#     node, such as its context and arguments."""
#
#     def __init__(
#         self,
#         context: Context,
#         unnamed_args: list | None = None,
#         named_args: dict | None = None,
#         tags: list | None = None,
#         subtype: str | None = None,
#     ):
#         self.context = context
#         self.unnamed_args = unnamed_args or []
#         self.named_args = named_args or {}
#         self.tags = tags or []
#         self.subtype = subtype
#
#     @classmethod
#     def empty(cls) -> NodeInfo:
#         return NodeInfo(context=Context.empty())
#
#     def asdict(self):
#         return {
#             "context": self.context.asdict(),
#             "unnamed_args": self.unnamed_args,
#             "named_args": self.named_args,
#             "tags": self.tags,
#             "subtype": self.subtype,
#         }
#
#
# class NodeData(ABC):
#     type: str = "none"
#
#     def asdict(self):
#         return {"type": self.type, "custom": {}}
#
#
# # This is used to bind the type Node to the content type.
# Data_co = TypeVar("Data_co", bound=NodeData, covariant=True)
#
#
# class Node(Generic[Data_co]):
#     def __init__(
#         self,
#         data: Data_co | None = None,
#         parent: Node[NodeData] | None = None,
#         # children: MutableMapping[str, MutableSequence[Node[NodeData]]] | None = None,
#         info: NodeInfo | None = None,
#     ):
#         # If we provided no content just
#         # add an empty one.
#         self.data: NodeData = data or NodeData()
#
#         # Set the parent of this node.
#         self.parent: Node[NodeData] | None = parent
#
#         # # Initialise children as an empty list,
#         # # then set them using the method that
#         # # adds the current node as parent.
#         # self.children: MutableMapping[str, MutableSequence[Node[NodeData]]] = (
#         #     defaultdict(list)
#         # )
#         # if children:
#         #     self.add_children(children)
#
#         self.info: NodeInfo = info or NodeInfo.empty()
#
#         # # Get a copy of the class allowed_keys
#         # # in case we need to modify it for this
#         # # node only (dynamic children, e.g.
#         # # block groups).
#         # self.allowed_keys = {}
#         # self.allowed_keys.update(self.content.allowed_keys)
#
#     def set_parent(self, parent: Node) -> Node:
#         # Set the parent of this node.
#         self.parent = parent
#
#         return self
#
#     # def add_children_at_position(
#     #     self,
#     #     position,
#     #     children: MutableSequence[Node[NodeData]],
#     #     allow_all: bool = False,
#     # ):
#     #     # Add the children nodes to the list at the given position.
#     #     self.children[position].extend(children)
#
#     #     if allow_all:
#     #         # Allow this specific position.
#     #         self.allowed_keys[position] = "Dynamically added children"
#
#     #     # Add this node as parent of each element.
#     #     for child in children:
#     #         child.set_parent(self)
#
#     # def add_children(
#     #     self,
#     #     children: MutableMapping[str, MutableSequence[Node[NodeData]]],
#     #     allow_all: bool = False,
#     # ) -> Node:
#     #     # Add the given mapping of children to this node.
#     #     for position, elements in children.items():
#     #         self.add_children_at_position(position, elements, allow_all)
#
#     #     return self
#
#     # def check_children(self) -> set[str]:
#     #     # Check the existing children against
#     #     # the allowed keys and return the
#     #     # set of incorrect keys.
#
#     #     children_keys = set(self.children.keys())
#     #     allowed_keys = set(self.allowed_keys.keys())
#
#     #     if not children_keys.issubset(allowed_keys):
#     #         return children_keys - allowed_keys
#
#     #     return set()
#
#     def asdict(self):
#         return {
#             "data": self.data.asdict(),
#             "info": self.info.asdict(),
#         }
#
#     @property
#     def tags(self):
#         return self.info.tags
#
#     def __eq__(self, other):
#         if not isinstance(other, Node):
#             return False
#
#         return self.asdict() == other.asdict()
#
#     def __repr__(self):  # pragma: no cover
#         return str(self.asdict())
#
#
# class NodeDataContentMixin:
#     def __init__(
#         self,
#         content: list[Node] | None = None,
#     ):
#         self.content: list[Node] = content or []
#
#     def content_asdict(self, base: dict):
#         base["custom"]["content"] = [i.asdict() for i in self.content]
#
#
# class NodeDataLabelsMixin:
#     def __init__(
#         self,
#         labels: dict[str, list[Node]] | None = None,
#     ):
#         self.labels = labels or {}
#
#     def content_asdict(self, base: dict):
#         base["custom"]["labels"] = {
#             k: [i.asdict() for i in v] for k, v in self.labels.items()
#         }
#
#
# class ValueNodeData(NodeData):
#     type = "value"
#
#     def __init__(self, value: str):
#         self.value = value
#
#     def asdict(self):
#         base = super().asdict()
#         base["custom"] = {"value": self.value}
#
#         return base
#
#
# class WrapperNodeData(NodeData, NodeDataContentMixin):
#     type = "wrapper"
#
#     def __init__(self, content: list[Node] | None = None):
#         super().__init__()
#         NodeDataContentMixin.__init__(self, content)
#
#     def asdict(self):
#         base = super().asdict()
#         NodeDataContentMixin.content_asdict(self, base)
#
#         return base
#
#
# # def format_node(node: Node, indent: int = 0) -> str:  # pragma: no cover
# #     # Everything shuld be indented at
# #     # least at this level.
# #     prefix = " " * indent
#
# #     output_lines = []
#
# #     node_type = node.content.type.upper()
# #     output_lines.append(node_type)
#
# #     node_info = f"  INFO: {node.info.context}"
# #     output_lines.append(node_info)
#
# #     node_content = f"  CONTENT: {node.content.asdict()}"
# #     output_lines.append(node_content)
#
# #     node_children = "  CHILDREN:"
# #     output_lines.append(node_children)
#
# #     for key, children in node.children.items():
# #         output_lines.append(f"    [{key}]")
#
# #         for child in children:
# #             child_output = format_node(child, indent=indent + 6)
# #             output_lines.append(child_output)
#
# #     output_lines = [prefix + line for line in output_lines]
# #     return "\n".join(output_lines)
