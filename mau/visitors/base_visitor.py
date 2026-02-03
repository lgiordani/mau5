from collections.abc import Mapping, Sequence

from mau.environment.environment import Environment
from mau.error import MauError, MauErrorType, MauException
from mau.nodes.node import Node
from mau.text_buffer import adjust_context, adjust_context_dict


def create_visitor_exception(
    message: str,
    node: Node | None = None,
    data: dict | None = None,
    environment: Environment | None = None,
    additional_info: dict[str, str] | None = None,
):
    context = "unknown"
    if data:
        data_context = data["_info"]["context"]
        context = adjust_context_dict(data_context)
    elif node:
        context = adjust_context(node.info.context)

    content = {
        "Context": context,
    }

    if node:
        content["Node type"] = node.type

    if data:
        content["Template data"] = data

    if additional_info:
        content.update(additional_info)

    error = MauError(type=MauErrorType.VISITOR, content=content)

    return MauException(message, error)


class BaseVisitor:
    # The output format that identifies this visitor.
    format_code = "python"

    def __init__(self, environment: Environment = Environment()):
        self.toc = None
        self.footnotes = None

        self.environment = environment

    def process(self, node: Node | None, *args, **kwargs):
        # This is a wrapper around the method visit
        # that allows the visitor to preprocess
        # the input data and postprocess the output.

        # Preprocess the input node.
        node = self.preprocess(node, *args, **kwargs)

        # Visit the node.
        result = self.visit(node, *args, **kwargs)

        # Postprocess the result.
        result = self.postprocess(result, *args, **kwargs)

        return result

    def preprocess(self, node: Node | None, *args, **kwargs):
        return node

    def postprocess(self, result, *args, **kwargs):
        return result

    def visit(self, node: Node | None, *args, **kwargs):
        # Simple implementation of the visitor pattern.
        # Here, the visitor passes itself to the node
        # through the method `accept`
        # The node calls a suitable method of the
        # visitor, and the result is returned here.
        #
        # All visitor functions return a dictionary with
        # the key "data" that contains the result of the visit.
        # This is done to provide space for metadata or other values
        # like templates used to render the node.

        if node is None:
            return {}

        result = node.accept(self, *args, **kwargs)

        if transformer := kwargs.get("transformer"):
            result = transformer(result)

        return result

    def visitlist(
        self, current_node: Node, nodes_list: Sequence[Node], *args, **kwargs
    ):
        # Visit all the nodes in the given sequence.
        return [self.visit(node, *args, **kwargs) for node in nodes_list]

    def visitdict(
        self, current_node: Node, nodes_dict: Mapping[str, Node], *args, **kwargs
    ):
        # Visit all the nodes in the given dictionary.
        return {k: self.visit(node, *args, **kwargs) for k, node in nodes_dict.items()}

    def visitdictlist(
        self,
        current_node: Node,
        nodes_dict: Mapping[str, Sequence[Node]],
        *args,
        **kwargs,
    ):
        # Visit all the nodes in the given dictionary.
        return {
            k: self.visitlist(current_node, nodes, *args, **kwargs)
            for k, nodes in nodes_dict.items()
        }

    def _add_visit_content(self, result: dict, node: Node, *args, **kwargs):
        result.update(
            {
                "content": self.visitlist(node, node.content, *args, **kwargs),
            }
        )

    def _add_visit_labels(self, result: dict, node: Node, *args, **kwargs):
        result.update(
            {
                "labels": self.visitdictlist(node, node.labels, *args, **kwargs),
            }
        )

    def _get_node_data(self, node: Node, *args, **kwargs) -> dict:
        if not node:
            return {}

        return {
            "_type": node.type,
            "_context": node.info.context.asdict(),
            "unnamed_args": node.info.unnamed_args,
            "named_args": node.info.named_args,
            "tags": node.info.tags,
            "subtype": node.info.subtype,
        }

    def _visit_default(self, node: Node, *args, **kwargs) -> dict:
        # This is the default code to visit a node.

        data = self._get_node_data(node)
        data["parent"] = self._get_node_data(node)

        return data

    def _visit_value(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "value": node.value,
            }
        )

        return result

    def _visit_text(self, node: Node, *args, **kwargs) -> dict:
        return self._visit_value(node, *args, **kwargs)

    def _visit_verbatim(self, node: Node, *args, **kwargs) -> dict:
        return self._visit_value(node, *args, **kwargs)

    def _visit_word(self, node: Node, *args, **kwargs) -> dict:
        return self._visit_value(node, *args, **kwargs)

    def _visit_style(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "style": node.style,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _get_header_data(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "level": node.level,
                "internal_id": node.internal_id,
                "name": node.name,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_header(self, node: Node, *args, **kwargs) -> dict:
        return self._get_header_data(node, *args, **kwargs)

    def _visit_macro(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "name": node.name,
                "unnamed_args": node.unnamed_args,
                "named_args": node.named_args,
            }
        )

        return result

    def _visit_macro__class(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "classes": node.classes,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _visit_macro__link(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "target": node.target,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _visit_macro__unicode(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "value": node.value,
            }
        )

        return result

    def _visit_macro__raw(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "value": node.value,
            }
        )

        return result

    def _visit_macro__image(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "uri": node.uri,
                "alt_text": node.alt_text,
                "width": node.width,
                "height": node.height,
            }
        )

        return result

    def _visit_macro__header(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        header_data = (
            self._get_header_data(node.header, *args, **kwargs) if node.header else {}
        )

        result.update(
            {
                "target_name": node.target_name,
                "header": header_data,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _get_footnote_data(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "name": node.name,
                "public_id": node.public_id,
                "internal_id": node.internal_id,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _visit_macro__footnote(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        footnote_data = (
            self._get_footnote_data(node.footnote, *args, **kwargs)
            if node.footnote
            else None
        )

        result.update(
            {
                "footnote": footnote_data,
            }
        )

        return result

    def _visit_footnotes_item(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "footnote": self._get_footnote_data(node.footnote, *args, **kwargs),
            }
        )

        return result

    def _visit_footnotes(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "footnotes": self.visitlist(node, node.footnotes, *args, **kwargs),
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_toc_item(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "header": self.visit(node.header, *args, **kwargs),
                "entries": self.visitlist(node, node.entries, *args, **kwargs),
            }
        )

        return result

    def _visit_toc(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "plain_entries": self.visitlist(
                    node, node.plain_entries, *args, **kwargs
                ),
                "nested_entries": self.visitlist(
                    node, node.nested_entries, *args, **kwargs
                ),
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_block_group(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "name": node.name,
                "blocks": self.visitdict(node, node.blocks, *args, **kwargs),
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_command(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "name": node.name,
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_block(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "classes": node.classes,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_horizontal_rule(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_document(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _visit_include(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "content_type": node.content_type,
                "uris": node.uris,
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_include_image(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "uri": node.uri,
                "alt_text": node.alt_text,
                "classes": node.classes,
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_include_mau(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "uri": node.uri,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_list_item(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "level": node.level,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)

        return result

    def _visit_list(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "ordered": node.ordered,
                "main_node": node.main_node,
                "start": node.start,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_paragraph(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "lines": self.visitlist(node, node.lines, *args, **kwargs),
            }
        )

        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_paragraph_line(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_source_marker(self, node: Node, *args, **kwargs) -> dict:
        return self._visit_value(node, *args, **kwargs)

    def _visit_source_line(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "line_number": node.line_number,
                "line_content": node.line_content,
                "highlight_style": node.highlight_style,
                "marker": self.visit(node.marker, *args, **kwargs),
            }
        )

        return result

    def _visit_source(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)
        result.update(
            {
                "language": node.language,
                "classes": node.classes,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result

    def _visit_raw_line(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "value": node.value,
            }
        )

        return result

    def _visit_raw(self, node: Node, *args, **kwargs) -> dict:
        result = self._visit_default(node, *args, **kwargs)

        result.update(
            {
                "classes": node.classes,
            }
        )

        self._add_visit_content(result, node, *args, **kwargs)
        self._add_visit_labels(result, node, *args, **kwargs)

        return result
