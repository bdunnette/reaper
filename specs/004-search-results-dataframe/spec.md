# Feature Specification: Convenience DataFrame Search Function

**Feature Branch**: `004-search-results-dataframe`

**Created**: 2026-06-11

**Status**: Draft

**Input**: User description: "create convenience function for returning all/paginated search results as dataframe"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve Paginated Search Results directly as a DataFrame (Priority: P1)

As a data scientist or developer using Reaper, I want to fetch search results directly as a Narwhals DataFrame (supporting pandas or polars) without having to manually iterate over a paginated generator or build custom conversion wrappers.

**Why this priority**: Directly targets usability and simplifies data analysis workflows.

**Independent Test**: Call the convenience search DataFrame method on the sync client and ensure it returns a valid DataFrame containing all matched properties.

**Acceptance Scenarios**:

1. **Given** a query for properties in a location, **When** I call `client.search_properties_dataframe(location="Austin, TX", max_results=10)`, **Then** it returns a Narwhals DataFrame with 10 rows representing those properties.
2. **Given** a query that spans multiple pages of results, **When** I call `client.search_properties_dataframe(location="Austin, TX", page_size=5, max_results=10)`, **Then** it automatically handles pagination and returns a single combined DataFrame with 10 rows.

---

### User Story 2 - Asynchronous DataFrame Search (Priority: P2)

As an async python developer, I want to fetch paginated search results directly as a Narwhals DataFrame asynchronously so that I don't block the event loop while fetching large result sets.

**Why this priority**: Essential for keeping async application performance and parity with the sync client (as mandated by the Reaper Constitution).

**Independent Test**: Call the convenience search DataFrame method on the async client and ensure it returns a valid DataFrame containing the requested properties.

**Acceptance Scenarios**:

1. **Given** an async context, **When** I run `await async_client.search_properties_dataframe(location="Austin, TX", max_results=5)`, **Then** it returns a Narwhals DataFrame.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Both `RealtorClient` and `AsyncRealtorClient` MUST expose a `search_properties_dataframe()` method.
- **FR-002**: The `search_properties_dataframe()` method MUST accept the same search parameters as `search_properties_paginated()` (location, price ranges, status, beds/baths, prop_type, etc.) along with `backend` (e.g. "polars", "pandas", or `None`).
- **FR-003**: Under the hood, `search_properties_dataframe()` MUST use pagination to gather all properties matching the criteria up to the specified `max_results`.
- **FR-004**: The returned object MUST be a `narwhals.DataFrame` representing the aggregated properties, using the existing columns and conversion logic defined in `HomeSearchResult.to_dataframe()`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of dataframes returned contain all columns defined by `HomeSearchResult.to_dataframe()`.
- **SC-002**: Results spanning multiple pages are successfully aggregated into a single DataFrame.
- **SC-003**: The method runs successfully on Python 3.12+ (conforming to the updated requirements).

## Assumptions

- Narwhals remains the zero-dependency backend abstraction layer.
- `HomeSearchResult.to_dataframe` will be reused or extracted to prevent code duplication.
