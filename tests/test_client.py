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

from factories import AutocompleteResultFactory, PropertyFactory, SearchResponseFactory

# Helper function to generate mock GraphQL payloads
def make_autocomplete_response(results=None):
    if results is None:
        results = [AutocompleteResultFactory()]
    return {"data": {"autocomplete": {"results": results}}}

def make_search_response(results=None, total=1):
    if results is None:
        results = [PropertyFactory()]
    return {
        "data": {
            "home_search": {
                "count": len(results),
                "total": total,
                "results": results
            }
        }
    }

def make_detail_response(property_id="12345"):
    prop = PropertyFactory(property_id=property_id)
    return {"data": {"property": prop}}



def test_sync_autocomplete(monkeypatch):
    """Test the synchronous autocomplete method."""
    client = RealtorClient()

    def mock_get(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return make_autocomplete_response(results=[AutocompleteResultFactory(city="Austin", state_code="TX")])
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
                return make_search_response(results=[PropertyFactory(property_id="12345", list_price=500000, description={"beds": 3, "baths": 2.5, "sqft": 2000, "year_built": 2015, "type": "single_family"})])
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
        variables = json_data.get("variables", {})
        query_vars = variables.get("query", {})
        query_prop_id = query_vars.get("property_id", "12345")

        class MockResponse:
            status_code = 200
            def json(self):
                if "home_search" in query_str:
                    return make_search_response(results=[PropertyFactory(property_id=query_prop_id)])
                else:
                    return make_detail_response(property_id=query_prop_id)
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
                return make_autocomplete_response(results=[AutocompleteResultFactory(city="Austin", state_code="TX")])
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
                return make_search_response()
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    res = client.search_properties(location="Austin, TX")

    # Mock import of polars and pandas to verify zero-dependency fallback behavior
    import builtins
    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name in ("polars", "pandas"):
            raise ImportError(f"Mocked missing {name}")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)

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
                return make_search_response(results=[PropertyFactory(property_id="12345")])
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
                return make_search_response(results=[PropertyFactory(property_id="12345")])
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


def test_sync_search_properties_dataframe(monkeypatch):
    """Test the synchronous search_properties_dataframe method."""
    client = RealtorClient()

    def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return make_search_response(results=[PropertyFactory(property_id="12345")])
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    df = client.search_properties_dataframe(location="Austin, TX", max_results=1)

    assert df is not None
    assert "property_id" in df.columns
    assert df.shape[0] == 1


@pytest.mark.asyncio
async def test_async_search_properties_dataframe(monkeypatch):
    """Test the asynchronous search_properties_dataframe method."""
    client = AsyncRealtorClient()

    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return make_search_response(results=[PropertyFactory(property_id="12345")])
            def raise_for_status(self):
                pass
        return MockResponse()

    monkeypatch.setattr(client.client, "post", mock_post)
    df = await client.search_properties_dataframe(location="Austin, TX", max_results=1)

    assert df is not None
    assert "property_id" in df.columns
    assert df.shape[0] == 1
    await client.close()
