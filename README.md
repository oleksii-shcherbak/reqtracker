# reqtracker

`reqtracker` is a Python library designed to automatically detect and manage Python dependencies in a clean, intelligent, and customizable way. Unlike traditional tools like `pip freeze`, which simply dump all installed packages, `reqtracker` focuses on generating accurate `requirements.txt` files based on actual project usage—scanning either source code or runtime behavior.

## Goals

* **Automated and Smart Dependency Tracking:** Track all third-party packages imported in a project and write them to `requirements.txt` automatically.
* **Multiple Tracking Modes:** Supports Static (AST analysis), Dynamic (import system hooks), and Hybrid (default) modes.
* **User-Centric Simplicity:** Minimal API (`reqtracker.track()`) with no configuration required out of the box, but highly customizable.
* **Safe and Clean Output:** Skips standard library and builtin modules, deduplicates results, and allows filtering.
* **Developer Workflow Integration:** Updates dependencies seamlessly during development.
* **Ready for Packaging and Open Source Use:** PyPI-compatible, lightweight, fast, and extensible.
