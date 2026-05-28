# examples/location_suggestions.py

"""
Example showing how to fetch location suggestions or autocomplete search areas.
"""

from reaper import RealtorClient, RealtorError

def main():
    print("Initializing RealtorClient...")

    with RealtorClient() as client:
        try:
            # User partial entry
            search_query = "Austin"
            print(f"\nRequesting autocomplete suggestions for '{search_query}'...")

            results = client.autocomplete(query=search_query)

            print(f"\nFound {len(results)} autocomplete suggestions:")
            for idx, item in enumerate(results, 1):
                area = item.area_type.upper() if item.area_type else "UNKNOWN"
                print(f" {idx}. [{area}] {item.single_line_address or item.city} (Slug: {item.slug_id})")

        except RealtorError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
