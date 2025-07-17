# reqtracker/tracker.py

import sys
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from typing import Set, List, Optional
from .core import is_third_party_module
from pathlib import Path

# Global state for dynamic tracking
_tracked_modules: Set[str] = set()
_original_meta_path: Optional[List] = None
_reqtracker_finder: Optional["ReqtrackerMetaPathFinder"] = None

class ReqtrackerMetaPathFinder(MetaPathFinder):
    """
    A custom MetaPathFinder that intercepts module imports to record them.
    It delegates to the default import system for actual module loading.
    """
    def __init__(self, project_root: Path, exclude_modules: Optional[List[str]] = None):
        self.project_root = project_root
        self.exclude_modules = set(exclude_modules) if exclude_modules else set()

    def find_spec(self, fullname: str, path: Optional[List[str]], target=None) -> Optional[ModuleSpec]:
        """
        Intercepts import attempts. Records top-level third-party module names.
        """
        top_level_module_name = fullname.split('.')[0]

        if top_level_module_name.startswith('reqtracker'):
            pass
        elif top_level_module_name not in self.exclude_modules and \
             is_third_party_module(top_level_module_name, self.project_root):
            _tracked_modules.add(top_level_module_name)

        return None

def enable_dynamic_tracking(project_root: Path, exclude_modules: Optional[List[str]] = None) -> None:
    """
    Enables dynamic tracking by inserting ReqtrackerMetaPathFinder into sys.meta_path.
    """
    global _reqtracker_finder, _original_meta_path
    if _reqtracker_finder is not None:
        return

    _reqtracker_finder = ReqtrackerMetaPathFinder(project_root, exclude_modules)
    _original_meta_path = sys.meta_path[:]
    sys.meta_path.insert(0, _reqtracker_finder)

def disable_dynamic_tracking() -> None:
    """
    Disables dynamic tracking by removing ReqtrackerMetaPathFinder from sys.meta_path.
    Resets sys.meta_path to its original state if possible.
    """
    global _reqtracker_finder, _original_meta_path
    if _reqtracker_finder is None:
        return

    try:
        sys.meta_path.remove(_reqtracker_finder)
    except ValueError:
        pass

    if _original_meta_path is not None and sys.meta_path != _original_meta_path:
        sys.meta_path = _original_meta_path[:]

    _reqtracker_finder = None
    _original_meta_path = None

def get_tracked_modules() -> Set[str]:
    """
    Returns the set of modules tracked during dynamic analysis.
    """
    return _tracked_modules.copy()

def clear_tracked_modules() -> None:
    """
    Clears the set of modules tracked by the dynamic analysis.
    Useful for resetting between runs or tests.
    """
    global _tracked_modules
    _tracked_modules.clear()
