from mau.nodes.node import NodeContent


class BlockNodeContent(NodeContent):
    """A block.

    This node contains a generic block.

    Arguments:
        classes: a comma-separated list of classes
        engine: the engine used to render this block
        preprocessor: the preprocessor used for this block
    """

    type = "block"
    allowed_keys = {
        "content": "The text contained in this paragraph.",
        "title": "The title of the included content.",
    }

    def __init__(
        self,
        classes=None,
        engine=None,
        preprocessor=None,
    ):
        self.classes = classes or []
        self.engine = engine
        self.preprocessor = preprocessor

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "classes": self.classes,
                "engine": self.engine,
                "preprocessor": self.preprocessor,
            }
        )

        return base


# class BlockGroupNodeContent(NodeContent):
#     """This instructs Mau to insert a group of nodes."""

#     node_type = "block_group"

#     def __init__(
#         self,
#         group_name,
#         group,
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
#         self.title = title
#         self.group_name = group_name
#         self.group = group

#     def _custom_dict(self):
#         return {
#             "title": self.title,
#             "group_name": self.group_name,
#             "group": self.group,
#         }
