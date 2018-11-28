"""Sanity tests for template rendering."""


from flatware.template_rendering import render_template


def test_template_rendering():
    """Sanity test for template rendering."""
    template = "{{ hello }}"
    context = {"hello": "world"}
    assert render_template(template, context) == "world"
