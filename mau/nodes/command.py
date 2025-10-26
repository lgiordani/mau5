from mau.nodes.node import NodeContent

COMMAND_HELP = """
Syntax:

(. LABEL)*
([ARGS])?
::COMMAND(:ARGS)?

The command operator `::` runs the requested command passing the optional arguments.
"""


class TocNodeContent(NodeContent):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc"
    allowed_keys = {
        "nested_entries": "The ToC entries in a tree-like fashion.",
        "plain_entries": "The ToC entries in a plain list without nesting.",
    }


class TocItemNodeContent(NodeContent):
    """A Table of Contents command.

    This node contains the headers that go into the ToC.
    """

    type = "toc-item"
    allowed_keys = {
        "text": "The text of the header.",
        "entries": "The ToC entries nested under this entry.",
    }

    def __init__(
        self,
        level: int,
        internal_id: str,
    ):
        self.level = level
        self.internal_id = internal_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "internal_id": self.internal_id,
            }
        )

        return base


class FootnotesNodeContent(NodeContent):
    type = "footnotes"
    allowed_keys = {
        "entries": "All footnotes in order of appearance (mention).",
    }


class FootnotesItemNodeContent(NodeContent):
    """An entry of the list of footnotes."""

    type = "footnote"
    allowed_keys = {
        "content": "The content of the footnote.",
    }

    def __init__(
        self,
        # The unique internal name of the
        # referenced footnote content.
        name: str,
        # The visible ID assigned to this footnote
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


class BlockGroupNodeContent(NodeContent):
    type = "block-group"

    def __init__(
        self,
        name: str,
    ):
        self.name = name

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
            }
        )

        return base
