from mau.nodes.node import NodeContent


class TocNodeContent(NodeContent):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc"
    allowed_keys = {
        "nested_entries": "The ToC entries in a tree-like fashion.",
        "plain_entries": "The ToC entries in a plain list without nesting.",
    }
