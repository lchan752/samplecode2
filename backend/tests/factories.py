import factory


class CustomerFactoryBase(factory.Factory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    address1 = factory.Faker('street_address')
    address2 = ""
    city = factory.Faker('city')
    state = factory.Faker('state')
    code = factory.Faker('zipcode')

    class Meta:
        abstract = True
