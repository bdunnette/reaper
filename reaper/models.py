# reaper/models.py

"""
Pydantic models representing the data structures returned by Realtor.com's frontdoor API.
"""

from pydantic import BaseModel, Field

class Coordinate(BaseModel):
    lat: float | None = None
    lon: float | None = None

class Address(BaseModel):
    line: str | None = None
    city: str | None = None
    state: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    coordinate: Coordinate | None = None

class Location(BaseModel):
    address: Address | None = None

class PropertyDescription(BaseModel):
    beds: int | None = None
    baths: float | None = None
    baths_full: int | None = None
    baths_half: int | None = None
    sqft: int | None = None
    lot_sqft: int | None = None
    year_built: int | None = None
    type: str | None = None
    text: str | None = None

class Photo(BaseModel):
    href: str | None = None

class School(BaseModel):
    name: str | None = None
    rating: int | None = None
    grades: list[str] | str | None = None
    distance: float | None = None
    type: str | None = None

class Assessment(BaseModel):
    building: int | None = None
    land: int | None = None
    total: int | None = None

class TaxHistory(BaseModel):
    tax: int | None = None
    year: int | None = None
    assessment: Assessment | None = None

class PropertyHistory(BaseModel):
    date: str | None = None
    event_name: str | None = None
    price: int | None = None
    sqft: int | None = None

class Property(BaseModel):
    property_id: str
    listing_id: str | None = None
    status: str | None = None
    list_price: int | None = None
    description: PropertyDescription | None = None
    location: Location | None = None
    primary_photo: Photo | None = None
    photos: list[Photo] | None = Field(default_factory=list)
    schools: list[School] | None = Field(default_factory=list)
    tax_history: list[TaxHistory] | None = Field(default_factory=list)
    property_history: list[PropertyHistory] | None = Field(default_factory=list)

class HomeSearchResult(BaseModel):
    count: int
    total: int
    results: list[Property]

    def to_dataframe(self, backend: str | None = None):
        """
        Convert the search results to a Narwhals-compatible DataFrame.

        Args:
            backend: Optional backend name to use (e.g. "polars", "pandas").
                     If None, it will automatically detect and use the first available backend (polars or pandas).

        Returns:
            A narwhals.DataFrame wrapping the generated native DataFrame.
        """
        import narwhals as nw

        if backend is None:
            try:
                import polars as pl
                backend = "polars"
            except ImportError:
                try:
                    import pandas as pd
                    backend = "pandas"
                except ImportError:
                    raise ImportError(
                        "No dataframe backend (polars or pandas) found. "
                        "Please install polars or pandas to use to_dataframe()."
                    )

        flat_data = []
        for prop in self.results:
            desc = prop.description or PropertyDescription()
            addr = prop.location.address if (prop.location and prop.location.address) else Address()
            coord = addr.coordinate if addr else None

            flat_data.append({
                "property_id": prop.property_id,
                "listing_id": prop.listing_id,
                "status": prop.status,
                "list_price": prop.list_price,
                "beds": desc.beds,
                "baths": desc.baths,
                "baths_full": desc.baths_full,
                "baths_half": desc.baths_half,
                "sqft": desc.sqft,
                "lot_sqft": desc.lot_sqft,
                "year_built": desc.year_built,
                "property_type": desc.type,
                "address_line": addr.line,
                "city": addr.city,
                "state_code": addr.state_code,
                "postal_code": addr.postal_code,
                "latitude": coord.lat if coord else None,
                "longitude": coord.lon if coord else None,
                "primary_photo": prop.primary_photo.href if prop.primary_photo else None,
            })

        if not flat_data:
            dict_data = {
                "property_id": [], "listing_id": [], "status": [], "list_price": [],
                "beds": [], "baths": [], "baths_full": [], "baths_half": [],
                "sqft": [], "lot_sqft": [], "year_built": [], "property_type": [],
                "address_line": [], "city": [], "state_code": [], "postal_code": [],
                "latitude": [], "longitude": [], "primary_photo": []
            }
        else:
            keys = flat_data[0].keys()
            dict_data = {k: [item[k] for item in flat_data] for k in keys}

        return nw.from_dict(dict_data, backend=backend)

class AutocompleteItem(BaseModel):
    area_type: str | None = None
    city: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    slug_id: str | None = None
    single_line_address: str | None = None
