#!/usr/bin/env python3
"""
Flask Application Dependency Tracking Example.

This example demonstrates how to use reqtracker with Flask applications,
including blueprints, extensions, and deployment scenarios.
"""

import reqtracker
from reqtracker import Config, TrackerMode


def basic_flask_analysis():
    """Basic Flask application analysis."""
    print("=== Basic Flask Analysis ===")

    try:
        packages = reqtracker.track(["./app"], mode="hybrid")
        print(f"Found Flask dependencies: {packages}")
    except Exception as e:
        print(f"Example Flask tracking: {e}")


def flask_project_structure():
    """Analyze typical Flask project structure."""
    print("\n=== Flask Project Structure Analysis ===")

    # Typical Flask project structure
    flask_paths = [
        "./app",  # Main application
        "./app/models",  # Database models
        "./app/views",  # View functions
        "./app/blueprints",  # Flask blueprints
        "./app/utils",  # Utility functions
        "./config.py",  # Configuration
        "./run.py",  # Application runner
    ]

    all_dependencies = set()

    for path in flask_paths:
        component = path.split("/")[-1] or "root"
        print(f"\nAnalyzing {component}:")
        try:
            packages = reqtracker.track([path], mode="static")
            if packages:
                print(f"  Dependencies: {packages}")
                all_dependencies.update(packages)
            else:
                print("  No external dependencies")
        except Exception as e:
            print(f"  Path {path} not found: {e}")

    print(f"\nTotal Flask project dependencies: {all_dependencies}")


def flask_with_blueprints():
    """Analyze Flask app with blueprints."""
    print("\n=== Flask with Blueprints ===")

    # Flask blueprint analysis
    blueprint_config = Config(
        mode=TrackerMode.HYBRID,
        include_patterns=["*.py"],
        exclude_patterns=[
            "*_test.py",
            "test_*.py",
            "*/tests/*",
            "*/test/*",
            "tests/**/*",
            "static/**/*",
            "templates/**/*",
            "instance/**/*",
            "__pycache__/**/*",
            ".git/**/*",
            "venv/**/*",
            "env/**/*",
        ],
    )

    try:
        packages = reqtracker.track(["./app"], config=blueprint_config)
        print(f"Flask app with blueprints: {packages}")
    except Exception as e:
        print(f"Flask blueprints analysis: {e}")


def flask_environments():
    """Generate requirements for different Flask environments."""
    print("\n=== Flask Environment Requirements ===")

    environments = {
        "base": {
            "description": "Core Flask dependencies",
            "paths": ["./app/models", "./app/views", "./config.py"],
            "strategy": "compatible",
        },
        "development": {
            "description": "Development dependencies",
            "paths": ["./app", "./tests", "./run.py"],
            "strategy": "compatible",
        },
        "production": {
            "description": "Production dependencies",
            "paths": ["./app", "./config.py"],
            "strategy": "exact",
        },
        "testing": {
            "description": "Testing dependencies",
            "paths": ["./app", "./tests"],
            "strategy": "compatible",
        },
    }

    for env_name, env_config in environments.items():
        print(f"\n{env_name.title()} environment:")
        try:
            packages = reqtracker.track(env_config["paths"], mode="static")

            if packages:
                reqtracker.generate(
                    packages=packages,
                    output=f"requirements/{env_name}.txt",
                    version_strategy=env_config["strategy"],
                )
                print(f"  Generated requirements/{env_name}.txt")
                print(f"  {len(packages)} packages")
                print(f"  Strategy: {env_config['strategy']}")
            else:
                print("  No dependencies found")

        except Exception as e:
            print(f"  Error: {e}")


def flask_api_analysis():
    """Analyze Flask API dependencies."""
    print("\n=== Flask API Analysis ===")

    # API-specific patterns
    api_config = Config(
        mode=TrackerMode.HYBRID,
        include_patterns=["*.py"],
        exclude_patterns=["test_*.py", "*_test.py", "*/tests/*"],
    )

    api_components = [
        "./app/api",  # API blueprints
        "./app/models",  # Database models
        "./app/serializers",  # Data serialization
        "./app/auth",  # Authentication
        "./app/utils",  # Utilities
    ]

    try:
        packages = reqtracker.track(api_components, config=api_config)
        print(f"Flask API dependencies: {packages}")

        # Generate API-specific requirements
        if packages:
            reqtracker.generate(
                packages=packages,
                output="requirements/api.txt",
                version_strategy="compatible",
                include_header=True,
            )
            print("Generated requirements/api.txt for Flask API")

    except Exception as e:
        print(f"Flask API analysis: {e}")


def flask_cli_examples():
    """Show CLI examples for Flask projects."""
    print("\n=== Flask CLI Examples ===")

    cli_examples = [
        "# Basic Flask app analysis",
        "reqtracker analyze ./app",
        "",
        "# Exclude test files and static content",
        (
            "reqtracker analyze ./app --mode hybrid "
            "--version-strategy compatible "
            "--exclude-patterns '*/tests/*' --output requirements/base.txt"
        ),
        "",
        "# Production requirements with exact versions",
        (
            "reqtracker generate --version-strategy exact "
            "--output requirements/production.txt"
        ),
        "",
        "# Development environment",
        (
            "reqtracker analyze . --exclude-dirs instance migrations "
            "--output requirements/dev.txt"
        ),
        "",
        "# API-only dependencies",
        "reqtracker track ./app/api ./app/models --mode static",
        "",
        "# Flask with custom config",
        "reqtracker analyze --config flask.reqtracker.toml",
        "",
        "# Quick deployment check",
        "reqtracker track ./app --mode static --quiet",
    ]

    for example in cli_examples:
        print(example)


def flask_deployment_tips():
    """Deployment tips for Flask applications."""
    print("\n=== Flask Deployment Tips ===")

    tips = [
        "Deployment Best Practices:",
        "",
        "1. Use exact versions in production:",
        " reqtracker generate --version-strategy exact "
        "--output requirements/prod.txt",
        "",
        "2. Separate requirements by environment:",
        " - requirements/base.txt (core dependencies)",
        " - requirements/dev.txt (development tools)",
        " - requirements/prod.txt (production-ready)",
        "",
        "3. Exclude unnecessary files:",
        " - Test files and directories",
        " - Static files and templates",
        " - Migration files",
        " - Instance configuration",
        "",
        "4. Use static mode for production:",
        " reqtracker analyze --mode static ./app",
        "",
        "5. Integrate with CI/CD:",
        " - Run reqtracker in your deployment pipeline",
        " - Compare requirements before deployment",
        " - Update requirements automatically",
    ]

    for tip in tips:
        print(tip)


if __name__ == "__main__":
    print("Flask Application Dependency Tracking")
    print("=" * 40)

    basic_flask_analysis()
    flask_project_structure()
    flask_with_blueprints()
    flask_environments()
    flask_api_analysis()
    flask_cli_examples()
    flask_deployment_tips()

    print("\n=== Flask Examples Complete ===")
    print("\nNext steps:")
    print("1. Adapt the configuration patterns to your Flask project structure")
    print("2. Set up environment-specific requirements files")
    print("3. Configure your deployment pipeline to use reqtracker")
    print("4. Check out the config examples in ../config_examples/")
