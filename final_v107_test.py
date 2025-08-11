#!/usr/bin/env python3
"""Final comprehensive test for v1.0.7 release."""

import subprocess
import tempfile
from pathlib import Path
import sys

def test_cli_commands():
    """Test all major CLI commands."""
    print("Testing CLI Commands...\n")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("""
import requests
import numpy
import pandas
import matplotlib.pyplot as plt
import reqtracker  # Should be filtered
import os  # Should be filtered
import pyexpat  # Should be filtered
""")
        
        tests_passed = 0
        tests_failed = 0
        
        # Test 1: reqtracker track (default static mode)
        print("1. Testing: reqtracker track")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker track test.py",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            output = result.stdout.strip()
            if "reqtracker" not in output and "os" not in output and "pyexpat" not in output:
                print("   ✓ PASSED - No self-reference or stdlib")
                tests_passed += 1
            else:
                print("   ✗ FAILED - Contains filtered packages")
                tests_failed += 1
        else:
            print(f"   ✗ FAILED - Exit code {result.returncode}")
            tests_failed += 1
        
        # Test 2: reqtracker analyze
        print("2. Testing: reqtracker analyze")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker analyze test.py --output req.txt",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            req_content = (Path(tmpdir) / "req.txt").read_text()
            if "reqtracker" not in req_content and "pyexpat" not in req_content:
                print("   ✓ PASSED - Generated clean requirements.txt")
                tests_passed += 1
            else:
                print("   ✗ FAILED - Contains filtered packages")
                tests_failed += 1
        else:
            print(f"   ✗ FAILED - Exit code {result.returncode}")
            tests_failed += 1
        
        # Test 3: Version strategies
        print("3. Testing: Version strategies")
        for strategy in ["--exact", "--minimum", "--no-versions"]:
            result = subprocess.run(
                f"cd {tmpdir} && reqtracker generate {strategy} --output test_{strategy}.txt",
                shell=True, capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"   ✓ {strategy} works")
                tests_passed += 1
            else:
                print(f"   ✗ {strategy} failed")
                tests_failed += 1
        
        # Test 4: Static mode explicitly
        print("4. Testing: --mode static")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker track --mode static test.py",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            print("   ✓ PASSED - Static mode works")
            tests_passed += 1
        else:
            print("   ✗ FAILED")
            tests_failed += 1
        
        print(f"\nCLI Tests: {tests_passed} passed, {tests_failed} failed\n")
        return tests_failed == 0

def test_python_api():
    """Test Python API functionality."""
    print("Testing Python API...\n")
    
    tests_passed = 0
    tests_failed = 0
    
    try:
        import reqtracker
        
        # Test 1: Basic track
        print("1. Testing: reqtracker.track()")
        packages = reqtracker.track()
        if isinstance(packages, set):
            print("   ✓ PASSED - Returns set")
            tests_passed += 1
        else:
            print("   ✗ FAILED - Wrong return type")
            tests_failed += 1
        
        # Test 2: Generate
        print("2. Testing: reqtracker.generate()")
        content = reqtracker.generate()
        if isinstance(content, str) and "# Requirements generated" in content:
            print("   ✓ PASSED - Generates content")
            tests_passed += 1
        else:
            print("   ✗ FAILED")
            tests_failed += 1
        
        # Test 3: Analyze
        print("3. Testing: reqtracker.analyze()")
        packages = reqtracker.analyze(output="test_api.txt")
        if Path("test_api.txt").exists():
            print("   ✓ PASSED - Creates file")
            Path("test_api.txt").unlink()
            tests_passed += 1
        else:
            print("   ✗ FAILED")
            tests_failed += 1
        
    except Exception as e:
        print(f"   ✗ API Error: {e}")
        tests_failed += 1
    
    print(f"\nAPI Tests: {tests_passed} passed, {tests_failed} failed\n")
    return tests_failed == 0

def test_critical_bugs():
    """Verify critical bugs are fixed."""
    print("Testing Critical Bug Fixes...\n")
    
    tests_passed = 0
    tests_failed = 0
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test self-reference bug
        test_file = Path(tmpdir) / "test.py"
        test_file.write_text("import reqtracker\nimport requests")
        
        print("1. Self-reference bug")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker analyze --output req.txt",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            content = (Path(tmpdir) / "req.txt").read_text()
            if "reqtracker" not in content:
                print("   ✓ FIXED - No self-reference")
                tests_passed += 1
            else:
                print("   ✗ NOT FIXED - Still includes reqtracker")
                tests_failed += 1
        
        # Test stdlib filtering
        test_file.write_text("import os\nimport json\nimport pyexpat")
        print("2. Stdlib filtering")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker analyze --output req2.txt",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            content = (Path(tmpdir) / "req2.txt").read_text()
            if "pyexpat" not in content and "os" not in content:
                print("   ✓ FIXED - Stdlib filtered")
                tests_passed += 1
            else:
                print("   ✗ NOT FIXED - Stdlib in output")
                tests_failed += 1
        
        # Test namespace packages
        test_file.write_text("import matplotlib.pyplot as plt\nfrom mpl_toolkits import mplot3d")
        print("3. Namespace packages")
        result = subprocess.run(
            f"cd {tmpdir} && reqtracker track test.py",
            shell=True, capture_output=True, text=True
        )
        if result.returncode == 0:
            if "mpl_toolkits" not in result.stdout:
                print("   ✓ FIXED - Namespace packages filtered")
                tests_passed += 1
            else:
                print("   ✗ NOT FIXED - mpl_toolkits in output")
                tests_failed += 1
    
    print(f"\nBug Fix Tests: {tests_passed} passed, {tests_failed} failed\n")
    return tests_failed == 0

def main():
    """Run all tests and report results."""
    print("=" * 60)
    print("reqtracker v1.0.7 Release Test Suite")
    print("=" * 60 + "\n")
    
    cli_ok = test_cli_commands()
    api_ok = test_python_api()
    bugs_ok = test_critical_bugs()
    
    print("=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if cli_ok and api_ok and bugs_ok:
        print("\n✅ ALL TESTS PASSED! Ready for v1.0.7 release!")
        print("\nNext steps:")
        print("1. Review changes: git diff")
        print("2. Commit: git add -A && git commit -m 'Release v1.0.7'")
        print("3. Tag: git tag v1.0.7")
        print("4. Push: git push && git push --tags")
        print("5. Release on PyPI: python -m build && twine upload dist/*")
        return 0
    else:
        print("\n❌ SOME TESTS FAILED. Fix issues before release.")
        if not cli_ok:
            print("  - CLI commands have issues")
        if not api_ok:
            print("  - Python API has issues")
        if not bugs_ok:
            print("  - Critical bugs not fully fixed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
