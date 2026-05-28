# examples/polars_dataframe.py

"""
Example showing how to convert Realtor.com search results to a Polars DataFrame.
"""

from reaper import RealtorClient, RealtorError

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
            print("Converting search results to a Polars DataFrame...")

            # Convert directly to a Polars DataFrame
            df = search_res.to_polars()

            print("\n--- Polars DataFrame Summary ---")
            print(df)

            print("\n--- Filtering DataFrame (Properties with beds >= 4) ---")
            filtered_df = df.filter(df["beds"] >= 4)
            print(filtered_df.select(["property_id", "list_price", "beds", "sqft", "address_line"]))

            print("\n--- Average Price by Property Type ---")
            avg_price_df = df.group_by("property_type").agg(df["list_price"].mean().alias("avg_price"))
            print(avg_price_df)

        except RealtorError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
