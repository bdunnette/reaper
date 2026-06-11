# Feature Specification: Install Reaper from Git

**Feature Branch**: `001-pip-install-git`

**Created**: 2026-06-11

**Status**: Draft

**Input**: User description: "make it possible to pip install reaper library from git; add instructions to readme"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Install Reaper Library via pip from Git (Priority: P1)

As a python developer, I want to be able to install the reaper package directly from the Git repository using pip so that I can easily integrate it into my own projects without downloading the source code manually.

**Why this priority**: Core value of the feature. Without direct git installation, the library is not easily distributable.

**Independent Test**: Run `pip install git+https://github.com/bdunnette/reaper.git` in a clean python virtual environment and verify that the package installs successfully with all production dependencies.

**Acceptance Scenarios**:

1. **Given** a clean virtual environment, **When** I run `pip install git+https://github.com/bdunnette/reaper.git`, **Then** the installation completes with exit code 0.
2. **Given** a successful installation, **When** I run `python -c "import reaper"`, **Then** the module imports without any errors.
3. **Given** a successful installation, **When** I run `pip show reaper`, **Then** the output shows the correct metadata including package name, version, and dependencies.

---

### User Story 2 - Readme Instructions for Installation (Priority: P2)

As a developer looking at the reaper repository, I want clear, concise instructions in the README.md file explaining how to install and use the library so that I can quickly start using it.

**Why this priority**: Documentation is critical for onboarding and usability.

**Independent Test**: Inspect the README.md to ensure there is a clear "Installation" section detailing both git installation and dependency requirements.

**Acceptance Scenarios**:

1. **Given** the README.md file, **When** I open it, **Then** I see a dedicated section for "Installation" containing the exact command `pip install git+https://github.com/bdunnette/reaper.git`.
2. **Given** the README.md file, **When** I read the installation section, **Then** it clearly lists any prerequisites (like Python version compatibility).

---

### Edge Cases

- **Missing Build Backend**: What happens when the python environment uses a tool that requires explicit build system declarations? The system must include a robust `build-system` declaration in `pyproject.toml` so installation doesn't fail under modern build tools.
- **Offline/No Git**: How does the system handle environments without `git` installed or without internet connection? Standard pip error messages will bubble up, but instructions should state that `git` is a prerequisite.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The project configuration MUST support building the package automatically using standard Python build backends (e.g., setuptools or hatchling).
- **FR-002**: Installing the library via pip MUST automatically retrieve and install all production dependencies (`httpx`, `narwhals`, and `pydantic`).
- **FR-003**: The installed package MUST expose the `reaper` package name to Python imports.
- **FR-004**: The project README.md MUST be updated to include an installation section with the exact pip git commands.
- **FR-005**: The package version in metadata MUST match the current project version (`0.1.0`).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of installation tests from clean virtual environments succeed in under 30 seconds (excluding download speed variations).
- **SC-002**: Package metadata is verified via `pip show reaper` and lists the correct package version and dependencies.
- **SC-003**: README.md contains accurate, working installation instructions.

## Assumptions

- The repository will remain publicly accessible or accessible to users attempting the installation.
- Python >= 3.14 is installed in the target environment as defined by the Reaper Constitution.
- No changes to the library's actual functionality (sync/async client logic) are required for package distribution.
