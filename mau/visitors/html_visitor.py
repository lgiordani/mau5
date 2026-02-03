import html
from importlib.resources import files
from typing import Callable

from bs4 import BeautifulSoup
from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from mau.environment.environment import Environment
from mau.nodes.node import Node
from mau.visitors.jinja_visitor import JinjaVisitor, load_templates_from_path


# This removes trailing spaces and newlines from
# HTML templates. This allows to save them in a
# pretty format without passing unnecessary
# spaces and indentations to the template engine.
def filter_html(text):
    dedent = [i.lstrip() for i in text.split("\n")]
    dedent = [i for i in dedent if i != ""]
    return "".join(dedent)


templates = load_templates_from_path(
    str(files(__package__).joinpath("templates/html")), filter_html
)


class HtmlVisitor(JinjaVisitor):
    format_code = "html"
    extension = "html"
    templates_preprocess: Callable[[str], str] | None = filter_html

    default_templates = Environment.from_dict(templates)

    def postprocess(self, result, *args, **kwargs):
        # Check if the visitor settings enable
        # postprocessing of the resulting HTML.
        if not self.environment.get("mau.visitor.html.pretty", False):
            return result

        # The result is HTML code, let's
        # make it nice to read.
        soup = BeautifulSoup(result, "html.parser")
        pretty = soup.prettify()

        return pretty

    def _visit_text(self, node: Node, *args, **kwargs) -> dict:
        result = super()._visit_text(node, *args, **kwargs)

        result["value"] = html.escape(result["value"])

        return result

    def _visit_verbatim(self, node: Node, *args, **kwargs) -> dict:
        result = super()._visit_verbatim(node, *args, **kwargs)

        result["value"] = html.escape(result["value"])

        return result

    def _visit_source(self, node: Node, *args, **kwargs) -> dict:
        # Collect all markers and remove them
        # from the source code.
        all_markers = []
        for line in node.content:
            # Save the marker.
            all_markers.append(line.marker)

            # Remove the marker.
            line.marker = None

        highlight_default = [
            line.line_number
            for line in node.content
            if line.highlight_style == "default"
        ]

        # Render the code without markers.
        code = self.visitlist(node, node.content, *args, **kwargs)

        # Find the highlighter set in the environment.
        highlighter_name = self.environment.get(
            "mau.visitor.html.highlighter", "pygments"
        )

        # Override the globally set highlighter if
        # this specific block has a different one.
        highlighter = node.info.named_args.pop("highlighter", highlighter_name)

        if highlighter == "pygments":
            # The Pygments lexer for the given language.
            lexer = get_lexer_by_name(node.language)

            # Fetch global configuration for Pygments.
            formatter_config = self.environment.get(
                "mau.visitor.html.pygments", Environment.from_dict({"nowrap": True})
            ).asdict()

            # Find all the attributes of this specific block
            # that start with `pygments.`, remove the
            # prefix, and store them in a dictionary.
            node_pygments_config = {
                k.replace("pygments.", ""): v
                for k, v in node.info.named_args.items()
                if k.startswith("pygments.")
            }

            # The attribute `hl_lines` is a list of comma-separated
            # line numbers that must be converted into a list (if
            # present) before we pass it to pygments.
            hl_lines = node_pygments_config.get("hl_lines", "")
            hl_lines = [i for i in hl_lines.split(",") if i != ""]

            # Merge the requested lines with the highlighted lines.
            hl_lines = list(set(hl_lines) | set(highlight_default))

            # Tell Pygments which lines we want to highlight.
            formatter_config["hl_lines"] = hl_lines

            # Create the formatter and pass the config.
            formatter = get_formatter_by_name("html", **formatter_config)

            # Highlight the source with Pygments
            highlighted_src = highlight(code, lexer, formatter)

        # Split highlighted code again into lines.
        highlighted_lines = highlighted_src.split("\n")

        # This is a list of tuples (node, highlighted_code, marker)
        # for each node in the original content.
        tmp_content_tuples = list(zip(node.content, highlighted_lines, all_markers))

        # Put everything together.
        for line_node, code, marker in tmp_content_tuples:
            line_node.line_content = code
            line_node.marker = marker

        result = super()._visit_source(node, *args, **kwargs)

        return result
