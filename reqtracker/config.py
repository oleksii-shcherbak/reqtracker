# reqtracker/config.py

from pathlib import Path
import toml
from typing import Any, Dict, List, Optional


class ReqtrackerConfig:
    """
    Manages the configuration for the reqtracker application.

    This class loads configuration settings from multiple sources with a defined
    precedence:
    1. Default values (lowest precedence)
    2. Settings from a `.reqtracker.toml` file in the project root
    3. Inline overrides provided programmatically (e.g., via command-line arguments)
    4. Direct arguments passed to the `ReqtrackerConfig` constructor (highest precedence)

    Paths are resolved to absolute paths relative to the project root unless they
    are already absolute.
    """

    def __init__(
            self,
            project_root: str,
            output_file: str = "requirements.txt",
            mode: str = "hybrid",
            ignore_paths: Optional[List[str]] = None,
            exclude_modules: Optional[List[str]] = None,
            include_dev: bool = False,
            print_to_console: bool = False,
            inline_overrides: Optional[Dict[str, Any]] = None,
    ):
        """
        Initializes the ReqtrackerConfig with settings from various sources.

        Args:
            project_root: The root directory of the project to analyze. All relative
                          paths in configuration will be resolved against this.
            output_file: The name or path of the output file for requirements.
                         Defaults to "requirements.txt". Can be relative or absolute.
            mode: The tracking mode ("static", "dynamic", "hybrid"). Defaults to "hybrid".
            ignore_paths: A list of paths (directories or files) to ignore during analysis.
                          Defaults to an empty list.
            exclude_modules: A list of module names to exclude from the requirements.
                             Defaults to an empty list.
            include_dev: If True, includes development dependencies. Defaults to False.
            print_to_console: If True, prints discovered dependencies to the console.
                              Defaults to False.
            inline_overrides: A dictionary of settings to apply programmatically,
                              overriding TOML settings. Keys should match config attributes.
        """
        self.project_root = Path(project_root).resolve()

        self._config_data: Dict[str, Any] = {
            "output_file": (self.project_root / "requirements.txt").resolve(),
            "mode": "hybrid",
            "ignore_paths": [],
            "exclude_modules": [],
            "include_dev": False,
            "print_to_console": False,
        }

        toml_settings = self._load_toml_config(self.project_root)
        if toml_settings:
            for key, value in toml_settings.items():
                if key == "output_file":
                    toml_output_path = Path(value)
                    if not toml_output_path.is_absolute():
                        self._config_data[key] = (self.project_root / toml_output_path).resolve()
                    else:
                        self._config_data[key] = toml_output_path.resolve()
                elif key in self._config_data:
                    self._config_data[key] = value

        if inline_overrides:
            for key, value in inline_overrides.items():
                if value is not None:
                    if key == "output_file":
                        inline_output_path = Path(value)
                        if not inline_output_path.is_absolute():
                            self._config_data[key] = (self.project_root / inline_output_path).resolve()
                        else:
                            self._config_data[key] = inline_output_path.resolve()
                    elif key in self._config_data:
                        self._config_data[key] = value

        default_output_file_name = "requirements.txt"
        if output_file != default_output_file_name or Path(output_file).is_absolute():
            ctor_output_path_obj = Path(output_file)
            if not ctor_output_path_obj.is_absolute():
                self._config_data["output_file"] = (self.project_root / ctor_output_path_obj).resolve()
            else:
                self._config_data["output_file"] = ctor_output_path_obj.resolve()

        default_mode = "hybrid"
        if mode != default_mode:
            self._config_data["mode"] = mode

        if ignore_paths is not None:
            self._config_data["ignore_paths"] = ignore_paths

        if exclude_modules is not None:
            self._config_data["exclude_modules"] = exclude_modules

        default_include_dev = False
        if include_dev != default_include_dev:
            self._config_data["include_dev"] = include_dev

        default_print_to_console = False
        if print_to_console != default_print_to_console:
            self._config_data["print_to_console"] = print_to_console

        for key, value in self._config_data.items():
            if key != "project_root":
                setattr(self, key, value)

    @staticmethod
    def _load_toml_config(project_root: Path) -> Optional[Dict[str, Any]]:
        """
        Loads configuration settings from the .reqtracker.toml file in the project root.

        Args:
            project_root: The root directory of the project.

        Returns:
            A dictionary of settings found under the `[reqtracker]` section,
            or None if the file does not exist or cannot be parsed.
        """
        config_path = project_root / ".reqtracker.toml"
        if config_path.exists():
            try:
                config_data = toml.load(config_path)
                return config_data.get("reqtracker")
            except toml.TomlDecodeError as e:
                print(f"Warning: Could not parse {config_path}. Using the default configuration. Error: {e}")
                return None
        return None

    def __getattr__(self, name: str) -> Any:
        """
        Provides direct attribute access to configuration settings.

        Args:
            name: The name of the configuration setting to retrieve.

        Returns:
            The value of the specified configuration setting.

        Raises:
            AttributeError: If the requested attribute does not exist in the configuration.
        """
        if name in self._config_data:
            return self._config_data[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __repr__(self) -> str:
        """
        Provides a string representation of the ReqtrackerConfig object for debugging.

        Returns:
            A string showing the current configuration data.
        """
        data_for_repr = self._config_data.copy()
        data_for_repr["project_root"] = self.project_root
        return f"ReqtrackerConfig({data_for_repr})"
