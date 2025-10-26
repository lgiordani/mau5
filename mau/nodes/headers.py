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
        external_id: str | None = None,
    ):
        self.level = level
        self.internal_id = internal_id
        self.external_id = external_id

    def asdict(self):
        base = super().asdict()
        base.update(
            {
                "level": self.level,
                "internal_id": self.internal_id,
                "external_id": self.external_id,
            }
        )

        return base
