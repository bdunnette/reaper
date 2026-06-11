# Feature Specification: Support Python 3.12 and Later

**Feature Branch**: `002-python-312-support`

**Created**: 2026-06-11

**Status**: Draft

**Input**: User description: "update python requirement to allow building on python 3.12 and later (for e.g. google colab)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Run Reaper in Python 3.12+ Environments (Priority: P1)

As a python developer using older runtime environments like Google Colab (which runs Python 3.12 or 3.13), I want to be able to install and import the reaper library so that I can use its Realtor.com integration without upgrading my runtime environment to Python 3.14.

**Why this priority**: Crucial for developers using hosted notebooks or standard enterprise Python runtimes (e.g. Colab).

**Independent Test**: Install `reaper` in a Python 3.12 or 3.13 environment and verify that it installs, imports, and executes core queries successfully.

**Acceptance Scenarios**:

1. **Given** a Python 3.12 or 3.13 environment, **When** I run `pip install .`, **Then** the installation completes successfully.
2. **Given** a successful installation in Python 3.12+, **When** I run a script importing and running `RealtorClient`, **Then** it completes without any syntax errors or runtime incompatibility issues.

---

### User Story 2 - Build Package for Python 3.12+ (Priority: P2)

As a maintainer of the reaper library, I want our package builds to indicate compatibility with Python 3.12 and later so that package managers (like pip, poetry, or uv) allow installation on these environments.

**Why this priority**: Necessary to declare official support in package metadata.

**Independent Test**: Build the package using `uv build` and check the metadata configuration for the python version requirement.

**Acceptance Scenarios**:

1. **Given** the built package metadata, **When** I inspect `Requires-Python`, **Then** it specifies `>=3.12`.

---

### Edge Cases

- **Python 3.14 Specific Syntax**: If the source code uses syntax introduced only in Python 3.14 (e.g., specific typing features, standard library upgrades, or syntax changes), it will fail under Python 3.12. The build check must catch syntax incompatibilities during testing on Python 3.12.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The package configuration MUST specify `requires-python = ">=3.12"` in the project metadata.
- **FR-002**: The codebase MUST not use any Python features, syntax, or standard library APIs that are exclusive to Python 3.13 or 3.14 unless backward-compatible fallbacks are provided.
- **FR-003**: The test suite MUST run and pass successfully on Python 3.12, 3.13, and 3.14.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Package metadata lists `requires-python = ">=3.12"`.
- **SC-002**: 100% of unit tests pass on Python 3.12 and 3.13.
- **SC-003**: No syntax errors or import errors are raised when running on Python 3.12 or 3.13.

## Assumptions

- No core library functionality requires features unique to Python >= 3.14.
- Standard libraries (like `httpx`, `narwhals`, and `pydantic`) support Python 3.12.
