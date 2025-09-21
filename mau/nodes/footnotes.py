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
        # The unique id of that will be assigned
        # to the footnote and will be rendered.
        _id: str | None = None,
    ):
        self.name = name
        self.id = _id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
                "id": self.id,
            }
        )

        return base


# class FootnotesNodeContent(NodeContent):
#     type = "footnotes"
#     allowed_keys = {
#         # TODO shall we implement a check of the types in children?
#         "entries": "The list of all footnotes.",
#     }
