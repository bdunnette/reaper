# Implementation Plan: Convenience DataFrame Search Function

**Branch**: `004-search-results-dataframe` | **Date**: 2026-06-11 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/004-search-results-dataframe/spec.md`

## Summary

The goal of this feature is to add `search_properties_dataframe` convenience methods to both the synchronous `RealtorClient` and asynchronous `AsyncRealtorClient`. These methods will automatically perform paginated searches, accumulate all matching properties up to `max_results` (or all properties if `max_results` is not specified), and export the final dataset directly into a Narwhals DataFrame.

## Technical Context

**Language/Version**: Python >= 3.12

**Primary Dependencies**:
- httpx>=0.28.1
- narwhals>=2.21.2
- pydantic>=2.0

**Storage**: None

**Testing**:
- pytest>=9.0.3
- pytest-asyncio>=1.4.0

**Target Platform**: OS-agnostic Python environment (Python >= 3.12)

**Project Type**: library

**Performance Goals**: Efficient memory allocation during accumulation of properties.

**Constraints**: Parity must be maintained between sync and async client APIs. Narwhals abstraction must be used to preserve zero-dependency dataframe interoperability.

**Scale/Scope**: Adding 2 helper methods on clients and updating client interfaces.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Principle I: Browser Fingerprint Emulation & Proxy Integration**: Pass (Uses existing client's requests under the hood).
- **Principle II: Pydantic-Validated Models**: Pass (Reuses `HomeSearchResult` and `Property` models).
- **Principle III: Sync and Async API Parity**: Pass (Exposing matching methods on both `RealtorClient` and `AsyncRealtorClient`).
- **Principle IV: Zero-Dependency Dataframe Interoperability**: Pass (Uses Narwhals dataframe backend detection).
- **Principle V: Clean Testing Discipline**: Pass (Unit tests will verify result accumulation and conversion for both clients).

## Project Structure

### Documentation (this feature)

```text
specs/004-search-results-dataframe/
├── plan.md              # This file
├── research.md          # Phase 0 output
└── quickstart.md        # Phase 1 output
```

### Source Code (repository root)

We will modify client methods:

```text
reaper/client.py         # Add search_properties_dataframe to RealtorClient and AsyncRealtorClient
```

**Structure Decision**: Single project layout. Adding client features in `reaper/client.py`.

## Complexity Tracking

No violations of the Constitution.
