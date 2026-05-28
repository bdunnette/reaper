# Reaper 🏡

Reaper is a fully typed, high-performance, synchronous and asynchronous Python library designed to retrieve real estate information from Realtor.com's federated GraphQL API endpoint at `https://www.realtor.com/frontdoor/graphql`.

Built with modern Python (supporting Python >= 3.14), `httpx`, and `pydantic` (v2), Reaper supports clean data serialization, automatic browser header emulation, and custom exceptions.

---

## ✨ Features

- ⚡ **Sync & Async Support**: Exposes both `RealtorClient` and `AsyncRealtorClient`.
- 🛡️ **Sophisticated Header Emulation**: Automatic injection of browser-like fingerprints to reduce risk of bot protection blocks.
- ⚙️ **Proxy Integration**: Seamless routing of requests through standard and rotating HTTP/HTTPS proxies.
- 📐 **GraphQL Schemas**: Prebuilt schemas for Autocomplete, Property Search, and Property details.
- 🏷️ **Pydantic Validation**: Robust, type-safe validation of location addresses, coordinate models, descriptions, tax histories, school details, and property transaction histories.
- ❌ **Clean Exceptions**: Custom exception mapping including `RealtorAPIError` and `RealtorAuthenticationError`.

---

## 🚀 Installation

This project uses `uv` for lightning-fast package management:

```bash
uv add httpx pydantic
```

---

## 💻 Quickstart

### 1. Synchronous Search

```python
from reaper import RealtorClient

with RealtorClient() as client:
    # Search for active homes in Austin, TX with min 3 beds under $600,000
    res = client.search_properties(
        location="Austin, TX",
        price_max=600000,
        beds_min=3,
        prop_type=["single_family"]
    )

    print(f"Total matching listings: {res.total}")
    for prop in res.results:
        addr = prop.location.address if prop.location else None
        print(f"🏡 {addr.line}, {addr.city} | ${prop.list_price} (Beds: {prop.description.beds})")
```

### 2. Asynchronous Property Details

```python
import asyncio
from reaper import AsyncRealtorClient

async def get_details():
    async with AsyncRealtorClient() as client:
        prop = await client.get_property_detail(property_id="12345")
        if prop:
            print(f"Listing Address: {prop.location.address.line}")
            print(f"Property SqFt: {prop.description.sqft}")
            print(f"Year Built: {prop.description.year_built}")

asyncio.run(get_details())
```

### 3. Autocomplete Location Suggestions

```python
from reaper import RealtorClient

with RealtorClient() as client:
    results = client.autocomplete(query="Austin, TX")
    for item in results:
        print(f"Found: {item.single_line_address} (Slug: {item.slug_id})")
```

### 4. Dataframe Conversion (Zero-Dependency via Narwhals)

Convert your search results directly to a Narwhals DataFrame. Narwhals has zero mandatory dependencies on Polars or Pandas, but will automatically detect and wrap whichever backend is installed in your local environment.

```python
from reaper import RealtorClient

with RealtorClient() as client:
    res = client.search_properties(location="Austin, TX", price_max=700000)

    # Converts list of properties to a Narwhals DataFrame automatically
    df = res.to_dataframe()
    print("DataFrame shape:", df.shape)

    # Run generic library-agnostic filters
    filtered_df = df.filter(df["beds"] >= 4)
    print(filtered_df.select(["property_id", "list_price", "beds", "address_line"]))
```

---

## 🧬 Exception Hierarchy

All custom exceptions inherit from `RealtorError`:

```
RealtorError
├── RealtorRequestError (Connection or HTTP Status failures)
├── RealtorAuthenticationError (Access Denied / WAF blocks e.g. 403)
└── RealtorAPIError (Valid HTTP request but returns GraphQL schema errors)
```

---

## 🧪 Testing

To run the unit tests, use the following `uv` commands:

```bash
uv add --dev pytest pytest-asyncio
uv run pytest -o pythonpath=.
```
