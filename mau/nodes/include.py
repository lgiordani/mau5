from mau.nodes.node import NodeContent


class IncludeNodeContent(NodeContent):
    """Content included in the page.

    This represents generic content included in the page.
    """

    type = "content"
    allowed_keys = ["title"]

    def __init__(
        self,
        content_type: str,
        uris: list[str],
    ):
        self.content_type = content_type
        self.uris = uris

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "content_type": self.content_type,
                "uris": self.uris,
            }
        )

        return base


# class ContentImageNode(Node):
#     """An image included in the page."""

#     node_type = "content_image"

#     def __init__(
#         self,
#         uri,
#         alt_text=None,
#         classes=None,
#         title=None,
#         parent=None,
#         parent_position=None,
#         children=None,
#         subtype=None,
#         args=None,
#         kwargs=None,
#         tags=None,
#         context=None,
#     ):
#         super().__init__(
#             parent=parent,
#             parent_position=parent_position,
#             children=children,
#             subtype=subtype,
#             args=args,
#             kwargs=kwargs,
#             tags=tags,
#             context=context,
#         )
#         self.uri = uri
#         self.title = title
#         self.alt_text = alt_text
#         self.classes = classes

#     def _custom_dict(self):
#         return {
#             "uri": self.uri,
#             "title": self.title,
#             "alt_text": self.alt_text,
#             "classes": self.classes,
#         }
