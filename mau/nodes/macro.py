from collections.abc import Mapping, Sequence

from mau.nodes.footnote import FootnoteNode
from mau.nodes.header import HeaderNode
from mau.nodes.node import Node, NodeContentMixin, NodeInfo, ValueNode

MACRO_HELP = """
Syntax:

[NAME](ARGS)

A generic macro named NAME that contains the given ARGS.
"""

MACRO_CLASS_HELP = """
Syntax:

[class](class1, class2, ...)

A macro to assign classes to text.
"""

MACRO_LINK_HELP = """
Syntax:

[link](target[, text])

A macro that creates a link. The text of the link is the target itself
unless the option `text` is gien a value.
"""

MACRO_IMAGE_HELP = """
Syntax:

[image](uri[, alt_text, width, height])

A macro that inserts an image. The macro requires the `uri` and
accepts optional `alt_text`, `width`, and `height`.
"""

MACRO_HEADER_HELP = """
Syntax:

[header](header_alias)

A macro that inserts a link to a header. The macro requires
the header exernal ID as a parameter.
"""

MACRO_FOOTNOTE_HELP = """
Syntax:

[footnote](footnote_name)

A macro that inserts a link to a footnote. The macro requires
the footnote name associated with the relative data block.
"""


class MacroNode(Node):
    """This node contains a macro, with a name and arguments."""

    type = "macro"

    def __init__(
        self,
        name: str,
        unnamed_args: Sequence[str] | None = None,
        named_args: Mapping[str, str] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.name = name
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}

    @property
    def custom_attributes(self) -> list[str]:
        return [self.name]


class MacroClassNode(Node, NodeContentMixin):
    """Text with one or more classes."""

    type = "macro.class"

    def __init__(
        self,
        classes: Sequence[str],
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)
        self.classes = classes
        NodeContentMixin.__init__(self, content)


class MacroLinkNode(Node, NodeContentMixin):
    """This node contains a link."""

    type = "macro.link"

    def __init__(
        self,
        target: str,
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.target = target
        NodeContentMixin.__init__(self, content)


class MacroImageNode(Node):
    """This node contains an inline image."""

    type = "macro.image"

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        width: str | None = None,
        height: str | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.uri = uri
        self.alt_text = alt_text
        self.width = width
        self.height = height


class MacroHeaderNode(Node, NodeContentMixin):
    """This node contains a link to a header node."""

    type = "macro.header"

    def __init__(
        self,
        target_name: str,
        header: HeaderNode | None = None,
        content: Sequence[Node] | None = None,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        # This is the internal name of the
        # header that we are pointing to.
        self.target_name = target_name

        # The header linked by this macro.
        self.header = header

        NodeContentMixin.__init__(self, content)


class MacroFootnoteNode(Node):
    """This node contains a link to a footnote node."""

    type = "macro.footnote"

    def __init__(
        self,
        footnote: FootnoteNode,
        parent: Node | None = None,
        info: NodeInfo | None = None,
    ):
        super().__init__(parent=parent, info=info)

        self.footnote = footnote


class MacroUnicodeNode(ValueNode):
    """This node contains a unicode code point."""

    type = "macro.unicode"


class MacroRawNode(ValueNode):
    """This node contains a unicode code point."""

    type = "macro.raw"
