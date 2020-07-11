import factory

from apps.counterparties.tests.factories import CounterpartyFactory
from apps.orders.models import Order, OrderItem
from apps.products.tests.factories import ProductFactory


class OrderFactory(factory.DjangoModelFactory):
    counterparty = factory.SubFactory(CounterpartyFactory)

    class Meta:
        model = Order


class OrderItemFactory(factory.DjangoModelFactory):
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    product_quantity = factory.Faker('random_digit')

    class Meta:
        model = OrderItem
