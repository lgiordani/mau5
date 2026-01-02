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
        "content": "The text contained in this block.",
        # TODO TODO TOODO
        # Why didn't this complain when I added the key "sections"?
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


class BlockSectionNodeContent(NodeContent):
    """A section.

    This node contains a section of a block.
    """

    type = "block-section"
    allowed_keys = {
        "content": "The text contained in this block.",
    }

    def __init__(
        self,
        name,
    ):
        self.name = name or []

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "name": self.name,
            }
        )

        return base
