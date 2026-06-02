# reaper/client.py

"""
Synchronous and Asynchronous GraphQL clients to retrieve real estate data from Realtor.com.
"""

from typing import Any, Generator, AsyncGenerator
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
    "rdc-client-name": "realtor-web",
    "rdc-client-version": "1.0.0",
    "apollographql-client-name": "realtor-web",
    "apollographql-client-version": "1.0.0",
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
        operation_name = None
        if "query " in query:
            parts = query.split("query ")
            if len(parts) > 1:
                op_part = parts[1].split("(")[0].split("{")[0].strip()
                if op_part:
                    operation_name = op_part

        payload = {
            "query": query,
            "variables": variables,
        }
        if operation_name:
            payload["operationName"] = operation_name
        try:
            response = self.client.post(self.endpoint, json=payload)
            if response.status_code in (401, 403):
                raise RealtorAuthenticationError(
                    f"Access denied (HTTP {response.status_code}). Realtor.com bot-detection might have blocked this request."
                )

            # Check for detailed GraphQL errors in response body first
            try:
                data = response.json()
                if "errors" in data:
                    raise RealtorAPIError(
                        f"GraphQL query returned errors: {data['errors'][0].get('message')}",
                        errors=data["errors"],
                    )
            except (ValueError, KeyError, IndexError):
                pass

            response.raise_for_status()
            return data.get("data", {})
        except httpx.HTTPStatusError as e:
            body_msg = ""
            try:
                body_msg = f" | Response Body: {e.response.text[:500]}"
            except Exception:
                pass
            raise RealtorRequestError(f"HTTP error occurred: {e}{body_msg}") from e
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
        # Build the search criteria dynamically
        query_criteria = {
            "search_location": {"location": location}
        }
        if status:
            # Convert status strings to lowercase Enums (e.g. "FOR_SALE" -> "for_sale")
            query_criteria["status"] = [s.lower() for s in status]

        # Only add list_price filter if min or max is provided
        if price_min is not None or price_max is not None:
            query_criteria["list_price"] = {}
            if price_min is not None:
                query_criteria["list_price"]["min"] = float(price_min)
            if price_max is not None:
                query_criteria["list_price"]["max"] = float(price_max)

        # Only add beds filter if min or max is provided
        if beds_min is not None or beds_max is not None:
            query_criteria["beds"] = {}
            if beds_min is not None:
                query_criteria["beds"]["min"] = beds_min
            if beds_max is not None:
                query_criteria["beds"]["max"] = beds_max

        # Only add baths filter if min or max is provided
        if baths_min is not None or baths_max is not None:
            query_criteria["baths"] = {}
            if baths_min is not None:
                query_criteria["baths"]["min"] = baths_min
            if baths_max is not None:
                query_criteria["baths"]["max"] = baths_max

        if prop_type:
            query_criteria["type"] = prop_type

        variables = {
            "query": query_criteria,
            "limit": limit,
            "offset": offset,
        }

        res = self._execute_query(PROPERTY_SEARCH_QUERY, variables)
        search_data = res.get("home_search") or {"count": 0, "total": 0, "results": []}
        return HomeSearchResult.model_validate(search_data)

    def search_properties_paginated(
        self,
        location: str,
        page_size: int = 20,
        max_results: int | None = None,
        status: list[str] | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        beds_min: int | None = None,
        beds_max: int | None = None,
        baths_min: float | None = None,
        baths_max: float | None = None,
        prop_type: list[str] | None = None,
    ) -> Generator[Property, None, None]:
        """
        Search for properties matching specified criteria, yielding results dynamically
        page-by-page. Automatically handles offset increments and respects max_results.

        Args:
            location: City/state (e.g. "Austin, TX"), postal code, or location query.
            page_size: Number of results to return per page (default: 20).
            max_results: Maximum total results to yield. If None, yields all available results.
            status: Listing status, e.g. ["for_sale", "for_rent", "sold"].
            price_min: Minimum listing price.
            price_max: Maximum listing price.
            beds_min: Minimum number of bedrooms.
            beds_max: Maximum number of bedrooms.
            baths_min: Minimum number of bathrooms.
            baths_max: Maximum number of bathrooms.
            prop_type: List of property types, e.g. ["single_family", "condo"].

        Yields:
            Property models matching the search criteria.
        """
        offset = 0
        total_yielded = 0
        while True:
            limit = page_size
            if max_results is not None:
                remaining = max_results - total_yielded
                if remaining <= 0:
                    break
                limit = min(page_size, remaining)

            result = self.search_properties(
                location=location,
                limit=limit,
                offset=offset,
                status=status,
                price_min=price_min,
                price_max=price_max,
                beds_min=beds_min,
                beds_max=beds_max,
                baths_min=baths_min,
                baths_max=baths_max,
                prop_type=prop_type,
            )

            if not result.results:
                break

            for prop in result.results:
                yield prop
                total_yielded += 1
                if max_results is not None and total_yielded >= max_results:
                    return

            offset += len(result.results)
            if len(result.results) < limit:
                break

    def get_property_detail(self, property_id: str) -> Property | None:
        """
        Retrieve complete details for a single property by its ID.

        Args:
            property_id: The unique Realtor.com property identifier.

        Returns:
            A Property model or None if not found.
        """
        # 1. Fetch core details using home_search
        search_res = self._execute_query(
            PROPERTY_SEARCH_QUERY,
            {"query": {"property_id": property_id}}
        )
        results = search_res.get("home_search", {}).get("results") or []
        if not results:
            return None
        prop_data = results[0]

        # 2. Fetch history using property query
        try:
            history_res = self._execute_query(
                PROPERTY_DETAIL_QUERY,
                {"property_id": property_id}
            )
            hist_data = history_res.get("property") or {}
            for k, v in hist_data.items():
                if v is not None and k != "property_id":
                    prop_data[k] = v
        except Exception:
            # If the history query fails or isn't supported, we still have core details
            pass

        return Property.model_validate(prop_data)

    def autocomplete(self, query: str) -> list[AutocompleteItem]:
        """
        Autocomplete / suggest location areas or addresses based on a search term.

        Args:
            query: Partially typed address, city, state, or zipcode.

        Returns:
            A list of AutocompleteItem models.
        """
        try:
            response = self.client.get(
                "https://www.realtor.com/api/v1/suggest",
                params={"input": query, "client_id": "rdc-x"}
            )
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
            # Handle GraphQL-style nested data envelopes if present
            suggestion_data = data.get("data") or data
            results = suggestion_data.get("autocomplete") or suggestion_data.get("suggestions") or []
            if isinstance(results, dict):
                results = results.get("results") or []
            return [AutocompleteItem.model_validate(item) for item in results]
        except httpx.HTTPStatusError as e:
            raise RealtorRequestError(f"HTTP error occurred: {e}") from e
        except httpx.RequestError as e:
            raise RealtorRequestError(f"Network error occurred: {e}") from e
        except ValueError as e:
            raise RealtorError(f"Failed to parse JSON response: {e}") from e

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
        operation_name = None
        if "query " in query:
            parts = query.split("query ")
            if len(parts) > 1:
                op_part = parts[1].split("(")[0].split("{")[0].strip()
                if op_part:
                    operation_name = op_part

        payload = {
            "query": query,
            "variables": variables,
        }
        if operation_name:
            payload["operationName"] = operation_name
        try:
            response = await self.client.post(self.endpoint, json=payload)
            if response.status_code in (401, 403):
                raise RealtorAuthenticationError(
                    f"Access denied (HTTP {response.status_code}). Realtor.com bot-detection might have blocked this request."
                )

            # Check for detailed GraphQL errors in response body first
            try:
                data = response.json()
                if "errors" in data:
                    raise RealtorAPIError(
                        f"GraphQL query returned errors: {data['errors'][0].get('message')}",
                        errors=data["errors"],
                    )
            except (ValueError, KeyError, IndexError):
                pass

            response.raise_for_status()
            return data.get("data", {})
        except httpx.HTTPStatusError as e:
            body_msg = ""
            try:
                body_msg = f" | Response Body: {e.response.text[:500]}"
            except Exception:
                pass
            raise RealtorRequestError(f"HTTP error occurred: {e}{body_msg}") from e
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
        # Build the search criteria dynamically
        query_criteria = {
            "search_location": {"location": location}
        }
        if status:
            # Convert status strings to lowercase Enums (e.g. "FOR_SALE" -> "for_sale")
            query_criteria["status"] = [s.lower() for s in status]

        # Only add list_price filter if min or max is provided
        if price_min is not None or price_max is not None:
            query_criteria["list_price"] = {}
            if price_min is not None:
                query_criteria["list_price"]["min"] = float(price_min)
            if price_max is not None:
                query_criteria["list_price"]["max"] = float(price_max)

        # Only add beds filter if min or max is provided
        if beds_min is not None or beds_max is not None:
            query_criteria["beds"] = {}
            if beds_min is not None:
                query_criteria["beds"]["min"] = beds_min
            if beds_max is not None:
                query_criteria["beds"]["max"] = beds_max

        # Only add baths filter if min or max is provided
        if baths_min is not None or baths_max is not None:
            query_criteria["baths"] = {}
            if baths_min is not None:
                query_criteria["baths"]["min"] = baths_min
            if baths_max is not None:
                query_criteria["baths"]["max"] = baths_max

        if prop_type:
            query_criteria["type"] = prop_type

        variables = {
            "query": query_criteria,
            "limit": limit,
            "offset": offset,
        }

        res = await self._execute_query(PROPERTY_SEARCH_QUERY, variables)
        search_data = res.get("home_search") or {"count": 0, "total": 0, "results": []}
        return HomeSearchResult.model_validate(search_data)

    async def search_properties_paginated(
        self,
        location: str,
        page_size: int = 20,
        max_results: int | None = None,
        status: list[str] | None = None,
        price_min: int | None = None,
        price_max: int | None = None,
        beds_min: int | None = None,
        beds_max: int | None = None,
        baths_min: float | None = None,
        baths_max: float | None = None,
        prop_type: list[str] | None = None,
    ) -> AsyncGenerator[Property, None]:
        """
        Search for properties matching specified criteria asynchronously, yielding results dynamically
        page-by-page. Automatically handles offset increments and respects max_results.

        Args:
            location: City/state (e.g. "Austin, TX"), postal code, or location query.
            page_size: Number of results to return per page (default: 20).
            max_results: Maximum total results to yield. If None, yields all available results.
            status: Listing status, e.g. ["for_sale", "for_rent", "sold"].
            price_min: Minimum listing price.
            price_max: Maximum listing price.
            beds_min: Minimum number of bedrooms.
            beds_max: Maximum number of bedrooms.
            baths_min: Minimum number of bathrooms.
            baths_max: Maximum number of bathrooms.
            prop_type: List of property types, e.g. ["single_family", "condo"].

        Yields:
            Property models matching the search criteria.
        """
        offset = 0
        total_yielded = 0
        while True:
            limit = page_size
            if max_results is not None:
                remaining = max_results - total_yielded
                if remaining <= 0:
                    break
                limit = min(page_size, remaining)

            result = await self.search_properties(
                location=location,
                limit=limit,
                offset=offset,
                status=status,
                price_min=price_min,
                price_max=price_max,
                beds_min=beds_min,
                beds_max=beds_max,
                baths_min=baths_min,
                baths_max=baths_max,
                prop_type=prop_type,
            )

            if not result.results:
                break

            for prop in result.results:
                yield prop
                total_yielded += 1
                if max_results is not None and total_yielded >= max_results:
                    return

            offset += len(result.results)
            if len(result.results) < limit:
                break

    async def get_property_detail(self, property_id: str) -> Property | None:
        """
        Retrieve complete details for a single property by its ID asynchronously.

        Args:
            property_id: The unique Realtor.com property identifier.

        Returns:
            A Property model or None if not found.
        """
        # 1. Fetch core details using home_search
        search_res = await self._execute_query(
            PROPERTY_SEARCH_QUERY,
            {"query": {"property_id": property_id}}
        )
        results = search_res.get("home_search", {}).get("results") or []
        if not results:
            return None
        prop_data = results[0]

        # 2. Fetch history using property query
        try:
            history_res = await self._execute_query(
                PROPERTY_DETAIL_QUERY,
                {"property_id": property_id}
            )
            hist_data = history_res.get("property") or {}
            for k, v in hist_data.items():
                if v is not None and k != "property_id":
                    prop_data[k] = v
        except Exception:
            # If the history query fails or isn't supported, we still have core details
            pass

        return Property.model_validate(prop_data)

    async def autocomplete(self, query: str) -> list[AutocompleteItem]:
        """
        Autocomplete / suggest location areas or addresses based on a search term asynchronously.

        Args:
            query: Partially typed address, city, state, or zipcode.

        Returns:
            A list of AutocompleteItem models.
        """
        try:
            response = await self.client.get(
                "https://www.realtor.com/api/v1/suggest",
                params={"input": query, "client_id": "rdc-x"}
            )
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
            # Handle GraphQL-style nested data envelopes if present
            suggestion_data = data.get("data") or data
            results = suggestion_data.get("autocomplete") or suggestion_data.get("suggestions") or []
            if isinstance(results, dict):
                results = results.get("results") or []
            return [AutocompleteItem.model_validate(item) for item in results]
        except httpx.HTTPStatusError as e:
            raise RealtorRequestError(f"HTTP error occurred: {e}") from e
        except httpx.RequestError as e:
            raise RealtorRequestError(f"Network error occurred: {e}") from e
        except ValueError as e:
            raise RealtorError(f"Failed to parse JSON response: {e}") from e

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
