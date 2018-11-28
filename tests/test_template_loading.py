"""Test template loading functions."""


import pytest
import flatware.template_loading as loading


def test_load_file(tmpdir):
    """Test we can load a plate."""
    plate = tmpdir.join("recipe")
    plate.write("Plate text")
    result = loading.load_template("recipe", template_dir=tmpdir)
    assert result == "Plate text"


def test_list_plates(tmpdir):
    """Test that we can list all plates."""
    plate = tmpdir.join("component")
    plate.write("Plate text")
    result = loading.get_avaliable_template_names(template_dir=tmpdir)
    assert result == ["component"]


def test_load_plate_does_not_exist(tmpdir):
    """Test proper errors are raised."""
    with pytest.raises(FileNotFoundError) as e_info:
        loading.load_template("ghost", tmpdir)
    assert "No template with name 'ghost' found!" in e_info.value.args[0]
