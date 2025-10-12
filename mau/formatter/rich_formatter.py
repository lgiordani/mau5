from .base_formatter import BaseFormatter
from mau.token import Token

from rich.console import Console
from rich.table import Table

console = Console()


class RichFormatter(BaseFormatter):
    type = "rich"

    @classmethod
    def print_tokens(cls, tokens: list[Token]):
        table = Table(title="Tokens", show_lines=True)
        table.add_column("Type", style="cyan", justify="left")
        table.add_column("Value", style="green", justify="left")
        table.add_column("Context", style="orange1", justify="left")

        for token in tokens:
            table.add_row(token.type.value, token.value, str(token.context))

        console.print(table)
