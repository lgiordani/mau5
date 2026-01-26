import itertools
import sys
from collections.abc import Sequence
from pathlib import Path
from typing import Callable

import jinja2

from mau.environment.environment import Environment
from mau.nodes.node import Node
from mau.visitors.base_visitor import BaseVisitor, MauVisitorException


class TemplateNotFound(ValueError):
    pass


# def dedent(text):
#     return textwrap.dedent(text).strip()


class MissingTemplateException(MauVisitorException):
    def __init__(
        self,
        node: Node,
        data: dict,
        environment: Environment,
        templates: list[str],
    ):
        message = "Cannot find a suitable template."
        additional_info = f"Accepted teplates: {templates}"

        super().__init__(message, node, data, environment, additional_info)


def _create_templates(
    node_type: str,
    extension: str | None = None,
    node_subtype: str | None = None,
    node_tags: list[str] | None = None,
    custom_attributes: list[str] | None = None,
    global_prefixes: list[str] | None = None,
    parent_prefix: str | None = None,
):
    # Given the following parameters
    #
    # prefix* - Custom prefixes
    # pprefix - The prefix of the parent
    # type    - The node type
    # stype   - The node subtype
    # custom* - Custom attributes
    #
    # we want to build the following list
    #
    # ${PREFIX}.pprefix.type.stype.custom1.custom2.custom3.ext
    # ${PREFIX}.pprefix.type.stype.custom1.custom2.ext
    # ${PREFIX}.pprefix.type.stype.custom1.custom3.ext
    # ${PREFIX}.pprefix.type.stype.custom2.custom3.ext
    # ${PREFIX}.pprefix.type.stype.custom1.ext
    # ${PREFIX}.pprefix.type.stype.custom2.ext
    # ${PREFIX}.pprefix.type.stype.custom3.ext
    # ${PREFIX}.pprefix.type.stype.ext
    # ${PREFIX}.pprefix.type.custom1.custom2.custom3.ext
    # ${PREFIX}.pprefix.type.custom1.custom2.ext
    # ${PREFIX}.pprefix.type.custom1.custom3.ext
    # ${PREFIX}.pprefix.type.custom2.custom3.ext
    # ${PREFIX}.pprefix.type.custom1.ext
    # ${PREFIX}.pprefix.type.custom2.ext
    # ${PREFIX}.pprefix.type.custom3.ext
    # ${PREFIX}.pprefix.type.ext
    # ${PREFIX}.type.stype.custom1.custom2.custom3.ext
    # ${PREFIX}.type.stype.custom1.custom2.ext
    # ${PREFIX}.type.stype.custom1.custom3.ext
    # ${PREFIX}.type.stype.custom2.custom3.ext
    # ${PREFIX}.type.stype.custom1.ext
    # ${PREFIX}.type.stype.custom2.ext
    # ${PREFIX}.type.stype.custom3.ext
    # ${PREFIX}.type.stype.ext
    # ${PREFIX}.type.custom1.custom2.custom3.ext
    # ${PREFIX}.type.custom1.custom2.ext
    # ${PREFIX}.type.custom1.custom3.ext
    # ${PREFIX}.type.custom2.custom3.ext
    # ${PREFIX}.type.custom1.ext
    # ${PREFIX}.type.custom2.ext
    # ${PREFIX}.type.custom3.ext
    # ${PREFIX}.type.ext
    #
    # For each PREFIX in prefix*, including
    # the empty prefix.

    node_tags = node_tags or []
    custom_attributes = custom_attributes or []
    global_prefixes = global_prefixes or []

    ####################################
    # Global prefixes

    # This will be
    # ["prefix1.", "prefix2.", ..., "prefixN.", ""]
    global_prefixes_list = [f"{prefix}." for prefix in global_prefixes]

    # Add the empty prefix.
    global_prefixes_list.append("")

    ####################################
    # Parent prefixes

    # Calculate the parent prefixes.
    parent_prefixes_list = []

    # If there is a parent prefix add it.
    if parent_prefix:
        parent_prefixes_list.append(f"{parent_prefix}.")

    # Add the empty parent prefix.
    parent_prefixes_list.append("")

    ####################################
    # Node components

    # This will be
    # ["type.stype.", "type."]
    node_components_list = []

    # If there is a subtype add "type.stype.".
    if node_subtype:
        node_components_list.append(f"{node_type}.{node_subtype}")

    # Add "type.".
    node_components_list.append(f"{node_type}")

    ####################################
    # Node tags

    # This will be
    # ["#tag1", "#tag2", ""]
    node_tags_list = [f"#{tag}" for tag in node_tags]

    # Add the empty suffix.
    node_tags_list.append("")

    ####################################
    # Custom attributes

    # Calculate all custom suffixes.
    # This generates out of A,B,C
    # [
    #   ".A.B.C",
    #   ".A.B",
    #   ".A.C",
    #   ".B.C",
    #   ".A",
    #   ".B",
    #   ".C",
    # ]
    custom_suffixes_list = [
        "." + ".".join(c)
        for r in range(len(custom_attributes), 0, -1)
        for c in itertools.combinations(custom_attributes, r)
    ]

    # Add the empty suffix.
    custom_suffixes_list.append("")

    ####################################
    # All templates

    # Put everything together.
    templates = [
        f"{global_prefix}{parent_prefix}{node_component}{custom_suffix}{node_tag}"
        for global_prefix in global_prefixes_list
        for parent_prefix in parent_prefixes_list
        for node_component in node_components_list
        for custom_suffix in custom_suffixes_list
        for node_tag in node_tags_list
    ]

    # Add the extension if present.
    if extension:
        templates = [f"{template}.{extension}" for template in templates]

    return templates


def _load_template_prefixes(environment: Environment) -> list[str]:
    # Load all the template prefixes that
    # have been configured for this execution.
    return environment.get("mau.visitor.templates.prefixes", [])


def _load_available_template_providers():  # pragma: no cover
    # Load all the template providers belonging
    # to the group "mau.templates".

    if sys.version_info < (3, 10):
        from importlib_metadata import entry_points
    else:
        from importlib.metadata import entry_points

    discovered_plugins = entry_points(group="mau.templates")

    # Load the available plugins
    return {i.name: i.load() for i in discovered_plugins}


def _load_templates_from_providers(environment: Environment) -> Environment:
    # Find all the template providers that
    # have been configured for this execution.
    requested_providers = environment.get("mau.visitor.templates.providers", [])

    # If we didn't request any template provider we can skip this.
    if not requested_providers:
        return Environment()

    # The environment that collects the loaded templates.
    templates = Environment()

    # Load available template provider plugins.
    available_providers = _load_available_template_providers()

    # Load requested providers.
    for provider in requested_providers:
        # Check if the provider is available.
        if provider not in available_providers:
            raise MauVisitorException(f"Template provider {provider} is not available")

        templates.dupdate(available_providers[provider].templates)

    return templates


def _load_templates_from_path(
    path_str: str | None,
    preprocess: Callable[[str], str] | None = None,
) -> dict[str, dict | str]:  # pragma: no cover
    # Recursively loads templates from the given path
    # and all its subpaths.

    # If the path string is empty just stop.
    if not path_str:
        return {}

    # The final dictionary of templates.
    result: dict[str, dict | str] = {}

    # Transform the path string into a Path.
    templates_path = Path(path_str)

    # If the path is not absolute, find the relative
    # version and make it absolute.
    if not templates_path.is_absolute():
        templates_path = templates_path.relative_to(Path.cwd())
        templates_path = Path.cwd() / Path(templates_path)

    # Set up the preprocess function.
    # If no preprocess function is given we can
    # use the identity function.
    preprocess = preprocess or (lambda x: x)

    # Scan all directories in the given path.
    for obj in templates_path.iterdir():
        # If we found a file, read the content,
        # preprocess and store it.
        # Otherwise it's a directory,
        # recursively load templates from there.
        if obj.is_file():
            result[obj.name] = preprocess(obj.read_text())
        else:
            result[obj.name] = _load_templates_from_path(
                obj.as_posix(), preprocess=preprocess
            )

    return result


def _load_templates_from_filesystem(
    environment: Environment,
    preprocess: Callable[[str], str] | None = None,
) -> Environment:
    # Scan a configured list of paths
    # for templates.

    # Get the templates path from
    # the configuration environment.
    templates_path_str_list: list[str] = environment.get(
        "mau.visitor.templates.paths", []
    )

    # If no paths have been specified,
    # return and empty environment.
    if not templates_path_str_list:
        return Environment()

    # The environment that collects
    # the loaded templates.
    templates = Environment()

    # Loop through all paths and try
    # to load templates from there.
    for templates_path_str in templates_path_str_list:
        templates.dupdate(
            _load_templates_from_path(
                templates_path_str,
                preprocess=preprocess,
            )
        )

    return templates


def _load_templates_from_environment(environment: Environment) -> Environment:
    templates_from_env: Environment = environment.get("mau.visitor.templates.custom")

    # If there are no templates return and empty environment.
    if not templates_from_env:
        return Environment()

    return Environment.from_environment(templates_from_env)


class JinjaVisitor(BaseVisitor):
    format_code = "jinja"
    extension = "j2"
    templates_preprocess: Callable[[str], str] | None = None

    join_with = {
        "document": "\n",
        "raw-content": "\n",
        "source": "\n",
        "paragraph": " ",
    }
    join_with_default = ""

    jinja_environment_options = {}
    default_templates = Environment().from_dict(
        {
            "document.j2": "{{ content }}",
            # "paragraph.j2": "{{ content }}",
            "text.j2": "{{ value }}",
        }
    )

    def __init__(self, environment: Environment, *args, **kwds):
        super().__init__(environment)

        # Load the template prefixes from the configuration.
        self.template_prefixes = _load_template_prefixes(self.environment)

        # Load default templates.
        # A custom implementation of this visitor might
        # provide default templates that can be overridden
        # by user-defined ones.
        self.templates = Environment.from_environment(self.default_templates)

        # Load the requested template providers from the configuration.
        templates_from_providers = _load_templates_from_providers(self.environment)
        self.templates.update(templates_from_providers)

        # Load user-defined templates from files.
        templates_from_filesystem = _load_templates_from_filesystem(
            self.environment,
            preprocess=self.templates_preprocess,
        )
        self.templates.update(templates_from_filesystem)

        # Load custom templates provided as a dictionary.
        self.templates.update(
            environment.get(
                "mau.visitor.templates.custom",
                Environment(),
            )
        )

        # This is the Jinja environment.
        # We prepare it with all the templates we loaded
        # in the previous section of the function.
        self._dict_env = jinja2.Environment(
            loader=jinja2.DictLoader(self.templates.asflatdict()),
            **self.jinja_environment_options,
        )

    def _render(
        self, node: Node, environment: Environment, template_full_name, **kwargs
    ) -> str:
        # This renders a template using the current
        # environment and the given parameters
        try:
            template = self._dict_env.get_template(template_full_name)
        except jinja2.exceptions.TemplateNotFound as exception:
            raise TemplateNotFound(exception) from exception

        try:
            rendered_template = template.render(
                config=self.environment.asdict(), **kwargs
            )
        except jinja2.exceptions.UndefinedError as exception:
            raise MauVisitorException(
                message=f"Error rendering node with template {template_full_name}: {str(exception)}",
                node=node,
                data=kwargs,
                environment=environment,
            ) from exception

        # print(f"NODE {node} RENDERED TO #{rendered_template}#")

        return rendered_template

    def visit(self, node, *args, **kwargs):
        # The visitor has to define functions for each node type
        # and those shall return a dictionary of keys.
        #
        # The node types are a list made of the key `node_types` and the node type.
        # This allows a function to return one or more types that have to
        # be used instead of the standard type, which also allows to write
        # generic functions. See _visit_style in HTMLVisitor which works for
        # multiple styles.
        #
        # The rest of the returned keys are passed to the _render function
        # as keys and are thus available in the template.

        # Template names are created with this schema

        # [prefix.][parent_type.][parent_subtype.][parent_position.][node_template][.node_subtype][.ext]

        # if node is None:
        #     return {}

        # Visit the node.
        result = super().visit(node, *args, **kwargs)

        if not result:
            return

        parent_prefix = None
        if node.parent:
            parent_prefix = f"{node.parent.type}"

        # print("PARENT:", node.parent)

        # Create the template names for the
        # current node.
        templates = _create_templates(
            node.type,
            self.extension,
            node.info.subtype,
            node.info.tags,
            node.custom_attributes,
            self.template_prefixes,
            parent_prefix,
        )

        # print(f"#### Node {node}")
        # print(f"#### Result {result}")
        # print(f"#### Templates: {templates}")

        # Scan all potential templates, trying to render
        # the given data with each of them.
        # Stop as soon as we find a working template.
        for template in templates:
            try:
                # print(f"RENDERING {template} WITH {result}")
                return self._render(node, self.environment, template, **result)
            except TemplateNotFound:
                continue

        # No templates were found, stop with an error.
        raise MissingTemplateException(
            node=node,
            data=result,
            environment=self.environment,
            templates=templates,
        )

    def visitlist(
        self, current_node: Node, nodes_list: Sequence[Node], *args, **kwargs
    ):
        # Find the string this visitor uses to join
        # children according to the current node type.
        join_with = self.join_with.get(current_node.type, self.join_with_default)

        # Visit all nodes in the list.
        visited_nodes = [self.visit(node, *args, **kwargs) for node in nodes_list]

        # Join the results if needed.
        if join_with is not None:
            return join_with.join(visited_nodes)

        return visited_nodes
