from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.counterparties.models import Counterparty
from apps.orders.models import Order


class Operation(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.PROTECT,
                                     related_name='operations')
    amount = models.DecimalField(max_digits=9, decimal_places=2, help_text=_('UAH'))
    time = models.DateTimeField(default=timezone.now)
    order = models.ForeignKey(Order, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name='operations')
    bank_id = models.CharField(max_length=24, null=True, blank=True, unique=True)
    is_reviewed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.counterparty}, {self.amount} UAH, {self.time}'

    def clean(self):
        if self.order and self.order.counterparty_id != self.counterparty_id:
            raise ValidationError(_("Operation and order counterparties don't match"))
