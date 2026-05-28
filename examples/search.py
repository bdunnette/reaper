# examples/search.py

"""
Example showing how to search property listings on Realtor.com using the reaper library.
"""

from reaper import RealtorClient, RealtorError

def main():
    print("Initializing Realtor.com synchronous client...")

    # Using 'with' context manager automatically closes the HTTP client on exit
    with RealtorClient() as client:
        try:
            print("\nSearching listings in Austin, TX...")
            # Query for active single family homes with at least 3 beds, max price $600k
            search_res = client.search_properties(
                location="Austin, TX",
                price_max=600000,
                beds_min=3,
                prop_type=["single_family"],
                limit=5
            )

            print(f"\nFound {search_res.total} matching listings. Showing top {len(search_res.results)}:")
            for idx, prop in enumerate(search_res.results, 1):
                addr = prop.location.address if prop.location else None
                desc = prop.description

                print(f"\n{idx}. Status: [{prop.status.upper()}] | Price: ${prop.list_price:,}")
                if addr:
                    print(f"   Address: {addr.line}, {addr.city}, {addr.state_code} {addr.postal_code}")
                if desc:
                    print(f"   Details: {desc.beds} Beds | {desc.baths} Baths | {desc.sqft:,} SqFt | Built: {desc.year_built}")
                if prop.primary_photo:
                    print(f"   Photo: {prop.primary_photo.href}")

        except RealtorError as e:
            print(f"An error occurred while communicating with Realtor.com: {e}")

if __name__ == "__main__":
    main()
