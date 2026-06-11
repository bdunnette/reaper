# Phase 0 Research: replace static test fixtures with factory_boy

## Decision
Create Python test factories in `tests/factories.py` utilizing the `factory_boy` package to generate mock dicts mimicking the GraphQL response schema.

## Rationale
Using a dedicated `tests/factories.py` keeps test code separated from the mock data definitions, and using `factory.DictFactory` matches the raw JSON response payload expected by the GraphQL parsing logic in `RealtorClient`.

## Alternatives Considered
- Keeping static fixtures: Verbose and makes it hard to test custom edge cases (e.g. paginated counts, sparse descriptions).
- Custom python helpers: Harder to maintain than a industry standard library like `factory_boy`.
