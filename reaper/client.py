# reaper/client.py

"""
Synchronous and Asynchronous GraphQL clients to retrieve real estate data from Realtor.com.
"""

from typing import Any
import httpx
from .queries import PROPERTY_SEARCH_QUERY, PROPERTY_DETAIL_QUERY, AUTOCOMPLETE_QUERY
from .models import Property, HomeSearchResult, AutocompleteItem
from .exceptions import RealtorError, RealtorAPIError, RealtorRequestError, RealtorAuthenticationError

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.realtor.com/",
    "Origin": "https://www.realtor.com",
    "Content-Type": "application/json",
}

DEFAULT_ENDPOINT = "https://www.realtor.com/frontdoor/graphql"

class RealtorClient:
    """Synchronous Realtor.com GraphQL API Client."""

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        headers: dict[str, str] | None = None,
        proxy: Any = None,
        timeout: float = 15.0,
    ):
        self.endpoint = endpoint
        self.headers = DEFAULT_HEADERS.copy()
        if headers:
            self.headers.update(headers)

        self.client = httpx.Client(
            headers=self.headers,
            proxy=proxy,
            timeout=timeout,
            follow_redirects=True,
        )

    def _execute_query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "query": query,
            "variables": variables,
        }
        try:
            response = self.client.post(self.endpoint, json=payload)
            if response.status_code in (401, 403):
                raise RealtorAuthenticationError(
                    f"Access denied (HTTP {response.status_code}). Realtor.com bot-detection might have blocked this request."
                )
            response.raise_for_status()

            data = response.json()
            if "errors" in data:
                raise RealtorAPIError(
                    f"GraphQL query returned errors: {data['errors'][0].get('message')}",
                    errors=data["errors"],
                )
            return data.get("data", {})
        except httpx.HTTPStatusError as e:
            raise RealtorRequestError(f"HTTP error occurred: {e}") from e
        except httpx.RequestError as e:
            raise RealtorRequestError(f"Network error occurred: {e}") from e
        except ValueError as e:
            raise RealtorError(f"Failed to parse JSON response: {e}") from e

    def search_properties(
        self,
        location: str,
        limit: int = 20,
        offset: int = 0,
        status: list[str] | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        beds_min: int | None = None,
        beds_max: int | None = None,
        baths_min: float | None = None,
        baths_max: float | None = None,
        prop_type: list[str] | None = None,
    ) -> HomeSearchResult:
        """
        Search for properties matching specified criteria.

        Args:
            location: City/state (e.g. "Austin, TX"), postal code, or location query.
            limit: Number of results to return (default: 20).
            offset: Result offset for pagination (default: 0).
            status: Listing status, e.g. ["for_sale", "for_rent", "sold"].
            price_min: Minimum listing price.
            price_max: Maximum listing price.
            beds_min: Minimum number of bedrooms.
            beds_max: Maximum number of bedrooms.
            baths_min: Minimum number of bathrooms.
            baths_max: Maximum number of bathrooms.
            prop_type: List of property types, e.g. ["single_family", "condo"].

        Returns:
            A HomeSearchResult model.
        """
        variables = {
            "location": location,
            "limit": limit,
            "offset": offset,
            "status": status,
            "priceMin": price_min,
            "priceMax": price_max,
            "bedsMin": beds_min,
            "bedsMax": beds_max,
            "bathsMin": baths_min,
            "bathsMax": baths_max,
            "propType": prop_type,
        }

        # Remove None values so they don't break the query or use defaults
        variables = {k: v for k, v in variables.items() if v is not None}

        res = self._execute_query(PROPERTY_SEARCH_QUERY, variables)
        search_data = res.get("home_search") or {"count": 0, "total": 0, "results": []}
        return HomeSearchResult.model_validate(search_data)

    def get_property_detail(self, property_id: str) -> Property | None:
        """
        Retrieve complete details for a single property by its ID.

        Args:
            property_id: The unique Realtor.com property identifier.

        Returns:
            A Property model or None if not found.
        """
        variables = {"property_id": property_id}
        res = self._execute_query(PROPERTY_DETAIL_QUERY, variables)
        prop_data = res.get("property")
        if not prop_data:
            return None
        return Property.model_validate(prop_data)

    def autocomplete(self, query: str) -> list[AutocompleteItem]:
        """
        Autocomplete / suggest location areas or addresses based on a search term.

        Args:
            query: Partially typed address, city, state, or zipcode.

        Returns:
            A list of AutocompleteItem models.
        """
        variables = {"query": query}
        res = self._execute_query(AUTOCOMPLETE_QUERY, variables)
        autocomplete_data = res.get("autocomplete") or {}
        results = autocomplete_data.get("results") or []
        return [AutocompleteItem.model_validate(item) for item in results]

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


class AsyncRealtorClient:
    """Asynchronous Realtor.com GraphQL API Client."""

    def __init__(
        self,
        endpoint: str = DEFAULT_ENDPOINT,
        headers: dict[str, str] | None = None,
        proxy: Any = None,
        timeout: float = 15.0,
    ):
        self.endpoint = endpoint
        self.headers = DEFAULT_HEADERS.copy()
        if headers:
            self.headers.update(headers)

        self.client = httpx.AsyncClient(
            headers=self.headers,
            proxy=proxy,
            timeout=timeout,
            follow_redirects=True,
        )

    async def _execute_query(self, query: str, variables: dict[str, Any]) -> dict[str, Any]:
        payload = {
            "query": query,
            "variables": variables,
        }
        try:
            response = await self.client.post(self.endpoint, json=payload)
            if response.status_code in (401, 403):
                raise RealtorAuthenticationError(
                    f"Access denied (HTTP {response.status_code}). Realtor.com bot-detection might have blocked this request."
                )
            response.raise_for_status()

            data = response.json()
            if "errors" in data:
                raise RealtorAPIError(
                    f"GraphQL query returned errors: {data['errors'][0].get('message')}",
                    errors=data["errors"],
                )
            return data.get("data", {})
        except httpx.HTTPStatusError as e:
            raise RealtorRequestError(f"HTTP error occurred: {e}") from e
        except httpx.RequestError as e:
            raise RealtorRequestError(f"Network error occurred: {e}") from e
        except ValueError as e:
            raise RealtorError(f"Failed to parse JSON response: {e}") from e

    async def search_properties(
        self,
        location: str,
        limit: int = 20,
        offset: int = 0,
        status: list[str] | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        beds_min: int | None = None,
        beds_max: int | None = None,
        baths_min: float | None = None,
        baths_max: float | None = None,
        prop_type: list[str] | None = None,
    ) -> HomeSearchResult:
        """
        Search for properties matching specified criteria asynchronously.

        Args:
            location: City/state (e.g. "Austin, TX"), postal code, or location query.
            limit: Number of results to return (default: 20).
            offset: Result offset for pagination (default: 0).
            status: Listing status, e.g. ["for_sale", "for_rent", "sold"].
            price_min: Minimum listing price.
            price_max: Maximum listing price.
            beds_min: Minimum number of bedrooms.
            beds_max: Maximum number of bedrooms.
            baths_min: Minimum number of bathrooms.
            baths_max: Maximum number of bathrooms.
            prop_type: List of property types, e.g. ["single_family", "condo"].

        Returns:
            A HomeSearchResult model.
        """
        variables = {
            "location": location,
            "limit": limit,
            "offset": offset,
            "status": status,
            "priceMin": price_min,
            "priceMax": price_max,
            "bedsMin": beds_min,
            "bedsMax": beds_max,
            "bathsMin": baths_min,
            "bathsMax": baths_max,
            "propType": prop_type,
        }

        variables = {k: v for k, v in variables.items() if v is not None}

        res = await self._execute_query(PROPERTY_SEARCH_QUERY, variables)
        search_data = res.get("home_search") or {"count": 0, "total": 0, "results": []}
        return HomeSearchResult.model_validate(search_data)

    async def get_property_detail(self, property_id: str) -> Property | None:
        """
        Retrieve complete details for a single property by its ID asynchronously.

        Args:
            property_id: The unique Realtor.com property identifier.

        Returns:
            A Property model or None if not found.
        """
        variables = {"property_id": property_id}
        res = await self._execute_query(PROPERTY_DETAIL_QUERY, variables)
        prop_data = res.get("property")
        if not prop_data:
            return None
        return Property.model_validate(prop_data)

    async def autocomplete(self, query: str) -> list[AutocompleteItem]:
        """
        Autocomplete / suggest location areas or addresses based on a search term asynchronously.

        Args:
            query: Partially typed address, city, state, or zipcode.

        Returns:
            A list of AutocompleteItem models.
        """
        variables = {"query": query}
        res = await self._execute_query(AUTOCOMPLETE_QUERY, variables)
        autocomplete_data = res.get("autocomplete") or {}
        results = autocomplete_data.get("results") or []
        return [AutocompleteItem.model_validate(item) for item in results]

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
