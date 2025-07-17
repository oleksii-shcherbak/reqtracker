# test/test_config.py

import pytest
from pathlib import Path
from reqtracker.config import ReqtrackerConfig


@pytest.fixture
def temp_project_dir(tmp_path: Path) -> Path:
    """Provides a temporary directory for tests."""
    return tmp_path


@pytest.fixture
def create_toml_config_file(temp_project_dir: Path):
    """
    A factory fixture to create a .reqtracker.toml file in the temporary project directory.

    Returns:
        A function that takes content (str) and writes it to the config file.
    """

    def _creator(content: str) -> Path:
        """
        Writes the given content to a .reqtracker.toml file in the temporary project directory.

        Args:
            content: The string content to write to the TOML file.

        Returns:
            The Path object of the created .reqtracker.toml file.
        """
        config_path = temp_project_dir / ".reqtracker.toml"
        config_path.write_text(content)
        return config_path

    return _creator


def test_config_defaults(tmp_path: Path):
    """
    Tests that ReqtrackerConfig initializes with correct default values
    when no TOML file or inline overrides are provided.
    """
    config = ReqtrackerConfig(project_root=str(tmp_path))
    assert config.project_root == tmp_path.resolve()
    assert config.output_file == (tmp_path / "requirements.txt").resolve()
    assert config.mode == "hybrid"
    assert config.ignore_paths == []
    assert config.exclude_modules == []
    assert config.include_dev is False
    assert config.print_to_console is False


def test_config_from_toml(temp_project_dir: Path, create_toml_config_file):
    """
    Tests that ReqtrackerConfig correctly loads and applies all settings
    from a .reqtracker.toml file.
    """
    toml_content = """
    [reqtracker]
    output_file = "custom_reqs.txt"
    mode = "static"
    ignore_paths = ["venv", "data"]
    exclude_modules = ["numpy", "pandas"]
    include_dev = true
    print_to_console = true
    """
    create_toml_config_file(toml_content)

    config = ReqtrackerConfig(project_root=str(temp_project_dir))
    assert config.output_file == (temp_project_dir / "custom_reqs.txt").resolve()
    assert config.mode == "static"
    assert config.ignore_paths == ["venv", "data"]
    assert config.exclude_modules == ["numpy", "pandas"]
    assert config.include_dev is True
    assert config.print_to_console is True


def test_config_toml_partial_override(temp_project_dir: Path, create_toml_config_file):
    """
    Tests that a partially specified .reqtracker.toml file
    only overrides the specified settings, leaving others at defaults.
    """
    toml_content = """
    [reqtracker]
    mode = "dynamic"
    """
    create_toml_config_file(toml_content)

    config = ReqtrackerConfig(project_root=str(temp_project_dir))
    assert config.mode == "dynamic"
    assert config.output_file == (temp_project_dir / "requirements.txt").resolve()
    assert config.ignore_paths == []


def test_config_toml_decode_error(temp_project_dir: Path, create_toml_config_file, capsys):
    """
    Tests that ReqtrackerConfig gracefully handles an invalid .reqtracker.toml file
    by printing a warning and reverting to default settings.
    """
    invalid_toml_content = """
    [reqtracker
    output_file = "test.txt"
    """
    create_toml_config_file(invalid_toml_content)

    config = ReqtrackerConfig(project_root=str(temp_project_dir))

    captured = capsys.readouterr()
    assert "Warning: Could not parse" in captured.out
    assert config.mode == "hybrid"


def test_config_inline_override(tmp_path: Path):
    """
    Tests that ReqtrackerConfig correctly applies settings from inline_overrides,
    overriding default values.
    """
    inline_overrides = {
        "output_file": "my_custom.txt",
        "mode": "dynamic",
        "exclude_modules": ["sys", "os"],
        "print_to_console": True
    }
    config = ReqtrackerConfig(project_root=str(tmp_path), inline_overrides=inline_overrides)
    assert config.output_file == (tmp_path / "my_custom.txt").resolve()
    assert config.mode == "dynamic"
    assert config.exclude_modules == ["sys", "os"]
    assert config.print_to_console is True


def test_config_inline_override_none_values(tmp_path: Path, create_toml_config_file):
    """
    Tests that `None` values in inline_overrides do not overwrite
    valid settings loaded from a TOML file.
    """
    toml_content = """
    [reqtracker]
    output_file = "toml_set.txt"
    mode = "static"
    """
    create_toml_config_file(toml_content)

    inline_overrides = {
        "output_file": None,
        "mode": None,
    }
    config = ReqtrackerConfig(project_root=str(tmp_path), inline_overrides=inline_overrides)

    assert config.output_file == (tmp_path / "toml_set.txt").resolve()
    assert config.mode == "static"


def test_config_toml_and_inline_precedence(temp_project_dir: Path, create_toml_config_file):
    """
    Tests the precedence: inline_overrides should override TOML settings,
    and TOML settings should override defaults.
    """
    toml_content = """
    [reqtracker]
    output_file = "toml_file.txt"
    mode = "static"
    ignore_paths = ["dist"]
    """
    create_toml_config_file(toml_content)

    inline_overrides = {
        "output_file": "inline_file.txt",
        "mode": "dynamic",
        "exclude_modules": ["logging"]
    }
    config = ReqtrackerConfig(project_root=str(temp_project_dir), inline_overrides=inline_overrides)

    assert config.output_file == (temp_project_dir / "inline_file.txt").resolve()
    assert config.mode == "dynamic"
    assert config.ignore_paths == ["dist"]
    assert config.exclude_modules == ["logging"]


def test_config_paths_resolved(tmp_path: Path):
    """
    Tests that `project_root` and `output_file` paths are correctly resolved
    to absolute paths.
    """
    config = ReqtrackerConfig(project_root=str(tmp_path / "sub_dir"), output_file="output/reqs.txt")
    assert config.project_root == (tmp_path / "sub_dir").resolve()
    assert config.output_file == (
                tmp_path / "sub_dir" / "output" / "reqs.txt").resolve()  # Output relative to project_root


def test_config_output_file_relative_to_project_root_default(tmp_path: Path):
    """
    Tests that the default `output_file` path is resolved relative
    to the `project_root` when no explicit output file is given.
    """
    custom_project_root = tmp_path / "my_project"
    custom_project_root.mkdir(exist_ok=True)
    config = ReqtrackerConfig(project_root=str(custom_project_root))

    assert config.output_file == (custom_project_root / "requirements.txt").resolve()
    assert config.project_root == custom_project_root.resolve()


def test_config_output_file_relative_to_project_root_explicit(tmp_path: Path):
    """
    Tests that an explicitly provided relative `output_file` path
    is resolved correctly relative to the `project_root`.
    """
    custom_project_root = tmp_path / "my_project"
    custom_project_root.mkdir()

    output_path_relative_to_project_str = "my_custom_reqs.txt"

    config = ReqtrackerConfig(
        project_root=str(custom_project_root),
        output_file=output_path_relative_to_project_str
    )
    assert config.output_file == (custom_project_root / output_path_relative_to_project_str).resolve()
    assert config.project_root == custom_project_root.resolve()


def test_config_getattr(tmp_path: Path):
    """
    Tests that configuration attributes can be accessed directly
    via `config.attribute_name`.
    """
    config = ReqtrackerConfig(project_root=str(tmp_path), inline_overrides={"mode": "static"})
    assert config.mode == "static"
    assert config.project_root == tmp_path.resolve()


def test_config_getattr_non_existent(tmp_path: Path):
    """
    Tests that accessing a non-existent configuration attribute
    raises an AttributeError.
    """
    config = ReqtrackerConfig(project_root=str(tmp_path))
    with pytest.raises(AttributeError):
        _ = config.non_existent_attribute


def test_config_output_file_absolute_path_toml(temp_project_dir: Path, create_toml_config_file):
    """
    Tests that an absolute `output_file` path specified in .reqtracker.toml
    is correctly used without being re-resolved relative to `project_root`.
    """
    abs_output_dir = temp_project_dir / "abs_output_dir"
    abs_output_dir.mkdir()
    abs_output_path = (abs_output_dir / "absolute_reqs_toml.txt").resolve()

    toml_content = f"""
    [reqtracker]
    output_file = "{abs_output_path}"
    """
    create_toml_config_file(toml_content)

    config = ReqtrackerConfig(project_root=str(temp_project_dir))
    assert config.output_file == abs_output_path


def test_config_output_file_absolute_path_inline(tmp_path: Path):
    """
    Tests that an absolute `output_file` path specified in inline_overrides
    is correctly used without being re-resolved relative to `project_root`.
    """
    abs_output_dir = tmp_path / "abs_output_dir_inline"
    abs_output_dir.mkdir()
    abs_output_path = (abs_output_dir / "absolute_reqs_inline.txt").resolve()

    inline_overrides = {
        "output_file": str(abs_output_path)
    }
    config = ReqtrackerConfig(project_root=str(tmp_path), inline_overrides=inline_overrides)
    assert config.output_file == abs_output_path


def test_config_constructor_override_toml_and_inline(temp_project_dir: Path, create_toml_config_file):
    """
    Tests that direct constructor arguments have the highest precedence,
    overriding both TOML settings and inline overrides.
    """
    toml_content = """
    [reqtracker]
    mode = "static"
    output_file = "toml_output.txt"
    """
    create_toml_config_file(toml_content)

    inline_overrides = {
        "mode": "dynamic",
        "output_file": "inline_output.txt"
    }

    constructor_mode = "test_mode"
    constructor_output_file = "constructor_output.txt"

    config = ReqtrackerConfig(
        project_root=str(temp_project_dir),
        mode=constructor_mode,
        output_file=constructor_output_file,
        inline_overrides=inline_overrides
    )

    assert config.mode == constructor_mode
    assert config.output_file == (temp_project_dir / constructor_output_file).resolve()
    assert config.project_root == temp_project_dir.resolve()


def test_config_empty_lists_from_toml_and_inline(temp_project_dir: Path, create_toml_config_file):
    """
    Tests that empty lists for `ignore_paths` and `exclude_modules` are correctly
    loaded from TOML and applied via inline overrides.
    """
    toml_content_empty_lists = """
    [reqtracker]
    ignore_paths = []
    exclude_modules = []
    """
    create_toml_config_file(toml_content_empty_lists)
    config_toml = ReqtrackerConfig(project_root=str(temp_project_dir))
    assert config_toml.ignore_paths == []
    assert config_toml.exclude_modules == []

    toml_content_non_empty_lists = """
    [reqtracker]
    ignore_paths = ["old_path"]
    exclude_modules = ["old_module"]
    """
    create_toml_config_file(toml_content_non_empty_lists)

    inline_overrides_empty_lists = {
        "ignore_paths": [],
        "exclude_modules": []
    }
    config_inline = ReqtrackerConfig(project_root=str(temp_project_dir), inline_overrides=inline_overrides_empty_lists)
    assert config_inline.ignore_paths == []
    assert config_inline.exclude_modules == []
