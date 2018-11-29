"""Tests related to template reading."""


from configparser import ConfigParser
import pytest
import flatware.template_reading as reading


def test_template_splits():
    """Test that templates split in the required method."""
    template = """[name]
type=str
default=Allysa P. Hacker
---
Hello {{ name }}!"""
    config, template = reading.parse_template_config(template)
    assert template[0] == "H"
    assert config.get("name", "type") == "str"


def test_template_splits_limited():
    """Test that templates are limited to splitting once."""
    template = """[packages]
type=list
default="htop vim git"
---
---
This should be after the tripe dash.
"""
    config, template = reading.parse_template_config(template)
    assert '---\n' in template
    assert config.get("packages", "type") == "list"


def test_read_incomplete_template():
    """Test the reading of incomplete templates."""
    template = """[place]
type=str
default=M.I.T
"""
    with pytest.raises(TypeError) as e_info:
        reading.parse_template_config(template)
    assert "Invalid Template" in e_info.value.args[0]


def test_create_argument_list():
    """Test the creation of argument lists from configs."""
    raw_config = """[firstname]
type=str
default=rayman"""
    config = ConfigParser()
    config.read_string(raw_config)
    results = reading.get_template_arguments(config)
    assert results[0]['name'] == 'firstname'


def test_incorrect_template_argument_types():
    """Test to make sure incorrect argument types are not accepted."""
    raw_config = """[place]
type=location
"""
    config = ConfigParser()
    config.read_string(raw_config)
    with pytest.raises(TypeError) as e_info:
        reading.get_template_arguments(config)
    assert "not an accepted template argument" in e_info.value.args[0]


def test_string_argument_parsing():
    """Test that generated argument parsers can read strings properly."""
    arguments = [
        {
            "name": "firstname",
            "type": "str",
            "default": "Allysa P. Hacker",
        },
    ]
    parser = reading.build_template_argparser(arguments)
    values = parser.parse_args(["--firstname", "john"])
    assert values.firstname == "john"


def test_list_argument_parsing():
    """Test the parsing of list arguments."""
    arguments = [
        {
            "name": "places",
            "type": "list",
            "default": None
        }
    ]
    parser = reading.build_template_argparser(arguments)
    values = parser.parse_args(["--places", "hawaii", "california", "oregon"])
    assert values.places == ["hawaii", "california", "oregon"]

    values_with_spaces = parser.parse_args(['--places', "california",
                                            "new mexico", "washington"])
    assert values_with_spaces.places == ["california",
                                         "new mexico",
                                         "washington"]


def test_default_integer_argument_value():
    """Test that default arguments have the proper type."""
    arguments = [
        {
            "name": "sum",
            "type": "int",
            "default": "4"
        },
    ]
    parser = reading.build_template_argparser(arguments)
    values = parser.parse_args([])
    assert values.sum == 4


def test_default_list_argument_value():
    """Test default arguments for lists."""
    arguments = [
        {
            "name": "foods",
            "type": "list",
            "default": "pizza salad soup",
        }
    ]
    parser = reading.build_template_argparser(arguments)
    values = parser.parse_args([])
    assert values.foods == ["pizza", "salad", "soup"]


def test_falsy_default_argument_values():
    """Test the absence of default arguments."""
    arguments = [
        {
            "name": "nonrequired",
            "type": "str",
            "default": None
        },
    ]
    parser = reading.build_template_argparser(arguments)
    values = parser.parse_args([])
    assert values.nonrequired is None


def test_end_to_end_parsing():
    """Test one path through the template parsing."""
    template = """[name]
type=str
---
Hello, this is my template!"""
    template, parser = reading.make_argparse_from_template(template)
    assert template == "Hello, this is my template!"
    values = parser.parse_args(["--name", "John Doe"])
    assert values.name == "John Doe"
