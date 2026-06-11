# Implementation Plan: Support Python 3.12 and Later

**Branch**: `002-python-312-support` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/002-python-312-support/spec.md`

## Summary

The goal of this feature is to lower the minimum python version required by the package from Python 3.14 to Python 3.12. This will enable installation in environments like Google Colab and standard developer platforms running stable Python 3.12/3.13. We will modify `pyproject.toml` to declare the lower requirement, verify codebase compatibility with Python 3.12/3.13, and ensure tests execute successfully.

## Technical Context

**Language/Version**: Python >= 3.12 (previously >= 3.14)

**Primary Dependencies**:
- httpx>=0.28.1
- narwhals>=2.21.2
- pydantic>=2.13.4

**Storage**: None

**Testing**:
- pytest>=9.0.3
- pytest-asyncio>=1.4.0

**Target Platform**: OS-agnostic Python environment (Python >= 3.12)

**Project Type**: library

**Performance Goals**: N/A (compile and runtime compatibility)

**Constraints**: Codebase must remain compatible with Python 3.12 syntax and typing rules (e.g. PEP 695 generic syntax is supported in 3.12, but Python 3.13/3.14 features cannot leak into library code).

**Scale/Scope**: Build system and source compatibility configuration.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Browser Fingerprint Emulation & Proxy Integration**: Pass (No impact).
- **Principle II: Pydantic-Validated Models**: Pass (Pydantic v2 supports Python 3.12).
- **Principle III: Sync and Async API Parity**: Pass (No impact).
- **Principle IV: Zero-Dependency Dataframe Interoperability**: Pass (Narwhals supports Python 3.12).
- **Principle V: Clean Testing Discipline**: Pass (Test suite must run and pass under Python 3.12).
- **Technology Stack & Constraints (Python >= 3.14)**: *VIOLATION (JUSTIFIED)*. The constitution specifies `Reaper targets modern Python versions (>= 3.14)`. Lowering the requirement to `requires-python = ">=3.12"` is necessary to support standard hosted runtimes like Google Colab.

## Project Structure

### Documentation (this feature)

```text
specs/002-python-312-support/
├── plan.md              # This file
├── research.md          # Phase 0 output
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

We will modify packaging configurations:

```text
pyproject.toml           # Modify requires-python to ">=3.12"
```

**Structure Decision**: Single project layout. Editing metadata in `pyproject.toml` at the repository root.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Python >= 3.14 constraint | Support Python 3.12 for Google Colab/standard runtimes | Rejecting Python 3.12 would lock out the vast majority of notebook and corporate developers |
