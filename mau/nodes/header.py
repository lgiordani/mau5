from collections.abc import Mapping, Sequence

from mau.nodes.node import (
    Node,
    NodeArguments,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
)

HEADER_HELP = """
Syntax:

([ARGS])?
(@CONTROL)?
(=)+ HEADER

The header prefix `=` can be repeated multiple times to create a
header on a deeper level.
"""


class HeaderNode(Node, NodeLabelsMixin, NodeContentMixin):
    """A header."""

    type = "header"

    def __init__(
        self,
        level: int,
        # The internal unique ID assigned to this footnote
        # that can be used to create references in
        # the rendered text.
        internal_id: str | None = None,
        # The unique internal name of the
        # referenced footnote content.
        # This name is used to link a
        # header macro (mention) with its
        # header (definition).
        name: str | None = None,
        content: list[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        source_text: str | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        self.level = level
        self.internal_id = internal_id

        # This is a name for this header,
        # used to link it internally.
        # Headers with an name will still
        # receive a programmatic ID.
        # TODO clarify and use correct names.
        self.name = name

        # The source text of the header.
        # This is the unparsed text
        # that will be used to generate
        # the unique id.
        self.source_text = source_text

        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)
