# reqtracker/output.py
from typing import Set
from pathlib import Path


def write_requirements_file(dependencies: Set[str], output_path: Path) -> None:
    """
    Writes a set of dependencies to a requirements.txt file.

    :param dependencies: A set of dependency names.
    :param output_path: The Path object for the output file.
    """
    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            for dep in sorted(list(dependencies)):
                f.write(f"{dep}\n")
        print(f"Successfully wrote {len(dependencies)} dependencies to '{output_path}'.")
    except IOError as e:
        print(f"Error: Could not write to requirements file '{output_path}'. Error: {e}")


def print_dependencies(dependencies: Set[str]) -> None:
    """
    Prints a set of dependencies to the console.

    :param dependencies: A set of dependency names.
    """
    print("\n--- Detected Dependencies ---")
    if not dependencies:
        print("No third-party dependencies found.")
    else:
        for dep in sorted(list(dependencies)):
            print(dep)
    print("-----------------------------\n")
