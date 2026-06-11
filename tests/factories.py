import factory

class AutocompleteResultFactory(factory.DictFactory):
    area_type = "city"
    city = factory.Iterator(["Austin", "Seattle", "Miami", "Denver"])
    state_code = factory.Iterator(["TX", "WA", "FL", "CO"])
    postal_code = None
    slug_id = factory.LazyAttribute(lambda o: f"{o.city}_{o.state_code}")
    single_line_address = factory.LazyAttribute(lambda o: f"{o.city}, {o.state_code}")

class DescriptionFactory(factory.DictFactory):
    beds = factory.Sequence(lambda n: 2 + (n % 4))
    baths = factory.Sequence(lambda n: 1.5 + (n % 3) * 0.5)
    sqft = factory.Sequence(lambda n: 1200 + (n % 5) * 400)
    year_built = factory.Sequence(lambda n: 1980 + (n % 10) * 5)
    type = "single_family"
    text = "Beautiful home."

class AddressFactory(factory.DictFactory):
    line = factory.Sequence(lambda n: f"{100 + n} Main St")
    city = factory.Iterator(["Austin", "Seattle", "Miami", "Denver"])
    state_code = factory.Iterator(["TX", "WA", "FL", "CO"])
    postal_code = factory.Sequence(lambda n: f"7870{n % 10}")

class LocationFactory(factory.DictFactory):
    address = factory.SubFactory(AddressFactory)

class PropertyFactory(factory.DictFactory):
    property_id = factory.Sequence(lambda n: f"prop_{n}")
    listing_id = factory.Sequence(lambda n: f"list_{n}")
    status = "for_sale"
    list_price = factory.Sequence(lambda n: 300000 + (n % 5) * 100000)
    description = factory.SubFactory(DescriptionFactory)
    location = factory.SubFactory(LocationFactory)
    tax_history = factory.List([{"tax": 5000, "year": 2023}])

class SearchResponseFactory(factory.DictFactory):
    count = 1
    total = 1
    results = factory.List([factory.SubFactory(PropertyFactory)])
