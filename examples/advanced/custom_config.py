#!/usr/bin/env python3
"""
Advanced reqtracker Configuration Example.

This example demonstrates advanced configuration options,
custom import mappings, and programmatic usage patterns.
"""

import reqtracker
from reqtracker import Config, RequirementsGenerator, TrackerMode, VersionStrategy


def create_custom_config():
    """Create and use custom configuration."""
    print("=== Custom Configuration ===")

    # Create highly customized configuration
    custom_config = Config(
        mode=TrackerMode.HYBRID,
        include_patterns=["*.py", "scripts/*.py", "src/**/*.py"],
        exclude_patterns=[
            "test_*.py",
            "*_test.py",
            "*/tests/*",
            "**/test_*.py",
            "setup.py",
            "conftest.py",
            "tests/**/*",
            "test/**/*",
            "docs/**/*",
            "documentation/**/*",
            "examples/**/*",
            "demo/**/*",
            "__pycache__/**/*",
            ".git/**/*",
            ".github/**/*",
            "venv/**/*",
            ".venv/**/*",
            "env/**/*",
            ".env/**/*",
            "node_modules/**/*",
            "dist/**/*",
            "build/**/*",
        ],
    )

    try:
        packages = reqtracker.track(config=custom_config)
        print(f"Custom config found: {packages}")
    except Exception as e:
        print(f"Custom config example: {e}")

    return custom_config


def custom_import_mappings():
    """Demonstrate custom import mappings."""
    print("\n=== Custom Import Mappings ===")

    # Load default config and add custom mappings
    Config()

    # Add custom mappings (this would normally be done via TOML config)
    custom_mappings = {
        "cv2": "opencv-python",
        "sklearn": "scikit-learn",
        "PIL": "Pillow",
        "yaml": "PyYAML",
        "dotenv": "python-dotenv",
        "jwt": "PyJWT",
        "psycopg2": "psycopg2-binary",
        "mysql": "PyMySQL",
        "redis": "redis",
        "celery": "celery",
        "requests": "requests",
        "httpx": "httpx",
    }

    print("Custom import mappings:")
    for import_name, package_name in custom_mappings.items():
        print(f"  {import_name} -> {package_name}")

    print("\nNote: Add these to .reqtracker.toml:")
    print("[tool.reqtracker.import_mappings]")
    for import_name, package_name in custom_mappings.items():
        print(f'{import_name} = "{package_name}"')


def programmatic_requirements_generation():
    """Advanced programmatic requirements generation."""
    print("\n=== Programmatic Requirements Generation ===")

    # Track dependencies first
    try:
        packages = reqtracker.track(["./src"], mode="static")

        if not packages:
            # Use demo packages for illustration
            packages = {"requests", "numpy", "pandas", "flask", "pytest"}
            print("Using demo packages for illustration")

        print(f"Working with packages: {packages}")

        # Generate different requirement files programmatically
        generators = {
            "exact": VersionStrategy.EXACT,
            "compatible": VersionStrategy.COMPATIBLE,
            "minimum": VersionStrategy.MINIMUM,
            "none": VersionStrategy.NONE,
        }

        for strategy_name, strategy in generators.items():
            generator = RequirementsGenerator(strategy)

            content = generator.generate(
                packages=packages,
                output_file=f"requirements_{strategy_name}.txt",
                include_header=True,
                sort_packages=True,
            )

            print(f"\n{strategy_name.title()} strategy output (first 3 lines):")
            lines = content.split("\n")[:3]
            for line in lines:
                if line.strip():
                    print(f"  {line}")

    except Exception as e:
        print(f"Programmatic generation: {e}")


def conditional_requirements():
    """Generate conditional requirements based on environment."""
    print("\n=== Conditional Requirements ===")

    # Simulate different environments
    environments = {
        "development": {
            "paths": ["./src", "./tests", "./scripts"],
            "strategy": "compatible",
            "extra_packages": {"pytest", "black", "flake8", "mypy"},
        },
        "production": {
            "paths": ["./src"],
            "strategy": "exact",
            "extra_packages": {"gunicorn", "psycopg2-binary"},
        },
        "testing": {
            "paths": ["./src", "./tests"],
            "strategy": "compatible",
            "extra_packages": {"pytest", "pytest-cov", "factory-boy"},
        },
    }

    for env_name, env_config in environments.items():
        print(f"\n{env_name.title()} environment:")

        try:
            # Track base dependencies
            base_packages = reqtracker.track(env_config["paths"], mode="static")

            # Add environment-specific packages
            all_packages = (base_packages or set()) | env_config["extra_packages"]

            # Generate requirements
            reqtracker.generate(
                packages=all_packages,
                output=f"requirements/{env_name}.txt",
                version_strategy=env_config["strategy"],
                include_header=True,
            )

            print(f"  {len(all_packages)} total packages")
            print(f"  Strategy: {env_config['strategy']}")
            print(f"  Output: requirements/{env_name}.txt")

        except Exception as e:
            print(f"  Error: {e}")


def project_analysis():
    """Analyze project structure and provide insights."""
    print("\n=== Project Analysis ===")

    project_components = {
        "Core Application": ["./src/app", "./src/core"],
        "API Layer": ["./src/api", "./src/views"],
        "Database Models": ["./src/models", "./src/db"],
        "Utilities": ["./src/utils", "./src/helpers"],
        "Configuration": ["./config", "./settings"],
        "Scripts": ["./scripts", "./bin"],
        "Tests": ["./tests"],
    }

    all_deps = set()
    component_deps = {}

    for component, paths in project_components.items():
        try:
            deps = reqtracker.track(paths, mode="static")
            if deps:
                component_deps[component] = deps
                all_deps.update(deps)
                print(f"\n{component}: {len(deps)} dependencies")
                print(f"  {', '.join(sorted(deps))}")
            else:
                print(f"\n{component}: No external dependencies")
        except FileNotFoundError:
            print(f"\n{component}: Component not found")

    print("\nProject Analysis Summary:")
    print(f"  Total unique dependencies: {len(all_deps)}")
    print(f"  Components with dependencies: {len(component_deps)}")

    # Find common dependencies
    if len(component_deps) > 1:
        common_deps = set.intersection(*component_deps.values())
        if common_deps:
            print(f"  Common dependencies: {', '.join(sorted(common_deps))}")


def integration_examples():
    """Show integration with other tools."""
    print("\n=== Integration Examples ===")

    integration_patterns = [
        "# Docker integration",
        "# In Dockerfile:",
        "RUN pip install reqtracker",
        "COPY . .",
        "RUN reqtracker analyze --output requirements.txt " "--version-strategy exact",
        "RUN pip install -r requirements.txt",
        "",
        "# Pre-commit hook integration",
        "# In .pre-commit-config.yaml:",
        "repos:",
        "  - repo: local",
        "    hooks:",
        "      - id: reqtracker",
        "        name: Update requirements",
        "        entry: reqtracker analyze",
        "        language: system",
        "        files: '^.*\\.py$'",
        "",
        "# Makefile integration",
        "# In Makefile:",
        "requirements:",
        "\trequirements = reqtracker analyze --output requirements.txt",
        "",
        "requirements-dev:",
        "\trequirements = reqtracker analyze --output requirements-dev.txt "
        "--include-dirs tests",
        "",
        "# tox integration",
        "# In tox.ini:",
        "[testenv:requirements]",
        "deps = reqtracker",
        "commands = reqtracker analyze --output {toxinidir}/requirements.txt",
    ]

    for pattern in integration_patterns:
        print(pattern)


if __name__ == "__main__":
    print("Advanced reqtracker Configuration Examples")
    print("=" * 50)

    custom_config = create_custom_config()
    custom_import_mappings()
    programmatic_requirements_generation()
    conditional_requirements()
    project_analysis()
    integration_examples()

    print("\n=== Advanced Examples Complete ===")
    print("\nKey takeaways:")
    print("1. Customize configuration for your specific project needs")
    print("2. Use programmatic API for complex workflows")
    print("3. Generate environment-specific requirements")
    print("4. Integrate reqtracker into your development tools")
    print("5. Analyze project structure for dependency insights")
