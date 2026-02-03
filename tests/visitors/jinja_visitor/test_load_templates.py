from unittest.mock import Mock, patch

import pytest

from mau.environment.environment import Environment
from mau.error import MauErrorType, MauException
from mau.visitors.jinja_visitor import (
    load_template_prefixes,
    load_templates_from_environment,
    load_templates_from_filesystem,
    load_templates_from_providers,
)


def testload_template_prefixes():
    env = Environment.from_dict({"mau.visitor.templates.prefixes": ["prefix1"]})

    assert load_template_prefixes(env) == ["prefix1"]


@patch("mau.visitors.jinja_visitor.load_available_template_providers")
def testload_templates_from_providers_defined_empty(
    mockload_available_template_providers,
):
    env = Environment.from_dict({"mau.visitor.templates.providers": []})

    assert load_templates_from_providers(env).asdict() == {}

    mockload_available_template_providers.assert_not_called()


@patch("mau.visitors.jinja_visitor.load_available_template_providers")
def testload_templates_from_providers_undefined(
    mockload_available_template_providers,
):
    env = Environment()

    assert load_templates_from_providers(env).asdict() == {}

    mockload_available_template_providers.assert_not_called()


@patch("mau.visitors.jinja_visitor.load_available_template_providers")
def testload_templates_from_providers_provider_available(
    mockload_available_template_providers,
):
    provider1 = Mock()
    provider2 = Mock()

    mock_templates = {"template1": "text1"}
    provider1.templates = mock_templates

    mockload_available_template_providers.return_value = {
        "provider1": provider1,
        "provider2": provider2,
    }

    env = Environment.from_dict({"mau.visitor.templates.providers": ["provider1"]})

    assert load_templates_from_providers(env).asdict() == mock_templates

    mockload_available_template_providers.assert_called_once()


@patch("mau.visitors.jinja_visitor.load_available_template_providers")
def testload_templates_from_providers_provider_unavailable(
    mockload_available_template_providers,
):
    provider1 = Mock()

    provider1.templates = {}

    mockload_available_template_providers.return_value = {
        "provider1": provider1,
    }

    env = Environment.from_dict({"mau.visitor.templates.providers": ["provider2"]})

    with pytest.raises(MauException) as exc:
        assert load_templates_from_providers(env)

    assert exc.value.error.type == MauErrorType.VISITOR
    mockload_available_template_providers.assert_called_once()


@patch("mau.visitors.jinja_visitor.load_templates_from_path")
def testload_templates_from_filesystem_empty(mockload_templates_from_path):
    env = Environment.from_dict({"mau.visitor.templates.paths": []})

    assert load_templates_from_filesystem(env).asdict() == {}

    mockload_templates_from_path.assert_not_called()


@patch("mau.visitors.jinja_visitor.load_templates_from_path")
def testload_templates_from_filesystem_undefined(mockload_templates_from_path):
    env = Environment()

    assert load_templates_from_filesystem(env).asdict() == {}

    mockload_templates_from_path.assert_not_called()


@patch("mau.visitors.jinja_visitor.load_templates_from_path")
def testload_templates_from_filesystem(mockload_templates_from_path):
    mock_templates = {"template1": "text1"}
    mockload_templates_from_path.return_value = mock_templates

    env = Environment.from_dict({"mau.visitor.templates.paths": ["template_path"]})

    assert load_templates_from_filesystem(env).asdict() == mock_templates

    mockload_templates_from_path.assert_called_with("template_path", preprocess=None)


def testload_templates_from_environment_empty():
    env = Environment.from_dict({"mau.visitor.templates.custom": {}})

    assert load_templates_from_environment(env).asdict() == {}


def testload_templates_from_environment_undefined():
    env = Environment()

    assert load_templates_from_environment(env).asdict() == {}


def testload_templates_from_environment():
    mock_templates = {"template1": "text1"}

    env = Environment.from_dict({"mau.visitor.templates.custom": mock_templates})

    assert load_templates_from_environment(env).asdict() == mock_templates
