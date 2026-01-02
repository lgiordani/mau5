from mau.nodes.node import NodeContent, ValueNodeContent

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


class MacroNodeContent(NodeContent):
    """This node contains a macro, with a name and arguments."""

    type = "macro"

    def __init__(
        self,
        name: str,
        unnamed_args: list[str] | None = None,
        named_args: dict[str, str] | None = None,
    ):
        self.name = name
        self.unnamed_args = unnamed_args or []
        self.named_args = named_args or {}

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
                "unnamed_args": self.unnamed_args,
                "named_args": self.named_args,
            }
        )

        return base


class MacroClassNodeContent(NodeContent):
    """Text with one or more classes."""

    type = "macro.class"
    allowed_keys = {"text": "The text that is marked with the given classes."}

    def __init__(self, classes: list[str]):
        self.classes = classes

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "classes": self.classes,
            }
        )

        return base


class MacroLinkNodeContent(ValueNodeContent):
    """This node contains a link."""

    type = "macro.link"
    value_key = "target"
    allowed_keys = {"text": "The text linked to the target."}


class MacroImageNodeContent(NodeContent):
    """This node contains an inline image."""

    type = "macro.image"

    def __init__(
        self,
        uri: str,
        alt_text: str | None = None,
        width: str | None = None,
        height: str | None = None,
    ):
        self.uri = uri
        self.alt_text = alt_text
        self.width = width
        self.height = height

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "uri": self.uri,
                "alt_text": self.alt_text,
                "width": self.width,
                "height": self.height,
            }
        )

        return base


class MacroHeaderNodeContent(NodeContent):
    """This node contains a link to a header node."""

    type = "macro.header"
    allowed_keys = {
        "text": "The text linked to the header.",
        "header": "The header node connected with this link.",
    }

    def __init__(
        self,
        target_alias: str,
        target_id: str | None = None,
    ):
        # This is the internal name of the
        # header that we are pointing to.
        self.target_alias = target_alias

        # This is the ID of the header that
        # we are pointing to.
        # It is an automatically generated
        # unique ID.
        self.target_id = target_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "target_alias": self.target_alias,
                "target_id": self.target_id,
            }
        )

        return base


class MacroFootnoteNodeContent(NodeContent):
    """This node contains a link to a footnote node."""

    type = "macro.footnote"
    allowed_keys = {
        "footnote": "The footnote node connected with this link.",
    }

    def __init__(
        self,
        # The unique internal name of the
        # referenced footnote content.
        name: str,
        # The public ID assigned to this footnote
        # (typically a progressive number).
        public_id: str | None = None,
        # The private unique ID assigned to this footnote
        # that can be used as reference (e.g. for links).
        private_id: str | None = None,
    ):
        self.name = name
        self.public_id = public_id
        self.private_id = private_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
                "public_id": self.public_id,
                "private_id": self.private_id,
            }
        )

        return base
