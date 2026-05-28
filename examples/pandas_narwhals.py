# examples/pandas_narwhals.py

"""
Example showing how to convert search results to Pandas and Narwhals DataFrames.
"""

from reaper import RealtorClient, RealtorError

def main():
    print("Initializing RealtorClient...")

    with RealtorClient() as client:
        try:
            print("\nSearching properties in Austin, TX...")
            search_res = client.search_properties(
                location="Austin, TX",
                price_max=900000,
                beds_min=3,
                limit=5
            )

            # 1. Convert to Pandas DataFrame
            print("\nConverting results to a Pandas DataFrame...")
            df_pandas = search_res.to_dataframe(library="pandas")
            print("Pandas DataFrame type:", type(df_pandas))
            print(df_pandas[["property_id", "list_price", "beds", "city"]])

            # 2. Convert to Narwhals DataFrame for library-agnostic computations
            print("\nConverting results to a Narwhals DataFrame...")
            df_nw = search_res.to_dataframe(library="narwhals")
            print("Narwhals DataFrame type:", type(df_nw))

            # Perform a library-agnostic operation using Narwhals
            # Filter the dataframe for beds >= 4 and select columns
            print("\nPerforming agnostic selection on Narwhals DataFrame:")
            selected_nw = df_nw.filter(df_nw["beds"] >= 3).select(["property_id", "list_price", "beds"])
            # Return native dataframe to inspect
            native_df = selected_nw.to_native()
            print("Agnostic selection result (native polars type):")
            print(native_df)

        except RealtorError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
