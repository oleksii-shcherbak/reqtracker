#!/usr/bin/env python3
"""
Django Project Dependency Tracking Example.

This example shows how to use reqtracker with Django projects,
handling common Django-specific patterns and exclusions.
"""

import reqtracker
from reqtracker import Config, TrackerMode


def basic_django_analysis():
    """Basic Django project analysis."""
    print("=== Basic Django Analysis ===")

    # Simple Django project tracking
    try:
        packages = reqtracker.track(["./myproject"], mode="hybrid")
        print(f"Found Django dependencies: {packages}")
    except Exception as e:
        print(f"Example Django tracking: {e}")


def django_with_exclusions():
    """Django analysis with common exclusions."""
    print("\n=== Django with Smart Exclusions ===")

    # Create Django-specific configuration
    django_config = Config(
        mode=TrackerMode.HYBRID,
        include_patterns=["*.py"],
        exclude_patterns=[
            "*/migrations/*",  # Exclude migration files
            "*_test.py",  # Exclude test files
            "test_*.py",  # Exclude test files
            "*/tests/*",  # Exclude test directories
            "manage.py",  # Often exclude manage.py
            "*/settings/local.py",  # Local settings
            "*/static/*",  # Static files
            "*/media/*",  # Media files
            "migrations/**/*",
            "tests/**/*",
            "static/**/*",
            "media/**/*",
            "locale/**/*",
            "__pycache__/**/*",
            ".git/**/*",
            "venv/**/*",
            "env/**/*",
        ],
    )

    try:
        packages = reqtracker.track(["./myproject"], config=django_config)
        print(f"Django packages (with exclusions): {packages}")
    except Exception as e:
        print(f"Django with exclusions: {e}")


def django_requirements_separation():
    """Generate separate requirements files for Django."""
    print("\n=== Django Requirements Separation ===")

    # Common Django pattern: separate requirements files
    requirements_types = {
        "base": {
            "description": "Core dependencies",
            "strategy": "compatible",
            "paths": ["./myproject/core", "./myproject/apps"],
        },
        "development": {
            "description": "Development dependencies",
            "strategy": "compatible",
            "paths": ["./myproject", "./tests"],
        },
        "production": {
            "description": "Production dependencies",
            "strategy": "exact",
            "paths": ["./myproject/core", "./myproject/apps"],
        },
    }

    for req_type, config in requirements_types.items():
        print(f"\n{req_type.title()} requirements:")
        try:
            packages = reqtracker.track(config["paths"], mode="static")
            reqtracker.generate(
                packages=packages,
                output=f"requirements/{req_type}.txt",
                version_strategy=config["strategy"],
                include_header=True,
            )
            print(f"  Generated requirements/{req_type}.txt")
            print(f"  Strategy: {config['strategy']}")
            print(f"  Packages: {len(packages) if packages else 0}")
        except Exception as e:
            print(f"  Error: {e}")


def django_apps_analysis():
    """Analyze individual Django apps."""
    print("\n=== Django Apps Analysis ===")

    # Analyze individual Django apps
    django_apps = [
        "./myproject/apps/users",
        "./myproject/apps/blog",
        "./myproject/apps/api",
        "./myproject/core",
    ]

    all_dependencies = set()

    for app_path in django_apps:
        app_name = app_path.split("/")[-1]
        print(f"\nAnalyzing app: {app_name}")
        try:
            packages = reqtracker.track([app_path], mode="static")
            if packages:
                print(f"  Dependencies: {packages}")
                all_dependencies.update(packages)
            else:
                print("  No external dependencies found")
        except Exception as e:
            print(f"  Error analyzing {app_name}: {e}")

    print(f"\nAll Django project dependencies: {all_dependencies}")


def django_deployment_requirements():
    """Generate deployment-ready requirements."""
    print("\n=== Django Deployment Requirements ===")

    # Production deployment configuration
    production_config = Config(
        mode=TrackerMode.STATIC,  # Static for reproducible builds
        include_patterns=["*.py"],
        exclude_patterns=[
            "*/migrations/*",
            "*_test.py",
            "test_*.py",
            "*/tests/*",
            "*/local_settings.py",
            "*/dev_settings.py",
            "manage.py",
            "tests/**/*",
            "migrations/**/*",
            "static/**/*",
            "media/**/*",
            "locale/**/*",
            "docs/**/*",
            "__pycache__/**/*",
        ],
    )

    try:
        # Generate production requirements
        packages = reqtracker.track(["./myproject"], config=production_config)

        # Create production requirements with exact versions
        reqtracker.generate(
            packages=packages,
            output="requirements/production.txt",
            version_strategy="exact",
            include_header=True,
            sort_packages=True,
        )

        print("Generated production requirements:")
        print("File: requirements/production.txt")
        print(f"Packages: {len(packages) if packages else 0}")
        print("Strategy: exact versions for reproducible builds")

    except Exception as e:
        print(f"Production requirements error: {e}")


def django_cli_examples():
    """Show CLI examples for Django projects."""
    print("\n=== Django CLI Examples ===")

    cli_examples = [
        "# Basic Django analysis",
        "reqtracker analyze ./myproject",
        "",
        "# Exclude migrations and tests",
        (
            "reqtracker analyze ./myproject "
            "--exclude-patterns '*/migrations/*' '*/tests/*'"
        ),
        "",
        "# Production requirements with exact versions",
        (
            "reqtracker analyze ./myproject --mode static "
            "--version-strategy exact --output requirements/production.txt"
        ),
        "",
        "# Development requirements",
        (
            "reqtracker analyze . --exclude-dirs static media locale "
            "--output requirements/dev.txt"
        ),
        "",
        "# Analyze specific Django app",
        "reqtracker track ./myproject/apps/users --mode static",
        "",
        "# Use Django-specific config",
        "reqtracker analyze --config .reqtracker.toml",
    ]

    for example in cli_examples:
        print(example)


if __name__ == "__main__":
    print("Django Project Dependency Tracking")
    print("=" * 40)

    basic_django_analysis()
    django_with_exclusions()
    django_requirements_separation()
    django_apps_analysis()
    django_deployment_requirements()
    django_cli_examples()

    print("\n=== Django Examples Complete ===")
    print("\nNext steps:")
    print(
        "1. Copy the Django config template from "
        "../config_examples/django.reqtracker.toml"
    )
    print("2. Customize patterns and paths for your project structure")
    print("3. Set up separate requirements files for different environments")
    print("4. Integrate with your Django deployment pipeline")
