import factory

from apps.counterparties.models import Counterparty


class CounterpartyFactory(factory.DjangoModelFactory):
    name = factory.Faker('name')

    class Meta:
        model = Counterparty
        django_get_or_create = ('name',)
