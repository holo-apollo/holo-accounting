from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.counterparties.models import Counterparty
from apps.products.models import Product
from .managers import OrderManager


class Order(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(default=timezone.now)
    deadline = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    objects = OrderManager()

    def __str__(self):
        return f'{self.counterparty} {self.created_at}'

    def is_completed(self):
        return self.completed_at is not None

    def is_delivered(self):
        return self.delivered_at is not None

    def is_overdue(self):
        return not self.delivered_at and self.deadline and self.deadline < timezone.now()

    def time_overdue(self):
        if self.is_overdue():
            return timezone.now() - self.deadline
        return None

    def total_value(self):
        if hasattr(self, 'prepared_total_value'):
            return self.prepared_total_value or 0
        return self.items.all().aggregate(total=models.Sum('total_value'))['total'] or 0

    def total_paid(self):
        if hasattr(self, 'prepared_total_paid'):
            return self.prepared_total_paid or 0
        return self.operations.all().aggregate(total=models.Sum('amount'))['total'] or 0

    def amount_due(self):
        if self.is_completed():
            return self.total_value() - self.total_paid()
        return 0


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    product_quantity = models.DecimalField(max_digits=9, decimal_places=2)
    total_value = models.DecimalField(max_digits=9, decimal_places=2, help_text=_('UAH'))

    def __str__(self):
        return f'{self.order} {self.product}'
