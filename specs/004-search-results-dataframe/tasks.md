# Tasks: Convenience DataFrame Search Function

**Input**: Design documents from `/specs/004-search-results-dataframe/`

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

- [X] T001 Verify existing client structure in reaper/client.py

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T002 Check HomeSearchResult.to_dataframe execution in reaper/models.py

**Checkpoint**: Foundation ready - user story implementation can now begin

## Phase 3: User Story 1 - Retrieve Paginated Search Results directly as a DataFrame (Priority: P1) 🎯 MVP

**Goal**: Support direct extraction of synchronous paginated results into a Narwhals DataFrame.

**Independent Test**: Verify sync search_properties_dataframe returns valid Narwhals DataFrame.

### Implementation for User Story 1

- [X] T003 [US1] Implement search_properties_dataframe in RealtorClient in reaper/client.py
- [X] T004 [US1] Verify sync search_properties_dataframe returns valid Narwhals DataFrame in specs/004-search-results-dataframe/quickstart.md

**Checkpoint**: Synchronous DataFrame search functionality verified.

## Phase 4: User Story 2 - Asynchronous DataFrame Search (Priority: P2)

**Goal**: Support direct extraction of asynchronous paginated results into a Narwhals DataFrame.

**Independent Test**: Verify async search_properties_dataframe returns valid Narwhals DataFrame.

### Implementation for User Story 2

- [X] T005 [US2] Implement search_properties_dataframe in AsyncRealtorClient in reaper/client.py
- [X] T006 [US2] Verify async search_properties_dataframe returns valid Narwhals DataFrame in specs/004-search-results-dataframe/quickstart.md

**Checkpoint**: Asynchronous DataFrame search functionality verified.

## Phase 5: Documentation & Example Updates (Priority: P3)

**Goal**: Provide clear documentation and runnable examples for the newly added client dataframe search methods.

**Independent Test**: Run python example script and verify it prints the retrieved dataframe shape and content.

### Implementation for Phase 5

- [X] T009 [US3] Add search_properties_dataframe usage examples to README.md
- [X] T010 [US3] Update examples/narwhals_dataframe.py to include search_properties_dataframe example

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T007 Create new test cases for client DataFrame search methods in tests/test_client.py
- [X] T008 Run ruff check across codebase to verify styling conforms in reaper/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Documentation (Phase 5)**: Depends on Phase 3 and Phase 4 implementation completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Logically independent but can be implemented sequentially
- **User Story 3 (P3)**: Depends on US1 and US2 completion
