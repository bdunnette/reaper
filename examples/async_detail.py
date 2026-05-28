# examples/async_detail.py

"""
Example showing how to asynchronously fetch detailed real estate information including schools, tax history, and transaction history.
"""

import asyncio
from reaper import AsyncRealtorClient, RealtorError

async def fetch_property_details(property_id: str):
    print(f"Initializing AsyncRealtorClient to fetch property: {property_id}...")

    async with AsyncRealtorClient() as client:
        try:
            prop = await client.get_property_detail(property_id=property_id)
            if not prop:
                print(f"Property with ID '{property_id}' was not found.")
                return

            # Address information
            addr = prop.location.address if prop.location else None
            print(f"\n--- PROPERTY DETAILS ({prop.property_id}) ---")
            if addr:
                print(f"Address: {addr.line}, {addr.city}, {addr.state_code} {addr.postal_code}")
                if addr.coordinate:
                    print(f"Coordinates: Lat {addr.coordinate.lat}, Lon {addr.coordinate.lon}")

            print(f"Status: {prop.status} | List Price: ${prop.list_price:,}")

            if prop.description:
                desc = prop.description
                print(f"Beds/Baths: {desc.beds} Beds, {desc.baths} Baths")
                print(f"Square Footage: {desc.sqft:,} SqFt")
                print(f"Lot Size: {desc.lot_sqft:,} SqFt" if desc.lot_sqft else "Lot Size: N/A")
                print(f"Year Built: {desc.year_built}")
                if desc.text:
                    print(f"Description: {desc.text[:200]}...")

            # School Information
            if prop.schools:
                print("\n--- NEARBY SCHOOLS ---")
                for school in prop.schools[:3]:
                    print(f" - [{school.rating}/10] {school.name} ({school.grades}) - {school.distance} miles away")

            # Tax History
            if prop.tax_history:
                print("\n--- TAX & ASSESSMENT HISTORY ---")
                for tax in prop.tax_history[:3]:
                    assess = tax.assessment.total if tax.assessment else "N/A"
                    print(f" - Year {tax.year}: Tax ${tax.tax:,} | Assessment Total: ${assess:,}")

            # Transaction History
            if prop.property_history:
                print("\n--- TRANSACTION HISTORY ---")
                for event in prop.property_history[:3]:
                    print(f" - {event.date}: {event.event_name} | Price: ${event.price:, if event.price else 'N/A'}")

        except RealtorError as e:
            print(f"An error occurred: {e}")

async def main():
    # To make the example interactive and functional out-of-the-box,
    # we first search for a live property in Austin, TX to get a valid ID.
    print("Searching for a live property ID in Austin, TX...")
    async with AsyncRealtorClient() as client:
        try:
            search_res = await client.search_properties(location="Austin, TX", limit=1)
            if search_res.results:
                target_id = search_res.results[0].property_id
                print(f"Found live property ID: {target_id}")
                await fetch_property_details(target_id)
            else:
                print("No live properties found, using fallback dummy ID.")
                await fetch_property_details("12345")
        except Exception as e:
            print(f"Search failed: {e}. Falling back to dummy ID.")
            await fetch_property_details("12345")

if __name__ == "__main__":
    asyncio.run(main())
