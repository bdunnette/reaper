# Tasks: Install Reaper from Git

**Input**: Design documents from `/specs/001-pip-install-git/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, quickstart.md

**Tests**: None explicitly requested. Verification is handled manually via the quickstart guide.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root (reaper maps to `reaper/` at root)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Verify project structure and python configuration in pyproject.toml

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Verify setuptools version compatibility in pyproject.toml

**Checkpoint**: Foundation ready - user story implementation can now begin

## Phase 3: User Story 1 - Install Reaper Library via pip from Git (Priority: P1) 🎯 MVP

**Goal**: Make the repository package installable directly via pip from Git.

**Independent Test**: Run pip install from local folder/git and import `reaper`.

### Implementation for User Story 1

- [X] T003 [US1] Add [build-system] table with setuptools.build_meta to pyproject.toml
- [X] T004 [US1] Run package build check using build tool on pyproject.toml
- [X] T005 [US1] Verify package installation in clean virtualenv using specs/001-pip-install-git/quickstart.md

**Checkpoint**: At this point, User Story 1 is fully functional and testable independently.

## Phase 4: User Story 2 - Readme Instructions for Installation (Priority: P2)

**Goal**: Add clear, working install instructions to README.md.

**Independent Test**: Inspect README.md for the installation section.

### Implementation for User Story 2

- [X] T006 [US2] Add Installation section with git installation commands and python version requirement to README.md

**Checkpoint**: README.md contains working, accurate installation instructions.

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T007 Run ruff/mypy checks across source files in reaper/
- [X] T008 Run final validation scenarios as documented in specs/001-pip-install-git/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable but logically secondary to US1

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently using the quickstart guide.

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 → Test independently (MVP)
3. Add User Story 2 → Test README updates
4. Run final verification across the project
