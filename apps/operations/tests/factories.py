import factory

from apps.counterparties.tests.factories import CounterpartyFactory
from apps.operations.models import Operation


class OperationFactory(factory.DjangoModelFactory):
    counterparty = factory.SubFactory(CounterpartyFactory)

    class Meta:
        model = Operation
