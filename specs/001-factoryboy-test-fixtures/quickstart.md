# Quickstart Validation Guide: factory_boy Tests

Verify the migration of test fixtures to `factory_boy` by following these steps.

## Prerequisites

- Install `factory_boy` in the development environment:
  ```bash
  uv add --dev factory-boy
  ```

## Running Tests

To execute all unit and integration tests and confirm that the factories generate correct mock structures:

```bash
uv run pytest tests/test_client.py
```

## Verification

If successful, `pytest` will output passing results for all tests, showing that the dynamically generated mock data is correctly validated by the Reaper client models and assertions.
