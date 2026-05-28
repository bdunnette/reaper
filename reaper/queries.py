# reaper/queries.py

"""
GraphQL query definitions for Realtor.com's frontdoor API.
"""

PROPERTY_SEARCH_QUERY = """
query PropertySearch($query: HomeSearchCriteria!, $limit: Int, $offset: Int) {
  home_search(
    query: $query
    limit: $limit
    offset: $offset
  ) {
    count
    total
    results {
      property_id
      listing_id
      status
      list_price
      description {
        beds
        baths
        baths_full
        baths_half
        sqft
        lot_sqft
        year_built
        type
        text
      }
      location {
        address {
          line
          city
          state_code
          postal_code
          coordinate {
            lat
            lon
          }
        }
      }
      primary_photo {
        href
      }
      photos {
        href
      }
    }
  }
}
"""

PROPERTY_DETAIL_QUERY = """
query PropertyDetail($property_id: ID!) {
  property(id: $property_id) {
    property_id
    tax_history {
      tax
      year
      assessment {
        building
        land
        total
      }
    }
    property_history {
      date
      event_name
      price
      sqft
    }
  }
}
"""

AUTOCOMPLETE_QUERY = """
query Autocomplete($query: String!) {
  suggest(query: $query) {
    results {
      area_type
      city
      state_code
      postal_code
      slug_id
      single_line_address
    }
  }
}
"""
