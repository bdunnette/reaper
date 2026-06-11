# Tasks: Replace Static Test Fixtures with factory_boy

**Input**: Design documents from `/specs/001-factoryboy-test-fixtures/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md

**Tests**: Unit tests are required to check both base factory features and that migrated tests pass.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- Single project structure: Files under root `tests/` directory.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize factory_boy by adding it to pyproject.toml development dependencies.
- [x] T002 Create factories definition file tests/factories.py with basic imports.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create base dict-based factory or structure in tests/factories.py that matches GraphQL response structures.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Dynamic Mock Data for Autocomplete Tests (Priority: P1) 🎯 MVP

**Goal**: Autocomplete tests in tests/test_client.py migrated to use factory_boy.

**Independent Test**: Run `pytest tests/test_client.py -k autocomplete` and see them pass.

### Implementation for User Story 1

- [x] T004 [P] [US1] Define AutocompleteResultFactory in tests/factories.py
- [x] T005 [US1] Modify test_sync_autocomplete and test_async_autocomplete in tests/test_client.py to use AutocompleteResultFactory instead of static dicts.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - Dynamic Mock Data for Property Search and Detail Tests (Priority: P2)

**Goal**: Property search and property details tests in tests/test_client.py migrated to use factory_boy, making address and description generation more dynamic.

**Independent Test**: Run `pytest tests/test_client.py` for search and detail test cases and see them pass.

### Implementation for User Story 2

- [x] T006 [P] [US2] Define AddressFactory with dynamic attributes (such as dynamic line addresses, state codes, and cities) in tests/factories.py
- [x] T007 [P] [US2] Define DescriptionFactory with dynamic ranges (such as dynamic beds, baths, sqft, and year_built ranges) in tests/factories.py
- [x] T008 [P] [US2] Define PropertyFactory in tests/factories.py using AddressFactory and DescriptionFactory as subfactories.
- [x] T009 [P] [US2] Define SearchResponseFactory in tests/factories.py using PropertyFactory.
- [x] T010 [US2] Modify test_sync_search_properties, test_sync_get_property_detail, test_to_dataframe_zero_dependency, test_sync_search_properties_paginated, and test_async_search_properties_paginated in tests/test_client.py to use PropertyFactory and SearchResponseFactory.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T011 Code cleanup: Remove unused static dictionaries MOCK_AUTOCOMPLETE_RESPONSE, MOCK_SEARCH_RESPONSE, and MOCK_DETAIL_RESPONSE from tests/test_client.py.
- [x] T012 Run all unit tests by executing uv run pytest tests/test_client.py to confirm all tests pass cleanly.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### Parallel Opportunities

- AutocompleteResultFactory (T004) and AddressFactory/DescriptionFactory (T006/T007) can be written in parallel.
- Once factories are written, refactoring tasks T005 and T010 can be executed in parallel since they target distinct parts of the tests.
