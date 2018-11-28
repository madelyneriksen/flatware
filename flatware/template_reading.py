"""Module in charge of reading and parsing plates."""


import logging
import argparse
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


def build_template_argparser(template_args: list) -> argparse.ArgumentParser:
    """Build an argument parser for the template."""
    argparser = argparse.ArgumentParser()
    for argument in template_args:
        argument_parsers = {
            "str": parse_str,
            "list": parse_list,
            "int": parse_int,
            "float": parse_float,
        }
        parser = argument_parsers.get(argument["type"], "str")
        parser(argument, argparser)
    return argparser


# Argument Parsers for building argparser on template arguments.
def parse_str(argument: dict, argparser: argparse.ArgumentParser) -> None:
    """Add a string argument to the argparser."""
    argparser.add_argument(
        "--{}".format(argument["name"]),
        type=str,
        default=argument["default"],
    )


def parse_list(argument: dict, argparser: argparse.ArgumentParser) -> None:
    """Add a list argument to the argparser."""
    if argument["default"]:
        extra_args = {"default": argument["default"].split(' ')}
    else:
        extra_args = {}
    argparser.add_argument(
        "--{}".format(argument["name"]),
        nargs='*',
        **extra_args
    )


def parse_int(argument: dict, argparser: argparse.ArgumentParser) -> None:
    """Add a int argument to the argparser."""
    if argument["default"]:
        extra_args = {"default": int(argument["default"].strip())}
    else:
        extra_args = {}
    argparser.add_argument(
        "--{}".format(argument["name"]),
        type=int,
        **extra_args,
    )


def parse_float(argument: dict, argparser: argparse.ArgumentParser) -> None:
    """Add a float argument to the argparser."""
    if argument["default"]:
        extra_args = {"default": float(argument["default"].strip())}
    else:
        extra_args = {}
    argparser.add_argument(
        "--{}".format(argument["name"]),
        type=float,
        **extra_args,
    )


def make_argparse_from_template(template: str) -> tuple:
    """Make an argparser from a template given as a string.

    This is the top level function for this module and what the
    command line wraps.

    Arguments:
        template: A string version of a plate
    Returns:
        result: A tuple of a template string and the argparser for it.
    """
    config, template = parse_template_config(template)
    arguments = get_template_arguments(config)
    argparser = build_template_argparser(arguments)
    return template, argparser
