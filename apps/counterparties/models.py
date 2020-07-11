from django.contrib.postgres.fields import CICharField
from django.db import models
from django.utils.translation import gettext_lazy as _


class Counterparty(models.Model):
    name = CICharField(max_length=100, unique=True)
    is_reviewed = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = _('counterparties')

    def __str__(self):
        return self.name + (' (archived)' if self.is_archived else '')


class CounterpartyBankAlias(models.Model):
    counterparty = models.ForeignKey(Counterparty, on_delete=models.CASCADE,
                                     related_name='bank_aliases')
    alias = CICharField(max_length=254, unique=True)

    def __str__(self):
        return self.alias
