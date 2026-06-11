# Data Model Design: factory_boy Mock Schema

## Mocks & Dict Structures

Since `RealtorClient` handles raw JSON dictionaries returned by the GraphQL APIs, our factories should subclass `factory.DictFactory` (or `factory.Factory` with a custom strategy to output dicts) to mimic the exact response schemas.

### 1. Autocomplete Result Schema
- `area_type`: string (default "city")
- `city`: string (default "Austin")
- `state_code`: string (default "TX")
- `postal_code`: string (default None)
- `slug_id`: string (default "Austin_TX")
- `single_line_address`: string (default "Austin, TX")

### 2. Description Schema
- `beds`: integer (default 3)
- `baths`: float (default 2.5)
- `sqft`: integer (default 2000)
- `year_built`: integer (default 2015)
- `type`: string (default "single_family")
- `text`: string (default "Beautiful home.")

### 3. Address Schema
- `line`: string (default "123 Main St")
- `city`: string (default "Austin")
- `state_code`: string (default "TX")
- `postal_code`: string (default "78701")

### 4. Property Result Schema
- `property_id`: string (default sequential sequence)
- `listing_id`: string (default sequential sequence)
- `status`: string (default "for_sale")
- `list_price`: integer (default 500000)
- `description`: dict (via Description Schema)
- `location`: dict containing `address` (via Address Schema)
- `tax_history`: list of tax objects `[{"tax": 5000, "year": 2023}]`
