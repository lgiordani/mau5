from mau.nodes.node import NodeContent


class FootnoteNodeContent(NodeContent):
    node_type = "footnote"

    # def __init__(
    #     self,
    #     number=None,
    #     reference_anchor=None,
    #     content_anchor=None,
    # ):
    #     super().__init__()
    #     self.number = number
    #     self.reference_anchor = reference_anchor
    #     self.content_anchor = content_anchor

    # def _custom_dict(self):
    #     return {
    #         "number": self.number,
    #         "reference_anchor": self.reference_anchor,
    #         "content_anchor": self.content_anchor,
    #     }

    # def to_entry(self):
    #     return FootnotesEntryNodeContent(
    #         number=self.number,
    #         reference_anchor=self.reference_anchor,
    #         content_anchor=self.content_anchor,
    #         parent=self.parent,
    #         parent_position=self.parent_position,
    #         children=self.children,
    #         subtype=self.subtype,
    #         args=self.args,
    #         kwargs=self.kwargs,
    #         tags=self.tags,
    #         context=self.context,
    #     )


class MacroFootnoteNodeContent(FootnoteNodeContent):
    """A footnote created inside a piece of text."""

    node_type = "footnote"


class FootnotesEntryNodeContent(FootnoteNodeContent):
    """An entry of the list of footnotes."""

    node_type = "footnotes_entry"


class FootnotesNodeContent(NodeContent):
    """This instructs Mau to insert the list of footnotes."""

    node_type = "footnotes"
