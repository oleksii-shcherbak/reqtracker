# reqtracker/config.py

from pathlib import Path
import toml
from typing import List, Optional, Dict, Any

class ReqtrackerConfig:
    """
    Manages reqtracker configuration, merging defaults, .reqtracker.toml,
    and inline overrides.
    """
    def __init__(
        self,
        project_root: str = ".",
        output_file: str = "requirements.txt",
        mode: str = "hybrid",
        ignore_paths: Optional[List[str]] = None,
        exclude_modules: Optional[List[str]] = None,
        include_dev: bool = False,
        inline_overrides: Optional[Dict[str, Any]] = None
    ):
        self._defaults = {
            "project_root": Path("."),
            "output_file": "requirements.txt",
            "mode": "hybrid", # 'static', 'dynamic', 'hybrid'
            "ignore_paths": [],
            "exclude_modules": [],
            "include_dev": False,
        }

        self._toml_config = self._load_toml_config(project_root)

        # Merge defaults, then TOML, then inline overrides
        self._effective_config = self._defaults.copy()
        self._effective_config.update(self._toml_config)

        # Apply inline overrides
        if inline_overrides:
            # Only update for keys that actually have non-None values in overrides
            # This allows track(output_file=None) to not override if it was explicitly passed None
            self._effective_config.update({k: v for k, v in inline_overrides.items() if v is not None})

        # Ensure paths are Path objects if they came from string in TOML
        # And ensure explicit __init__ args take precedence
        self._effective_config['project_root'] = Path(project_root) if project_root != self._defaults['project_root'] else Path(self._effective_config['project_root'])

        if output_file != self._defaults['output_file']:
            self._effective_config['output_file'] = output_file
        if mode != self._defaults['mode']:
            self._effective_config['mode'] = mode
        if ignore_paths is not None:
            self._effective_config['ignore_paths'] = ignore_paths
        if exclude_modules is not None:
            self._effective_config['exclude_modules'] = exclude_modules
        if include_dev is not self._defaults['include_dev']: # Check if different from default False
             self._effective_config['include_dev'] = include_dev


    def _load_toml_config(self, project_root: str) -> Dict[str, Any]:
        """Loads configuration from .reqtracker.toml if it exists."""
        config_path = Path(project_root) / ".reqtracker.toml"
        if config_path.exists():
            try:
                with open(config_path, 'r') as f:
                    return toml.load(f)
            except toml.TomlDecodeError as e:
                print(f"Warning: Could not parse {config_path}. Check TOML syntax. Error: {e}")
                return {}
        return {}

    def __getattr__(self, name: str) -> Any:
        """Allows accessing config settings as attributes (e.g., config.output_file)."""
        if name in self._effective_config:
            return self._effective_config[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

    def __str__(self):
        return f"Config({self._effective_config})"

    def __repr__(self):
        return self.__str__()
