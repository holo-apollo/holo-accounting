from django.test import TestCase
from django.utils import timezone

from apps.operations.tests.factories import OperationFactory
from apps.orders.models import Order
from .factories import OrderFactory, OrderItemFactory


class OrderTestCase(TestCase):
    def test_amount_due(self):
        order = OrderFactory()
        self.assertEqual(0, order.total_value())
        self.assertEqual(0, order.total_paid())
        self.assertEqual(0, order.amount_due())

        OrderItemFactory(total_value=1000, order=order)
        OrderItemFactory(total_value=2000, order=order)
        self.assertEqual(3000, order.total_value())

        OperationFactory(order=order, amount=500)
        OperationFactory(order=order, amount=600)
        self.assertEqual(1100, order.total_paid())
        self.assertEqual(0, order.amount_due())

        order.completed_at = timezone.now()
        order.save()
        self.assertEqual(1900, order.amount_due())

    def test_amount_due_filtering(self):
        order1 = OrderFactory(completed_at=timezone.now())  # no payment, no value

        order2 = OrderFactory(completed_at=timezone.now())  # has value, no payments
        OrderItemFactory(total_value=1000, order=order2)
        OrderItemFactory(total_value=2000, order=order2)

        order3 = OrderFactory(completed_at=timezone.now())  # no value, has payment
        OperationFactory(order=order3, amount=500)
        OperationFactory(order=order3, amount=600)

        order4 = OrderFactory(completed_at=timezone.now())  # payment is less than value
        OrderItemFactory(total_value=1000, order=order4)
        OrderItemFactory(total_value=2000, order=order4)
        OperationFactory(order=order4, amount=500)
        OperationFactory(order=order4, amount=600)

        order5 = OrderFactory(completed_at=timezone.now())  # payment is equal to value
        OrderItemFactory(total_value=1000, order=order5)
        OrderItemFactory(total_value=2000, order=order5)
        OperationFactory(order=order5, amount=1500)
        OperationFactory(order=order5, amount=1500)

        order6 = OrderFactory(completed_at=timezone.now())  # payment is more than value
        OrderItemFactory(total_value=1000, order=order6)
        OrderItemFactory(total_value=2000, order=order6)
        OperationFactory(order=order6, amount=1500)
        OperationFactory(order=order6, amount=2000)

        order7 = OrderFactory()  # payment is less than value but incomplete
        OrderItemFactory(total_value=1000, order=order4)
        OrderItemFactory(total_value=2000, order=order4)
        OperationFactory(order=order4, amount=500)
        OperationFactory(order=order4, amount=600)

        with_amount_due = Order.objects.with_amount_due()
        without_amount_due = Order.objects.without_amount_due()
        self.assertCountEqual([order2, order4], with_amount_due)
        self.assertCountEqual([order1, order3, order5, order6, order7], without_amount_due)
