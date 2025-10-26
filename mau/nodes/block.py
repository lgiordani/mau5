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
