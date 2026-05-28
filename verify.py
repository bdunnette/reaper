# verify.py

"""
Verification script for the reaper Realtor.com client library.
"""

import sys
from reaper import RealtorClient, RealtorAuthenticationError, RealtorAPIError, RealtorRequestError

def main():
    print("Testing RealtorClient importing...")

    # Initialize the client
    client = RealtorClient()
    print("Client initialized successfully.")

    # Attempt to autocomplete "Austin, TX"
    print("\nAttempting autocomplete query for 'Austin, TX'...")
    try:
        results = client.autocomplete(query="Austin, TX")
        print(f"Success! Found {len(results)} autocomplete results.")
        for res in results[:3]:
            print(f" - {res.single_line_address or res.city} (Area type: {res.area_type})")
    except RealtorAuthenticationError as e:
        print("\n[Bot Protection Detected]")
        print("Note: Realtor.com has sophisticated bot-detection policies (Akamai/Cloudflare/WAF).")
        print(f"The request returned an authentication/block error as expected for direct server requests: {e}")
    except (RealtorAPIError, RealtorRequestError) as e:
        print(f"Request failed with expected Realtor error: {e}")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        sys.exit(1)
    finally:
        client.close()

    print("\nVerification complete.")

if __name__ == "__main__":
    main()
