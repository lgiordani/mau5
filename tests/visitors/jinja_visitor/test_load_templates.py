from unittest.mock import Mock, patch

import pytest

from mau.environment.environment import Environment
from mau.visitors.base_visitor import MauVisitorException
from mau.visitors.jinja_visitor import (
    _load_template_prefixes,
    _load_templates_from_environment,
    _load_templates_from_filesystem,
    _load_templates_from_providers,
)


def test_load_template_prefixes():
    env = Environment.from_dict({"mau.visitor.templates.prefixes": ["prefix1"]})

    assert _load_template_prefixes(env) == ["prefix1"]


@patch("mau.visitors.jinja_visitor._load_available_template_providers")
def test_load_templates_from_providers_defined_empty(
    mock_load_available_template_providers,
):
    env = Environment.from_dict({"mau.visitor.templates.providers": []})

    assert _load_templates_from_providers(env).asdict() == {}

    mock_load_available_template_providers.assert_not_called()


@patch("mau.visitors.jinja_visitor._load_available_template_providers")
def test_load_templates_from_providers_undefined(
    mock_load_available_template_providers,
):
    env = Environment()

    assert _load_templates_from_providers(env).asdict() == {}

    mock_load_available_template_providers.assert_not_called()


@patch("mau.visitors.jinja_visitor._load_available_template_providers")
def test_load_templates_from_providers_provider_available(
    mock_load_available_template_providers,
):
    provider1 = Mock()
    provider2 = Mock()

    mock_templates = {"template1": "text1"}
    provider1.templates = mock_templates

    mock_load_available_template_providers.return_value = {
        "provider1": provider1,
        "provider2": provider2,
    }

    env = Environment.from_dict({"mau.visitor.templates.providers": ["provider1"]})

    assert _load_templates_from_providers(env).asdict() == mock_templates

    mock_load_available_template_providers.assert_called_once()


@patch("mau.visitors.jinja_visitor._load_available_template_providers")
def test_load_templates_from_providers_provider_unavailable(
    mock_load_available_template_providers,
):
    provider1 = Mock()

    provider1.templates = {}

    mock_load_available_template_providers.return_value = {
        "provider1": provider1,
    }

    env = Environment.from_dict({"mau.visitor.templates.providers": ["provider2"]})

    with pytest.raises(MauVisitorException):
        assert _load_templates_from_providers(env)

    mock_load_available_template_providers.assert_called_once()


@patch("mau.visitors.jinja_visitor._load_templates_from_path")
def test_load_templates_from_filesystem_empty(mock_load_templates_from_path):
    env = Environment.from_dict({"mau.visitor.templates.paths": []})

    assert _load_templates_from_filesystem(env).asdict() == {}

    mock_load_templates_from_path.assert_not_called()


@patch("mau.visitors.jinja_visitor._load_templates_from_path")
def test_load_templates_from_filesystem_undefined(mock_load_templates_from_path):
    env = Environment()

    assert _load_templates_from_filesystem(env).asdict() == {}

    mock_load_templates_from_path.assert_not_called()


@patch("mau.visitors.jinja_visitor._load_templates_from_path")
def test_load_templates_from_filesystem(mock_load_templates_from_path):
    mock_templates = {"template1": "text1"}
    mock_load_templates_from_path.return_value = mock_templates

    env = Environment.from_dict({"mau.visitor.templates.paths": ["template_path"]})

    assert _load_templates_from_filesystem(env).asdict() == mock_templates

    mock_load_templates_from_path.assert_called_with("template_path", preprocess=None)


def test_load_templates_from_environment_empty():
    env = Environment.from_dict({"mau.visitor.templates.custom": {}})

    assert _load_templates_from_environment(env).asdict() == {}


def test_load_templates_from_environment_undefined():
    env = Environment()

    assert _load_templates_from_environment(env).asdict() == {}


def test_load_templates_from_environment():
    mock_templates = {"template1": "text1"}

    env = Environment.from_dict({"mau.visitor.templates.custom": mock_templates})

    assert _load_templates_from_environment(env).asdict() == mock_templates
