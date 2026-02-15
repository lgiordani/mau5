from __future__ import annotations

from collections.abc import Mapping, Sequence

from mau.nodes.block import BlockNode
from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.node import (
    Node,
    NodeArguments,
    NodeContentMixin,
    NodeInfo,
    NodeLabelsMixin,
)

INCLUDE_HELP = """
Syntax:

([URI+, ARGS])?
(@CONTROL)?
(. LABEL)*
<< TYPE(:URI+, ARGS)?

The include operator `<<` includes content of type TYPE using the provided ARGS.
The ARGS must contain at least one unnamed URI.
"""

INCLUDE_IMAGE_HELP = """
Syntax:

([URI, ALT_TEXT, CLASSES, ARGS])?
(@CONTROL)?
(. LABEL)*
<< image(:URI, ALT_TEXT, CLASSES, ARGS)?

The include operator `<< image` includes an image using the provided URI.
"""

INCLUDE_MAU_HELP = """
Syntax:

([URI, ARGS])?
(@CONTROL)?
(. LABEL)*
<< mau(:URI, ARGS)?

The include operator `<< mau` includes an external Mau file image using the provided URI.
The file will be read and the content parsed and added to the parse tree of the document.
"""


class IncludeNode(Node, NodeLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include"
    long_help = INCLUDE_HELP

    def __init__(
        self,
        content_type: str,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.content_type = content_type

    @property
    def custom_attributes(self) -> list[str]:
        return [self.content_type]


class IncludeImageNode(Node, NodeLabelsMixin):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "include-image"
    long_help = INCLUDE_IMAGE_HELP

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        classes: Sequence[str] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.uri = uri
        self.alt_text = alt_text
        self.classes = classes or []


class IncludeMauNode(Node, NodeContentMixin, NodeLabelsMixin):
    """Mau content included in the page.

    This represents Mau content included
    in the page from an external file.
    """

    type = "include-mau"
    long_help = INCLUDE_MAU_HELP

    def __init__(
        self,
        uri: str,
        content: Sequence[Node] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeContentMixin.__init__(self, content)
        NodeLabelsMixin.__init__(self, labels)

        self.uri = uri


class FootnotesItemNode(Node):
    type = "footnotes-item"

    def __init__(
        self,
        footnote: FootnoteNode,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)

        self.footnote = footnote


class FootnotesNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "footnotes"

    def __init__(
        self,
        footnotes: Sequence[FootnotesItemNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.footnotes = footnotes or []


class TocItemNode(Node):
    """A Table of Contents.

    This node contains the headers that go into the ToC.
    """

    type = "toc-item"

    def __init__(
        self,
        header: HeaderNode,
        entries: Sequence[TocItemNode] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)

        self.header = header
        self.entries = entries or []


class TocNode(Node, NodeLabelsMixin):
    """The list of footnotes."""

    type = "toc"

    def __init__(
        self,
        plain_entries: Sequence[HeaderNode] | None = None,
        nested_entries: Sequence[TocItemNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.plain_entries = plain_entries or []
        self.nested_entries = nested_entries or []


class BlockGroupNode(Node, NodeLabelsMixin):
    type = "block-group"

    def __init__(
        self,
        name: str,
        blocks: Mapping[str, BlockNode] | None = None,
        labels: Mapping[str, Sequence[Node]] | None = None,
        parent: Node | None = None,
        arguments: NodeArguments | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, arguments=arguments, info=info)
        NodeLabelsMixin.__init__(self, labels)

        self.name = name
        self.blocks = blocks or {}
