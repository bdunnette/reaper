# reaper/queries.py

"""
GraphQL query definitions for Realtor.com's frontdoor API.
"""

PROPERTY_SEARCH_QUERY = """
query PropertySearch($location: String!, $limit: Int, $offset: Int, $status: [String!], $priceMin: Int, $priceMax: Int, $bedsMin: Int, $bedsMax: Int, $bathsMin: Float, $bathsMax: Float, $propType: [String!]) {
  home_search(
    query: {
      location: $location
      status: $status
      price: { min: $priceMin, max: $priceMax }
      beds: { min: $bedsMin, max: $bedsMax }
      baths: { min: $bathsMin, max: $bathsMax }
      prop_type: $propType
    }
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
      price_reduced
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
        state
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
    schools {
      name
      rating
      grades
      distance
      type
    }
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
  autocomplete(query: $query) {
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
