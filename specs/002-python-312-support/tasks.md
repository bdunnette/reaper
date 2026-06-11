# Tasks: Support Python 3.12 and Later

**Input**: Design documents from `/specs/002-python-312-support/`

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

- [X] T001 Verify requirements and target metadata format in pyproject.toml

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Check codebase files for any Python 3.14-only syntax using static analysis

**Checkpoint**: Foundation ready - user story implementation can now begin

## Phase 3: User Story 1 - Run Reaper in Python 3.12+ Environments (Priority: P1) 🎯 MVP

**Goal**: Run reaper and tests cleanly on Python 3.12 and 3.13.

**Independent Test**: Install and run pytest in Python 3.12 virtualenv.

### Implementation for User Story 1

- [X] T003 [US1] Run unit tests locally in Python 3.12 environment using specs/002-python-312-support/quickstart.md
- [X] T004 [US1] Run unit tests locally in Python 3.13 environment using specs/002-python-312-support/quickstart.md

**Checkpoint**: At this point, the library works perfectly on Python 3.12 and 3.13.

## Phase 4: User Story 2 - Build Package for Python 3.12+ (Priority: P2)

**Goal**: Update Python version constraint in metadata and verify package build.

**Independent Test**: Verify built wheel metadata Requires-Python field.

### Implementation for User Story 2

- [X] T005 [US2] Update requires-python constraint to >=3.12 in pyproject.toml
- [X] T006 [US2] Build wheel and sdist package using uv build on pyproject.toml
- [X] T007 [US2] Verify built metadata Requires-Python matches >=3.12 in specs/002-python-312-support/quickstart.md

**Checkpoint**: Package builds with correct Python 3.12 metadata compatibility.

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T008 Run ruff check to verify code styling conforms to standard formatting rules across reaper/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Logically depends on code compatibility (US1) succeeding first

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (validates the code is fully compatible before changing metadata)
4. **STOP and VALIDATE**: Confirm tests pass on Python 3.12/3.13.

### Incremental Delivery

1. Complete Setup + Foundational
2. Add User Story 1 → Verify runtime compatibility
3. Add User Story 2 → Update package specification metadata
4. Run polish phase checks
