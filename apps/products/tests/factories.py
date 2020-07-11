import factory

from apps.products.models import Product, ProductType, Unit


class UnitFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = Unit
        django_get_or_create = ('name',)


class ProductTypeFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')

    class Meta:
        model = ProductType
        django_get_or_create = ('name',)


class ProductFactory(factory.DjangoModelFactory):
    name = factory.Faker('word')
    type = factory.SubFactory(ProductTypeFactory)
    unit = factory.SubFactory(UnitFactory)

    class Meta:
        model = Product
        django_get_or_create = ('name',)
