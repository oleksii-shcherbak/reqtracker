# reqtracker/core.py

import ast
import sys
import os
from pathlib import Path
from typing import List, Set, Optional

class ImportVisitor(ast.NodeVisitor):
    """
    AST NodeVisitor to find imported module names.
    Collects top-level module names.
    """
    def __init__(self):
        self.imported_modules = set()

    def visit_Import(self, node):
        """Handles `import module_a, module_b` statements."""
        for alias in node.names:
            self.imported_modules.add(alias.name.split('.')[0])
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Handles `from module_a import func` statements."""
        if node.module:
            self.imported_modules.add(node.module.split('.')[0])
        self.generic_visit(node)

# --- Helper functions for module classification ---

def _get_module_origin(module_name: str) -> Optional[Path]:
    """
    Attempts to find the file path where a module is defined.
    Returns Path object if found, None otherwise.
    """
    spec = sys.modules.get(module_name)
    if spec and hasattr(spec, '__file__') and spec.__file__:
        return Path(spec.__file__).resolve()
    return None

def _is_in_stdlib_path(module_path: Path) -> bool:
    """
    Checks if a module's path indicates it's part of the standard library.
    This is a heuristic.
    """
    stdlib_dirs = [
        Path(sys.prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}",
        Path(sys.base_prefix) / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}",
    ]
    site_packages_dirs = [
        Path(p) for p in sys.path if 'site-packages' in p or 'dist-packages' in p
    ]

    for std_dir in stdlib_dirs:
        try:
            if module_path.is_relative_to(std_dir):
                if not any(module_path.is_relative_to(sp_dir) for sp_dir in site_packages_dirs):
                    return True
        except ValueError:
            continue
    return False

def is_third_party_module(module_name: str, project_root: Path) -> bool:
    """
    Determines if a module is a third-party dependency.
    It's NOT a third-party module if it's:
    1. A built-in module (from sys.builtin_module_names)
    2. A standard library module (checked using sys.stdlib_module_names or path heuristic)
    3. A module/package found locally within the project_root.
    """
    # 1. Check built-in modules
    if module_name in sys.builtin_module_names:
        return False

    # 2. Check standard library modules using Python 3.10+'s sys.stdlib_module_names
    if sys.version_info >= (3, 10):
        if module_name in sys.stdlib_module_names:
            return False
    else:
        # Fallback for Python versions < 3.10: use path heuristic
        module_path = _get_module_origin(module_name)
        if module_path and _is_in_stdlib_path(module_path):
            return False

    # 3. Check local modules/packages within the project_root
    for p in sys.path:
        candidate_path = Path(p) / module_name.replace('.', os.sep)
        if (candidate_path.is_file() and candidate_path.suffix == '.py') or \
           (candidate_path.is_dir() and (candidate_path / '__init__.py').is_file()):
            try:
                if candidate_path.resolve().is_relative_to(project_root.resolve()):
                    return False
            except ValueError:
                pass

    return True


def find_dependencies_static(
    project_root: str,
    ignore_paths: Optional[List[str]] = None,
    exclude_modules: Optional[List[str]] = None
) -> Set[str]:
    """
    Scans Python source files in the project_root to find third-party dependencies.
    """
    project_path = Path(project_root).resolve()
    found_dependencies = set()

    if ignore_paths is None:
        ignore_paths = []
    if exclude_modules is None:
        exclude_modules = []

    resolved_ignore_paths = [project_path / Path(p).relative_to('/') if Path(p).is_absolute() else project_path / p for p in ignore_paths]
    resolved_ignore_paths = [p.resolve() for p in resolved_ignore_paths]

    for root, _, files in os.walk(project_path):
        current_path = Path(root).resolve()

        if any(current_path.is_relative_to(ignore_p) for ignore_p in resolved_ignore_paths):
            continue

        for file in files:
            if file.endswith(".py"):
                file_path = current_path / file
                if any(file_path.is_relative_to(ignore_f) for ignore_f in resolved_ignore_paths):
                    continue

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        tree = ast.parse(f.read(), filename=str(file_path))

                    visitor = ImportVisitor()
                    visitor.visit(tree)

                    for module_name in visitor.imported_modules:
                        if is_third_party_module(module_name, project_path) and \
                           module_name not in exclude_modules:
                            found_dependencies.add(module_name)
                except Exception as e:
                    print(f"Warning: Could not parse {file_path}. Skipping. Error: {e}")

    return found_dependencies

def get_current_third_party_modules(project_root: Path, exclude_modules: Optional[List[str]] = None) -> Set[str]:
    """
    Inspects sys.modules to find currently loaded third-party dependencies.
    This is useful for the initial state when reqtracker.track() is called.
    """
    if exclude_modules is None:
        exclude_modules = []

    loaded_dependencies = set()

    for module_name, module in sys.modules.items():
        if module_name.startswith('_') or '.' in module_name:
            continue

        if is_third_party_module(module_name, project_root) and \
           module_name not in exclude_modules:
            loaded_dependencies.add(module_name)

    return loaded_dependencies


def filter_dependencies(
    raw_dependencies: Set[str],
    exclude_modules: Optional[List[str]] = None,
) -> Set[str]:
    """
    Filters a set of raw dependencies, primarily by user-defined exclude_modules.
    Standard library and built-in filtering should primarily happen during collection.
    """
    if exclude_modules is None:
        exclude_modules = []

    return {dep for dep in raw_dependencies if dep not in exclude_modules}
