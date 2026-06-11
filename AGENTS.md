# Agentic Integration Guide (`AGENTS.md`)

This guide outlines how AI Agents, LLM-based tools, or MCP (Model Context Protocol) services can consume the `reaper` library to retrieve real estate data from Realtor.com's frontdoor GraphQL API.

---

## 🤖 AI Agent Tool Definitions

If you are equipping an AI Agent with tools to search, analyze, or recommend real estate listings, you can wrap `reaper` methods in semantic declarations.

### 1. Autocomplete/Location Suggestion Tool

- **Description**: Autocompletes user-provided search text into a standardized location query acceptable by Realtor.com. Use this before running search queries.
- **Parameters**:
  - `query` (string, required): Partial location search string (e.g. `"Austin"`, `"78701"`).

```python
def suggest_locations(query: str) -> list[dict]:
    with RealtorClient() as client:
        items = client.autocomplete(query)
        return [item.model_dump() for item in items]
```

### 2. Property Search Tool

- **Description**: Search for property listings matching specifications including location, price range, beds, and property types.
- **Parameters**:
  - `location` (string, required): Standardized location string (e.g. `"Austin, TX"`).
  - `price_max` (integer, optional): Maximum listing price.
  - `beds_min` (integer, optional): Minimum bedrooms count.
  - `prop_type` (array of strings, optional): e.g. `["single_family", "condo"]`.

```python
def search_listings(location: str, price_max: int = None, beds_min: int = None, prop_type: list[str] = None) -> dict:
    with RealtorClient() as client:
        res = client.search_properties(
            location=location,
            price_max=price_max,
            beds_min=beds_min,
            prop_type=prop_type
        )
        return res.model_dump()
```

### 3. Property Detail Tool

- **Description**: Retrieves granular information for a specific property (including address details, square footage, year built, schools, tax history, and transactions).
- **Parameters**:
  - `property_id` (string, required): The unique Realtor.com property identifier.

```python
def get_property_details(property_id: str) -> dict:
    with RealtorClient() as client:
        prop = client.get_property_detail(property_id)
        return prop.model_dump() if prop else {}
```

---

## ⚙️ Handling Bot Blocks inside Agents

When running agent loops, Realtor.com's bot-detection policies may block requests (HTTP 403). The agent must gracefully handle `RealtorAuthenticationError`:

1. **Catch Authentication Errors**: Intercept `RealtorAuthenticationError`.
2. **Apply Proxy**: Instruct the agent to switch/rotate proxies.
3. **Notify User**: If no proxy is available, output a human-friendly warning.

```python
from reaper import RealtorClient, RealtorAuthenticationError

try:
    with RealtorClient() as client:
        results = client.autocomplete("Miami, FL")
except RealtorAuthenticationError:
    # Switch to proxy if available
    with RealtorClient(proxy="http://rotating-proxy.net:8000") as client:
        results = client.autocomplete("Miami, FL")
```

<!-- SPECKIT START -->
For additional context about technologies to be used, project structure,
shell commands, and other important information, read the current plan:
[plan.md](file:///C:/Users/dunn0172/Documents/GitHub/reaper/specs/001-factoryboy-test-fixtures/plan.md)
<!-- SPECKIT END -->
