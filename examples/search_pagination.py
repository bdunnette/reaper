# examples/search_pagination.py

"""
Example showing how to stream search results with pagination from Realtor.com using reaper library.
"""

import asyncio
from reaper import RealtorClient, AsyncRealtorClient, RealtorError

def run_sync_pagination():
    print("\n--- Synchronous Search Pagination ---")
    with RealtorClient() as client:
        try:
            # Stream up to 5 properties in Austin, TX, fetching 2 per page
            generator = client.search_properties_paginated(
                location="Austin, TX",
                page_size=2,
                max_results=5,
                prop_type=["single_family"]
            )

            print("Streaming properties page-by-page synchronously:")
            for idx, prop in enumerate(generator, 1):
                addr = prop.location.address if prop.location else None
                print(f" {idx}. [{prop.status.upper()}] {addr.line if addr else 'Unknown Address'} - ${prop.list_price:,}")

        except RealtorError as e:
            print(f"Sync pagination failed: {e}")

async def run_async_pagination():
    print("\n--- Asynchronous Search Pagination ---")
    async with AsyncRealtorClient() as client:
        try:
            # Stream up to 5 properties in Austin, TX, fetching 2 per page
            async_generator = client.search_properties_paginated(
                location="Austin, TX",
                page_size=2,
                max_results=5,
                prop_type=["single_family"]
            )

            print("Streaming properties page-by-page asynchronously:")
            idx = 1
            async for prop in async_generator:
                addr = prop.location.address if prop.location else None
                print(f" {idx}. [{prop.status.upper()}] {addr.line if addr else 'Unknown Address'} - ${prop.list_price:,}")
                idx += 1

        except RealtorError as e:
            print(f"Async pagination failed: {e}")

if __name__ == "__main__":
    run_sync_pagination()
    asyncio.run(run_async_pagination())
