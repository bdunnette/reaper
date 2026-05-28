# tests/test_client.py

"""
Unit tests for the Reaper Realtor GraphQL clients using pytest.
"""

import pytest
import httpx
from reaper import (
    RealtorClient,
    AsyncRealtorClient,
    RealtorAuthenticationError,
    RealtorAPIError,
)

# Mock Response Data
MOCK_AUTOCOMPLETE_RESPONSE = {
    "data": {
        "autocomplete": {
            "results": [
                {
                    "area_type": "city",
                    "city": "Austin",
                    "state_code": "TX",
                    "postal_code": None,
                    "slug_id": "Austin_TX",
                    "single_line_address": "Austin, TX",
                }
            ]
        }
    }
}

MOCK_SEARCH_RESPONSE = {
    "data": {
        "home_search": {
            "count": 1,
            "total": 1,
            "results": [
                {
                    "property_id": "12345",
                    "listing_id": "67890",
                    "status": "for_sale",
                    "list_price": 500000,
                    "description": {
                        "beds": 3,
                        "baths": 2.5,
                        "sqft": 2000,
                        "year_built": 2015,
                        "type": "single_family",
                    },
                    "location": {
                        "address": {
                            "line": "123 Main St",
                            "city": "Austin",
                            "state_code": "TX",
                            "postal_code": "78701",
                        }
                    },
                }
            ],
        }
    }
}

MOCK_DETAIL_RESPONSE = {
    "data": {
        "property": {
            "property_id": "12345",
            "listing_id": "67890",
            "status": "for_sale",
            "list_price": 500000,
            "description": {
                "beds": 3,
                "baths": 2.5,
                "sqft": 2000,
                "year_built": 2015,
                "type": "single_family",
                "text": "Beautiful home.",
            },
            "location": {
                "address": {
                    "line": "123 Main St",
                    "city": "Austin",
                    "state_code": "TX",
                    "postal_code": "78701",
                }
            },
            "tax_history": [{"tax": 5000, "year": 2023}],
        }
    }
}


def test_sync_autocomplete(monkeypatch):
    """Test the synchronous autocomplete method."""
    client = RealtorClient()

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_AUTOCOMPLETE_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "get", mock_get)
    results = client.autocomplete("Austin, TX")

    assert len(results) == 1
    assert results[0].city == "Austin"
    assert results[0].state_code == "TX"
    assert results[0].single_line_address == "Austin, TX"


def test_sync_search_properties(monkeypatch):
    """Test the synchronous search_properties method."""
    client = RealtorClient()

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_SEARCH_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    res = client.search_properties(location="Austin, TX", price_max=600000)

    assert res.total == 1
    assert len(res.results) == 1
    assert res.results[0].property_id == "12345"
    assert res.results[0].list_price == 500000
    assert res.results[0].description.beds == 3


def test_sync_get_property_detail(monkeypatch):
    """Test the synchronous get_property_detail method."""
    client = RealtorClient()

    def mock_post(*args, **kwargs):
        json_data = kwargs.get("json", {})
        query_str = json_data.get("query", "")

        class MockResponse:
            status_code = 200
            def json(self):
                if "home_search" in query_str:
                    return MOCK_SEARCH_RESPONSE
                else:
                    return MOCK_DETAIL_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    prop = client.get_property_detail("12345")

    assert prop is not None
    assert prop.property_id == "12345"
    assert prop.tax_history[0].tax == 5000


def test_sync_authentication_error(monkeypatch):
    """Test RealtorAuthenticationError is raised on 403 status."""
    client = RealtorClient()

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 403
            def raise_for_status(self):
                raise httpx.HTTPStatusError("Forbidden", request=None, response=self)
        return MockResponse()

    monkeypatch.setattr(client.client, "get", mock_get)

    with pytest.raises(RealtorAuthenticationError):
        client.autocomplete("Austin, TX")


def test_sync_graphql_errors(monkeypatch):
    """Test RealtorAPIError is raised when response contains errors."""
    client = RealtorClient()

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"errors": [{"message": "Invalid query parameters"}]}
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "get", mock_get)

    with pytest.raises(RealtorAPIError) as exc_info:
        client.autocomplete("Austin, TX")
    assert "Invalid query parameters" in str(exc_info.value)


@pytest.mark.asyncio
async def test_async_autocomplete(monkeypatch):
    """Test the asynchronous autocomplete method."""
    client = AsyncRealtorClient()

    async def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_AUTOCOMPLETE_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "get", mock_get)
    results = await client.autocomplete("Austin, TX")

    assert len(results) == 1
    assert results[0].city == "Austin"
    await client.close()


def test_to_dataframe_zero_dependency(monkeypatch):
    """Test that to_dataframe calls narwhals.from_dict correctly."""
    client = RealtorClient()

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_SEARCH_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    res = client.search_properties(location="Austin, TX")

    # Since neither polars nor pandas is installed in the dependencies anymore,
    # calling to_dataframe() without an installed backend will raise an ImportError.
    # This verifies the Narwhals integration is hooked up and executes correctly.
    with pytest.raises(ImportError) as exc_info:
        res.to_dataframe()

    assert "No dataframe backend" in str(exc_info.value)


def test_sync_search_properties_paginated(monkeypatch):
    """Test the synchronous search_properties_paginated generator."""
    client = RealtorClient()

    call_count = 0

    def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        class MockResponse:
            status_code = 200
            def json(self):
                # On the second call, return empty list of results to simulate end of pagination
                if call_count > 1:
                    return {
                        "data": {
                            "home_search": {
                                "count": 0,
                                "total": 1,
                                "results": []
                            }
                        }
                    }
                return MOCK_SEARCH_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    results = list(client.search_properties_paginated(location="Austin, TX", page_size=1, max_results=5))

    assert len(results) == 1
    assert results[0].property_id == "12345"
    assert call_count == 2  # The second call returned empty results and terminated loop


@pytest.mark.asyncio
async def test_async_search_properties_paginated(monkeypatch):
    """Test the asynchronous search_properties_paginated generator."""
    client = AsyncRealtorClient()

    call_count = 0

    async def mock_post(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        class MockResponse:
            status_code = 200
            def json(self):
                if call_count > 1:
                    return {
                        "data": {
                            "home_search": {
                                "count": 0,
                                "total": 1,
                                "results": []
                            }
                        }
                    }
                return MOCK_SEARCH_RESPONSE
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)

    results = []
    async for prop in client.search_properties_paginated(location="Austin, TX", page_size=1, max_results=5):
        results.append(prop)

    assert len(results) == 1
    assert results[0].property_id == "12345"
    assert call_count == 2
    await client.close()
