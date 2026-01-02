from mau.nodes.node import NodeContent

HEADER_HELP = """
Syntax:

([ARGS])?
(@CONTROL)?
(=)+ HEADER

The header prefix `=` can be repeated multiple times to create a
header on a deeper level.
"""


class HeaderNodeContent(NodeContent):
    """A header."""

    type = "header"
    allowed_keys = {
        "text": "The text of the header.",
    }

    def __init__(
        self,
        level: int,
        internal_id: str | None = None,
        alias: str | None = None,
    ):
        self.level = level
        self.internal_id = internal_id

        # This is an alias for this header,
        # used to link it internally.
        # Headers with an alias will still
        # receive a programmatic ID.
        self.alias = alias

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "internal_id": self.internal_id,
                "alias": self.alias,
            }
        )

        return base
