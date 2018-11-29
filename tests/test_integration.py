"""Integration tests."""


from flatware.cli import parse_render_template


def test_parse_render_template(tmpdir):
    """Test for reading, parsing, and rendering templates"""
    template = tmpdir.join("nameform")
    template.write(('[name]\n'
                    'type=str\n'
                    '\n'
                    '[places]\n'
                    'type=list\n'
                    '---\n'
                    'Hello {{ name }}!\n'
                    'Here are places you can go:\n'
                    '{% for place in places %}\n'
                    '{{ place }}\n'
                    '{% endfor %}'))
    extra_args = ['--name', 'Julia', '--places', 'New York', 'San Francisco']
    result = parse_render_template("nameform", extra_args, template_dir=tmpdir)
    assert 'Hello Julia!' in result
    assert 'New York' in result
    assert 'San Francisco' in result
