"""Small module for loading up templates."""


import os


TEMPLATE_DIR = os.path.expandvars(
    os.getenv("FLATWARE_TEMPLATE_DIR", "~/.plates/")
)


def get_avaliable_template_names(template_dir=TEMPLATE_DIR) -> list:
    """Show all plates in TEMPLATE_DIR."""
    files = [x for x in os.listdir(template_dir)
             if os.path.isfile(os.path.join(template_dir, x))]
    return files


def load_template(template_name: str, template_dir=TEMPLATE_DIR) -> str:
    """Load up a template by name from TEMPLATE_DIR."""
    file = os.path.join(template_dir, template_name)
    if not os.path.isfile(file):
        raise FileNotFoundError(("No template with name '{name}' found!"
                                 .format(name=template_name)))
    with open(file, "r") as raw_template:
        template = raw_template.read()
    return template
