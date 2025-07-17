# reqtracker/__init__.py

from typing import Set, List, Optional, Dict, Any

from .config import ReqtrackerConfig
from .core import find_dependencies_static, get_current_third_party_modules, filter_dependencies
from .output import write_requirements_file, print_dependencies
from .tracker import enable_dynamic_tracking, disable_dynamic_tracking, get_tracked_modules, clear_tracked_modules
from .exceptions import ReqtrackerError

__version__ = "0.1.0"

class Reqtracker:
    """
    The main class for reqtracker, managing dependency tracking.
    Orchestrates static analysis, dynamic runtime tracking, and output.
    """
    def __init__(self, config: ReqtrackerConfig):
        """
        Initializes the Reqtracker instance with a given configuration.

        :param config: An instance of ReqtrackerConfig.
        """
        self.config = config
        self._initial_loaded_modules: Set[str] = set()

    def _prepare_tracking(self) -> None:
        """
        Prepares the environment for dependency tracking.
        Clears previous tracking state, collects initially loaded modules,
        and enables dynamic import interception.
        """
        clear_tracked_modules()

        self._initial_loaded_modules = get_current_third_party_modules(
            project_root=self.config.project_root,
            exclude_modules=self.config.exclude_modules
        )

        enable_dynamic_tracking(
            project_root=self.config.project_root,
            exclude_modules=self.config.exclude_modules
        )

    def _finalize_tracking(self) -> Set[str]:
        """
        Finalizes tracking, disables dynamic interception, and consolidates
        dependencies from static analysis, initially loaded modules, and
        dynamically tracked imports.

        :return: A set of unique, filtered third-party dependency names.
        """
        disable_dynamic_tracking()

        dynamically_tracked = get_tracked_modules()

        all_found_dependencies = set()

        static_deps = find_dependencies_static(
            project_root=str(self.config.project_root),
            ignore_paths=self.config.ignore_paths,
            exclude_modules=self.config.exclude_modules
        )
        all_found_dependencies.update(static_deps)

        all_found_dependencies.update(self._initial_loaded_modules)

        all_found_dependencies.update(dynamically_tracked)

        final_dependencies = filter_dependencies(
            all_found_dependencies,
            exclude_modules=self.config.exclude_modules
        )

        return final_dependencies

    def track(self) -> None:
        """
        Initiates and manages the dependency tracking process.
        This method should be called early in the user's main script
        to capture all relevant imports.
        """
        if not self.config.project_root.exists():
            raise ReqtrackerError(f"Project root does not exist: {self.config.project_root}")

        print(f"Reqtracker: Starting dependency tracking for project: {self.config.project_root}")

        try:
            self._prepare_tracking()
        except Exception as e:
            disable_dynamic_tracking()
            raise ReqtrackerError(f"Error during Reqtracker preparation: {e}") from e
        finally:
            try:
                final_dependencies = self._finalize_tracking()

                if self.config.output_to_file:
                    write_requirements_file(
                        dependencies=final_dependencies,
                        output_path=self.config.output_file
                    )
                    print(f"Reqtracker: Dependencies written to {self.config.output_file}")

                if self.config.print_to_console:
                    print_dependencies(final_dependencies)

                print("Reqtracker: Dependency tracking complete.")

            except Exception as e:
                raise ReqtrackerError(f"Error during Reqtracker finalization or output: {e}") from e

_global_reqtracker_instance: Optional[Reqtracker] = None

def track(
    project_root: str = ".",
    output_file: str = "requirements.txt",
    output_to_file: bool = True,
    print_to_console: bool = False,
    ignore_paths: Optional[List[str]] = None,
    exclude_modules: Optional[List[str]] = None,
    mode: str = "hybrid",
    include_dev: bool = False
) -> None:
    """
    Main entry point to run Reqtracker's dependency tracking.

    :param project_root: The root directory of the project to scan. Defaults to current directory.
    :param output_file: The path to the output requirements file. Defaults to 'requirements.txt'.
    :param output_to_file: Whether to write dependencies to a file. Defaults to True.
    :param print_to_console: Whether to print dependencies to the console. Defaults to False.
    :param ignore_paths: List of paths (relative to project_root) to ignore during static analysis.
    :param exclude_modules: List of module names to exclude from the final dependency list.
    :param mode: The tracking mode ('static', 'dynamic', 'hybrid'). Defaults to 'hybrid'.
    :param include_dev: Whether to include development dependencies. Defaults to False.
    """
    global _global_reqtracker_instance

    if _global_reqtracker_instance is not None:
        disable_dynamic_tracking()
        clear_tracked_modules()

    try:
        inline_overrides: Dict[str, Any] = {
            "output_file": output_file,
            "output_to_file": output_to_file,
            "print_to_console": print_to_console,
            "ignore_paths": ignore_paths,
            "exclude_modules": exclude_modules,
            "mode": mode,
            "include_dev": include_dev,
        }

        config = ReqtrackerConfig(
            project_root=project_root,
            inline_overrides=inline_overrides
        )

        _global_reqtracker_instance = Reqtracker(config)
        _global_reqtracker_instance.track()
    except ReqtrackerError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        pass
