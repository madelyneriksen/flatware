"""Command line entrypoint for flatware."""


import sys
import argparse
from flatware.template_reading import make_argparse_from_template
from flatware.template_loading import load_template
from flatware.template_rendering import render_template


def create_argparser():
    """Create the main argparser."""
    main_argparser = argparse.ArgumentParser(
        "Flatware is an application for reading and using single-file "
        "templates called 'plates'."
    )
    main_argparser.add_argument("plate", help="Name of the plate file.")
    return main_argparser


def parse_render_template(plate: str, extra_args: list,
                          template_dir=None) -> str:
    """Parse and render a given plate."""
    if template_dir:
        raw_template = load_template(plate, template_dir=template_dir)
    else:
        raw_template = load_template(plate)
    template, argparser = make_argparse_from_template(raw_template)
    context = vars(argparser.parse_args(extra_args))
    return render_template(template, context)


def main():
    """Main entrypoint."""
    main_argparser = create_argparser()
    main_args, extra_args = main_argparser.parse_known_args()
    if main_args.plate:
        result = parse_render_template(main_args.plate, extra_args)
        print(result)
        sys.exit(0)


if __name__ == "__main__":
    main()
