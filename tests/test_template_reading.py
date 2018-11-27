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
