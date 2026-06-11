# Research: Convenience DataFrame Search Function Implementation

## Decision

Implement `search_properties_dataframe` by wrapping `search_properties_paginated` on both clients and converting the aggregated results using `HomeSearchResult(results=list_of_properties).to_dataframe(backend=backend)`.

## Rationale

- **DRY (Don't Repeat Yourself)**: `HomeSearchResult.to_dataframe()` already contains the complete logic for converting a list of `Property` models to a Narwhals DataFrame. Instantiating a temporary `HomeSearchResult` model allows us to reuse this logic entirely.
- **Async Parity**: We can easily iterate over `AsyncGenerator[Property, None]` yielded by `AsyncRealtorClient.search_properties_paginated` to build the async equivalent.
- **Parameter Parity**: Reusing parameter signatures ensures the API remains simple and clean.

## Alternatives Considered

- **Custom conversion logic inside `reaper/client.py`**:
  - *Why rejected*: Duplicates the flat property dict creation code and Narwhals conversion logic already defined in `HomeSearchResult.to_dataframe()`.
