# Tasks: Resolve Pydantic Dependency Conflict

**Input**: Design documents from `/specs/003-pydantic-dependency-conflict/`

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

- [X] T001 Verify project dependency configuration in pyproject.toml

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Check Pydantic v2 core syntax compatibility in reaper/models.py

**Checkpoint**: Foundation ready - user story implementation can now begin

## Phase 3: User Story 1 - Install Reaper alongside Gradio in Hosted Notebooks (Priority: P1) 🎯 MVP

**Goal**: Support concurrent installation of Gradio and Reaper without dependency conflicts.

**Independent Test**: Install gradio and reaper together in clean environment.

### Implementation for User Story 1

- [X] T003 [US1] Update pydantic version constraint to >=2.0 in pyproject.toml
- [X] T004 [US1] Run package dependency resolution test using gradio alongside reaper in specs/003-pydantic-dependency-conflict/quickstart.md

**Checkpoint**: At this point, Reaper can be installed alongside Gradio with no conflict.

## Phase 4: User Story 2 - Maintain Reaper Functionality with Older Pydantic Versions (Priority: P2)

**Goal**: Ensure Reaper models are fully functional under Pydantic 2.12.3.

**Independent Test**: Run unit tests under Pydantic 2.12.3.

### Implementation for User Story 2

- [X] T005 [US2] Run pytest suite with pinned older pydantic version using specs/003-pydantic-dependency-conflict/quickstart.md

**Checkpoint**: Core features verified functional on Pydantic 2.12.3.

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T006 Run ruff check across source files in reaper/
- [X] T007 Run final package build using uv build on pyproject.toml

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Logically depends on US1 succeeding first
