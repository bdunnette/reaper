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

class AutocompleteItem(BaseModel):
    area_type: str | None = None
    city: str | None = None
    state_code: str | None = None
    postal_code: str | None = None
    slug_id: str | None = None
    single_line_address: str | None = None
