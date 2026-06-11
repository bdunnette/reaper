# Implementation Plan: Install Reaper from Git

**Branch**: `001-pip-install-git` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-pip-install-git/spec.md`

## Summary

The goal of this feature is to make the `reaper` library installable directly from its Git repository using pip. This requires adding a valid `[build-system]` table to `pyproject.toml` so standard build frontends (like pip) can build the wheel/sdist and install the package. We will also update the root README.md with clear installation and quickstart instructions.

## Technical Context

**Language/Version**: Python >= 3.14

**Primary Dependencies**:
- httpx>=0.28.1
- narwhals>=2.21.2
- pydantic>=2.13.4

**Storage**: None

**Testing**:
- pytest>=9.0.3
- pytest-asyncio>=1.4.0

**Target Platform**: OS-agnostic Python environment (pip-compatible)

**Project Type**: library

**Performance Goals**: Minimal installation overhead (<30 seconds)

**Constraints**: Pure Python packaging. No production dependency creep. Must run cleanly on Python >= 3.14.

**Scale/Scope**: Developer installation via Git.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Browser Fingerprint Emulation & Proxy Integration**: Pass (N/A for packaging).
- **Principle II: Pydantic-Validated Models**: Pass (N/A for packaging).
- **Principle III: Sync and Async API Parity**: Pass (N/A for packaging).
- **Principle IV: Zero-Dependency Dataframe Interoperability**: Pass (N/A for packaging).
- **Principle V: Clean Testing Discipline**: Pass (Tested package build/install locally via pytest or python scripts in clean virtualenvs).

## Project Structure

### Documentation (this feature)

```text
specs/001-pip-install-git/
├── plan.md              # This file
├── research.md          # Phase 0 output
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

We will modify existing packaging and documentation files at the root level:

```text
pyproject.toml           # Modify to add [build-system]
README.md                # Modify to add Installation instructions
```

**Structure Decision**: Single project layout. We are only editing the build system configuration and documentation at the repository root.

## Complexity Tracking

No violations of the Constitution.
