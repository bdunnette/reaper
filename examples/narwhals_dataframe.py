# examples/narwhals_dataframe.py

"""
Example showing how to convert search results to a Narwhals-wrapped DataFrame,
including directly retrieving search results as a combined DataFrame sync & async.
"""

import asyncio
from reaper import RealtorClient, AsyncRealtorClient, RealtorError

async def run_async_example():
    print("\n--- Running Asynchronous DataFrame Search Example ---")
    async with AsyncRealtorClient() as client:
        try:
            print("Searching properties in Austin, TX directly as a DataFrame (async)...")
            df = await client.search_properties_dataframe(
                location="Austin, TX",
                price_max=800000,
                max_results=5
            )
            print("Async DataFrame shape:", df.shape)
            print(df.select(["property_id", "list_price", "beds", "address_line"]))
        except ImportError as e:
            print(f"[Async Environment Info]: {e}")
        except RealtorError as e:
            print(f"An async error occurred: {e}")

def main():
    print("Initializing RealtorClient...")

    with RealtorClient() as client:
        try:
            print("\nSearching properties in Austin, TX...")
            search_res = client.search_properties(
                location="Austin, TX",
                price_max=800000,
                beds_min=3,
                limit=10
            )

            print(f"Retrieved {len(search_res.results)} properties.")
            print("\nConverting search results to a Narwhals DataFrame...")
            print("Note: Narwhals is zero-dependency and will automatically adapt to")
            print("whichever DataFrame backend is available (e.g. Polars or Pandas).")

            try:
                # 1. Convert to a Narwhals-wrapped DataFrame
                df = search_res.to_dataframe()

                print("\n--- Narwhals DataFrame Summary ---")
                print("DataFrame type:", type(df))
                print("Shape:", df.shape)

                # 2. Perform library-agnostic computations using the Narwhals API
                print("\n--- Filtering DataFrame (Properties with beds >= 4) ---")
                filtered_df = df.filter(df["beds"] >= 4)
                print(filtered_df.select(["property_id", "list_price", "beds", "sqft", "address_line"]))

                # 3. Aggregations (Average listing price)
                print("\n--- Summary Price Stats ---")
                avg_price = df["list_price"].mean()
                print(f"Average listing price: ${avg_price:,.2f}")

                # 4. Extracting the native dataframe (either polars.DataFrame or pandas.DataFrame)
                native_df = df.to_native()
                print("\nNative DataFrame object:", type(native_df))

                # 5. Direct search as DataFrame convenience method demo
                print("\n--- Direct Search as DataFrame ---")
                direct_df = client.search_properties_dataframe(
                    location="Austin, TX",
                    price_max=800000,
                    max_results=5
                )
                print("Direct DataFrame shape:", direct_df.shape)
                print(direct_df.select(["property_id", "list_price", "beds", "address_line"]))

            except ImportError as e:
                print(f"\n[Environment Info]: {e}")
                print("Tip: Run `pip install polars` or `pip install pandas` to test the dataframe conversion.")

        except RealtorError as e:
            print(f"An error occurred: {e}")

    # Run the async example
    try:
        asyncio.run(run_async_example())
    except Exception as e:
        print(f"Could not run async example: {e}")

if __name__ == "__main__":
    main()
