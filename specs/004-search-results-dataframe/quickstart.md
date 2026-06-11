# Quickstart & Verification Guide: Convenience DataFrame Search Function

This guide details the validation steps to verify that `search_properties_dataframe` successfully retrieves search results as a Narwhals DataFrame.

## Prerequisites

- Python >= 3.12
- `uv` package manager

## Verification Scenarios

### Scenario 1: Synchronous DataFrame Search

Verify that the synchronous client can retrieve a DataFrame of properties.

1. **Verify via python code**:
   ```python
   from reaper import RealtorClient

   with RealtorClient() as client:
       df = client.search_properties_dataframe(location="Austin, TX", max_results=10)
       print("DataFrame Columns:", df.columns)
       print("DataFrame Shape:", df.shape)
   ```

### Scenario 2: Asynchronous DataFrame Search

Verify that the async client can retrieve a DataFrame of properties.

1. **Verify via async python code**:
   ```python
   import asyncio
   from reaper import AsyncRealtorClient

   async def run():
       async with AsyncRealtorClient() as client:
           df = await client.search_properties_dataframe(location="Austin, TX", max_results=5)
           print("Async DataFrame Columns:", df.columns)
           print("Async DataFrame Shape:", df.shape)

   asyncio.run(run())
   ```

### Scenario 3: README Documentation Verification

Verify that the README contains documentation and code examples for the newly added `search_properties_dataframe` methods on both clients.

1. **Verify README structure**: Ensure there is a section explaining how to query search results directly as a Narwhals DataFrame.
2. **Verify examples**: Ensure the code snippets in the README compile and match the method signatures.

### Scenario 4: Examples Directory Verification

Verify that `examples/narwhals_dataframe.py` includes a clean, executable demonstration of `search_properties_dataframe`.

1. **Run example**: Run the example script using `uv run python examples/narwhals_dataframe.py` (with `PYTHONPATH=.`) and verify it runs without error and outputs dataframe shape and content.
