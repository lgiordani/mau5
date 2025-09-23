from mau.nodes.node import NodeContent


# TODO tests for this class
class FootnoteNodeContent(NodeContent):
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


# TODO find a decent name for this and for the ToC node.
# They should be similar, as both contain the result of a command,
# and ultimately a list of elements collected in the text.
class FootnotesListNodeContent(NodeContent):
    type = "footnotes-list"
    allowed_keys = {
        "entries": "All footnotes in order of appearance (mention).",
    }
