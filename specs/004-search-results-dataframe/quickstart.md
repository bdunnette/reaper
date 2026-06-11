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
