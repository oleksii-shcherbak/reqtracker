# reqtracker/output.py

from pathlib import Path
from typing import List

def write_requirements_file(filepath: str, dependencies: List[str]) -> None:
    """
    Writes a list of dependencies to a requirements file.

    Args:
        filepath (str): The path to the requirements file (e.g., "requirements.txt").
        dependencies (List[str]): A sorted list of dependency names (e.g., ["numpy", "pandas"]).
    """
    try:
        output_path = Path(filepath)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w') as f:
            for dep in dependencies:
                f.write(f"{dep}\n")
        print(f"Successfully wrote {len(dependencies)} dependencies to '{filepath}'.")
    except IOError as e:
        print(f"Error: Could not write to requirements file '{filepath}'. {e}")
