"""Module in charge of reading and parsing plates."""


import logging
import configparser


LOG = logging.getLogger(__name__)
ARGUMENT_TYPES = ["str", "list", "int", "float"]


def parse_template_config(raw_template: str) -> tuple:
    """Split a template into its config and the template itself."""
    try:
        options, template = raw_template.split("---\n")
    except ValueError:
        raise TypeError("Invalid Template.")
    config = configparser.ConfigParser()
    config.read_string(options)
    return config, template


def get_template_arguments(config: configparser.ConfigParser) -> list:
    """Get the arguments defined in the template config.

    Arguments:
        config: config object from top of template.
    Returns:
        result: List of {"type": type, "default": default, "name": name}
    """
    sections = config.sections()
    results = []
    for argument in sections:
        argument_type = config.get(argument, "type", fallback="str")
        try:
            assert argument_type in ARGUMENT_TYPES
        except AssertionError:
            raise TypeError("Argument type '%s' is not an accepted "
                            "template argument type." % argument_type)
        argument_default = config.get(argument, "default", fallback=None)
        argument_name = argument
        results.append({
            "type": argument_type,
            "default": argument_default,
            "name": argument_name
        })
    return results
