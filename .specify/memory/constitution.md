<!--
SYNC IMPACT REPORT
- Version change: Initial -> 1.0.0
- List of modified principles:
  - PRINCIPLE_1: Browser Fingerprint Emulation & Proxy Integration
  - PRINCIPLE_2: Pydantic-Validated Models
  - PRINCIPLE_3: Sync and Async API Parity
  - PRINCIPLE_4: Zero-Dependency Dataframe Interoperability
  - PRINCIPLE_5: Clean Testing Discipline
- Added sections: Technology Stack & Constraints, Development Workflow & Code Quality
- Removed sections: None
- Templates requiring updates (✅ updated / ⚠ pending):
  - .specify/templates/plan-template.md (✅ updated)
  - .specify/templates/spec-template.md (✅ updated)
  - .specify/templates/tasks-template.md (✅ updated)
  - .specify/templates/checklist-template.md (✅ updated)
- Follow-up TODOs: None
-->

# Reaper Constitution

## Core Principles

### I. Browser Fingerprint Emulation & Proxy Integration
To prevent API blocking (HTTP 403), both Sync and Async clients MUST implement browser-like header emulation. All requests MUST support standard and rotating proxy integration. Clients must raise and handle RealtorAuthenticationError appropriately.

### II. Pydantic-Validated Models
All API responses MUST be mapped and validated using Pydantic (v2) models (e.g., Address, Coordinate, PropertyDescription, TaxHistory). No raw dictionaries should be returned directly to users.

### III. Sync and Async API Parity
Every frontdoor GraphQL endpoint interaction MUST be supported by both RealtorClient (sync) and AsyncRealtorClient (async), ensuring complete functional parity and signature alignment.

### IV. Zero-Dependency Dataframe Interoperability
Methods like search_properties result sets MUST support export to pandas/polars DataFrames using Narwhals for zero-dependency backend detection. No hard dependencies on pandas or polars are allowed in production.

### V. Clean Testing Discipline
TDD is highly recommended. All API integrations and client behaviors MUST be thoroughly tested using pytest and pytest-asyncio with robust API mocking to prevent rate-limiting and flaky test runs.

## Technology Stack & Constraints
Reaper targets modern Python versions (>= 3.14). Primary libraries are httpx for HTTP routing, pydantic for validation, and narwhals for dataframes. No heavyweight frameworks or unnecessary dependencies are permitted. Performance targets must handle lazy streaming pagination efficiently.

## Development Workflow & Code Quality
All changes must be fully typed and pass mypy/ruff checks. Code style follows strict formatting rules. Unused imports, unused variables, and draft placeholders must be removed before commit. The AGENTS.md document must remain in sync with any public tool definitions.

## Governance
The Reaper Constitution governs all design and development decisions. Any modification to this constitution requires a version bump: MAJOR for backward-incompatible removals, MINOR for new principles/sections, and PATCH for non-semantic updates/clarifications. All changes must be verified against current templates and documentation.

**Version**: 1.0.0 | **Ratified**: 2026-06-09 | **Last Amended**: 2026-06-09
