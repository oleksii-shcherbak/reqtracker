#!/usr/bin/env python3
"""
Basic reqtracker usage examples.

This script demonstrates the most common ways to use reqtracker
as a Python library for dependency tracking and requirements generation.
"""

from pathlib import Path

import reqtracker


def basic_usage():
    """Demonstrate basic reqtracker functionality."""
    print("=== Basic reqtracker Usage ===")

    # 1. Simple dependency tracking
    print("\n1. Track dependencies in current directory:")
    packages = reqtracker.track()
    print(f"Found packages: {packages}")

    # 2. Track specific directories
    print("\n2. Track dependencies in specific paths:")
    # Note: These paths may not exist in this example
    example_paths = ["../web_development", "../data_science"]
    try:
        packages = reqtracker.track(example_paths)
        print(f"Found packages: {packages}")
    except Exception as e:
        print(f"Example paths don't exist: {e}")

    # 3. Generate requirements.txt
    print("\n3. Generate requirements.txt:")
    try:
        content = reqtracker.generate()
        print("Generated requirements.txt content:")
        print(content[:200] + "..." if len(content) > 200 else content)
    except Exception as e:
        print(f"Generation example: {e}")


def different_modes():
    """Demonstrate different analysis modes."""
    print("\n=== Different Analysis Modes ===")

    # Static analysis (AST-based)
    print("\n1. Static analysis (AST-based):")
    try:
        packages = reqtracker.track(mode="static")
        print(f"Static analysis found: {packages}")
    except Exception as e:
        print(f"Static analysis: {e}")

    # Dynamic analysis (runtime)
    print("\n2. Dynamic analysis (runtime):")
    try:
        packages = reqtracker.track(mode="dynamic")
        print(f"Dynamic analysis found: {packages}")
    except Exception as e:
        print(f"Dynamic analysis: {e}")

    # Hybrid analysis (default)
    print("\n3. Hybrid analysis (combines both):")
    try:
        packages = reqtracker.track(mode="hybrid")
        print(f"Hybrid analysis found: {packages}")
    except Exception as e:
        print(f"Hybrid analysis: {e}")


def version_strategies():
    """Demonstrate different version strategies."""
    print("\n=== Version Strategies ===")

    # Mock some packages for demonstration
    demo_packages = {"requests", "numpy", "pandas"}

    strategies = ["exact", "compatible", "minimum", "none"]

    for strategy in strategies:
        print(f"\n{strategy.title()} version strategy:")
        try:
            content = reqtracker.generate(
                packages=demo_packages,
                version_strategy=strategy,
                output="demo_requirements.txt",
            )
            # Show first few lines
            lines = content.split("\n")[:3]
            for line in lines:
                if line.strip():
                    print(f"  {line}")
        except Exception as e:
            print(f"  Error with {strategy}: {e}")


def complete_workflow():
    """Demonstrate the complete workflow."""
    print("\n=== Complete Workflow ===")

    print("\nUsing reqtracker.analyze() for complete workflow:")
    try:
        packages = reqtracker.analyze(
            output="example_requirements.txt",
            mode="hybrid",
            version_strategy="compatible",
        )
        print(f"Complete workflow found packages: {packages}")

        # Check if file was created
        if Path("example_requirements.txt").exists():
            print("example_requirements.txt was created successfully!")
            # Clean up
            Path("example_requirements.txt").unlink()

    except Exception as e:
        print(f"Complete workflow: {e}")


def custom_configuration():
    """Demonstrate custom configuration usage."""
    print("\n=== Custom Configuration ===")

    try:
        from reqtracker import Config, TrackerMode

        # Create custom config
        config = Config(
            mode=TrackerMode.STATIC,
            include_patterns=["*.py"],
            exclude_patterns=[
                "test_*.py",
                "*_test.py",
                "tests/**/*",
                "docs/**/*",
                "__pycache__/**/*",
            ],
        )

        print("\nUsing custom configuration:")
        packages = reqtracker.track(config=config)
        print(f"Custom config found: {packages}")

    except Exception as e:
        print(f"Custom configuration: {e}")


if __name__ == "__main__":
    print("reqtracker Basic Usage Examples")
    print("=" * 40)

    # Run all examples
    basic_usage()
    different_modes()
    version_strategies()
    complete_workflow()
    custom_configuration()

    print("\n=== Examples Complete ===")
    print("\nNext steps:")
    print("- Try the CLI examples: bash cli_examples.sh")
    print("- Explore web development examples in ../web_development/")
    print("- Check out data science examples in ../data_science/")
    print("- Review configuration templates in ../config_examples/")
