from mau.environment.environment import Environment
from mau.nodes.node import Node


class MauVisitorException(ValueError):
    def __init__(self, message: str, **kwargs):
        super().__init__(message)
        self.kwargs = kwargs


class BaseVisitor:
    format_code = "python"

    def __init__(self, environment: Environment, *args, **kwds):
        self.toc = None
        self.footnotes = None

        self.environment = environment

    def visit(self, node: Node | None, *args, **kwargs):
        # Simple implementation of the visitor pattern.
        # Here, the visitor passes itself to the node
        # through the method `accept`
        # The node calls a suitable method of the
        # visitor, and the result is returned here.
        #
        # All visitor functions return a dictionary with
        # the key "data" that contains the result of the visit.
        # This is done to provide space for metadata or other values
        # like templates used to render the node.

        if node is None:
            return {}

        return node.accept(self, *args, **kwargs)

    def visitlist(self, node, nodes, *args, **kwargs):
        # Visit all the nodes in the given sequence.
        return [self.visit(node, *args, **kwargs) for node in nodes]

    def _visit_default(self, node: Node, *args, **kwargs) -> dict:
        # This is the default code to visit a node.
        # It returns the node dictionary (as provided by
        # the node itself) and visits all children.

        # This is the dictionary of rendered children.
        rendered_children = {}
        for key, value in node.children.items():
            # Each entry in the children dictionary
            # is a list of nodes.
            rendered_children[key] = self.visitlist(node, value)

        # Get the dictionary version of the node.
        node_dict = node.asdict()

        # Add the rendered children.
        node_dict["children"] = rendered_children

        return node_dict
