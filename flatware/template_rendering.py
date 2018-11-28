"""Small module for rendering templates with Jinja2."""


import jinja2


def render_template(raw_template: str, context: dict) -> str:
    """Render a template string with given context."""
    template = jinja2.Template(raw_template)
    return template.render(**context)
