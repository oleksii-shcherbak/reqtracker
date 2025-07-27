#!/usr/bin/env python3
"""
Jupyter Notebook Dependency Tracking Example.

This example shows how to use reqtracker with Jupyter notebooks
and data science projects that mix .py and .ipynb files.
"""

import reqtracker
from reqtracker import Config, TrackerMode


def notebook_dependency_tracking():
    """Track dependencies in Jupyter notebooks."""
    print("=== Jupyter Notebook Dependency Tracking ===")

    # Note: reqtracker primarily works with .py files
    # For notebooks, export to .py first or use dynamic tracking

    try:
        # Dynamic tracking works well with notebook environments
        packages = reqtracker.track(["./notebooks"], mode="dynamic")
        print(f"Notebook dependencies (dynamic): {packages}")
    except Exception as e:
        print(f"Notebook tracking: {e}")


def data_science_project():
    """Analyze a complete data science project."""
    print("\n=== Data Science Project Analysis ===")

    # Typical data science project structure
    ds_config = Config(
        mode=TrackerMode.HYBRID,
        include_patterns=["*.py"],
        exclude_patterns=[
            "*_test.py",
            "test_*.py",
            "*/tests/*",
            "*.ipynb_checkpoints/*",
            "*/.ipynb_checkpoints/*",
            "tests/**/*",
            "data/**/*",
            "outputs/**/*",
            "models/**/*",
            "plots/**/*",
            ".ipynb_checkpoints/**/*",
            "__pycache__/**/*",
            ".git/**/*",
        ],
    )

    ds_components = [
        "./src",  # Source code
        "./scripts",  # Analysis scripts
        "./notebooks",  # Jupyter notebooks (exported .py)
        "./utils",  # Utility functions
        "./pipeline",  # ML pipeline code
    ]

    try:
        packages = reqtracker.track(ds_components, config=ds_config)
        print(f"Data science project dependencies: {packages}")
    except Exception as e:
        print(f"Data science analysis: {e}")


def ml_pipeline_requirements():
    """Generate requirements for ML pipeline stages."""
    print("\n=== ML Pipeline Requirements ===")

    pipeline_stages = {
        "data_processing": {
            "paths": ["./src/data", "./scripts/preprocessing"],
            "description": "Data cleaning and preprocessing",
        },
        "feature_engineering": {
            "paths": ["./src/features", "./notebooks/feature_engineering.py"],
            "description": "Feature creation and selection",
        },
        "model_training": {
            "paths": ["./src/models", "./scripts/train.py"],
            "description": "Model training and validation",
        },
        "inference": {
            "paths": ["./src/inference", "./api"],
            "description": "Model serving and inference",
        },
    }

    all_ml_deps = set()

    for stage, config in pipeline_stages.items():
        print(f"\n{stage.replace('_', ' ').title()}:")
        try:
            packages = reqtracker.track(config["paths"], mode="static")
            if packages:
                print(f"  Dependencies: {packages}")
                all_ml_deps.update(packages)

                # Generate stage-specific requirements
                reqtracker.generate(
                    packages=packages,
                    output=f"requirements/{stage}.txt",
                    version_strategy="compatible",
                )
                print(f"  Generated requirements/{stage}.txt")
            else:
                print("  No dependencies found")
        except Exception as e:
            print(f"  Error: {e}")

    print(f"\nAll ML pipeline dependencies: {all_ml_deps}")


def research_vs_production():
    """Compare research and production requirements."""
    print("\n=== Research vs Production Requirements ===")

    environments = {
        "research": {
            "paths": ["./notebooks", "./experiments", "./research"],
            "strategy": "minimum",  # Flexible for research
            "description": "Research and experimentation",
        },
        "production": {
            "paths": ["./src", "./api", "./pipeline"],
            "strategy": "exact",  # Strict for production
            "description": "Production ML system",
        },
    }

    for env, config in environments.items():
        print(f"\n{env.title()} Environment:")
        try:
            packages = reqtracker.track(config["paths"], mode="static")

            if packages:
                reqtracker.generate(
                    packages=packages,
                    output=f"requirements/{env}.txt",
                    version_strategy=config["strategy"],
                    include_header=True,
                )
                print(f"  {len(packages)} packages")
                print(f"  Strategy: {config['strategy']}")
                print(f"  File: requirements/{env}.txt")
            else:
                print("  No dependencies found")

        except Exception as e:
            print(f"  Error: {e}")


def notebook_cli_examples():
    """CLI examples for notebook environments."""
    print("\n=== Notebook CLI Examples ===")

    examples = [
        "# Track notebook dependencies (dynamic mode recommended)",
        "reqtracker track ./notebooks --mode dynamic",
        "",
        "# Analyze data science project",
        "reqtracker analyze ./src --exclude-dirs data outputs models plots",
        "",
        "# Research environment (flexible versions)",
        "reqtracker generate --version-strategy minimum \\",
        " --output requirements/research.txt",
        "",
        "# Production ML system (exact versions)",
        "reqtracker analyze ./src --mode static --version-strategy exact \\",
        " --output requirements/production.txt",
        "",
        "# Quick notebook dependency check",
        "reqtracker track . --mode dynamic --quiet",
        "",
        "# Exclude data and output directories",
        "reqtracker analyze . --exclude-dirs data outputs models .ipynb_checkpoints",
    ]

    for example in examples:
        print(example)


if __name__ == "__main__":
    print("Jupyter Notebook Dependency Tracking")
    print("=" * 40)

    notebook_dependency_tracking()
    data_science_project()
    ml_pipeline_requirements()
    research_vs_production()
    notebook_cli_examples()

    print("\n=== Notebook Examples Complete ===")
    print("\nTips for Jupyter notebooks:")
    print("1. Use dynamic mode for active notebook sessions")
    print("2. Export notebooks to .py files for static analysis")
    print("3. Separate research and production requirements")
    print("4. Exclude data directories and model outputs")
    print("5. Use minimum versions for research flexibility")
